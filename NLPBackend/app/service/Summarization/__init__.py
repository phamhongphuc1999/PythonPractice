import json
import os
from collections import Counter, defaultdict
from datetime import timedelta
from functools import reduce
from itertools import product
from os.path import join

import torch
from cytoolz import identity, concat, curry
from torch.utils.data import DataLoader

from app.data.batcher import tokenize
from app.service import make_html_safe
from app.service.Summarization.Abstractor import Abstractor, BeamAbstractor
from app.service.Summarization.MoreObject import DecodeDataset
from app.service.Summarization.RLExtractor import RLExtractor
from app.service.make_token import tokenize_stories, get_article
from time import time
from torch import multiprocessing as mp
import operator as op

_PRUNE = defaultdict(lambda: 2, {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 4, 7: 3, 8: 3})


def coll(batch):
    articles = list(filter(bool, batch))
    return articles


def rerank_one(beams):
    @curry
    def process_beam(beam, n):
        for b in beam[:n]:
            b.gram_cnt = Counter(_make_n_gram(b.sequence))
        return beam[:n]

    beams = map(process_beam(n=_PRUNE[len(beams)]), beams)
    best_hyps = max(product(*beams), key=_compute_score)
    dec_outs = [h.sequence for h in best_hyps]
    return dec_outs


def _make_n_gram(sequence, n=2):
    return (tuple(sequence[i : i + n]) for i in range(len(sequence) - (n - 1)))


def _compute_score(hyps):
    all_cnt = reduce(op.iadd, (h.gram_cnt for h in hyps), Counter())
    repeat = sum(c - 1 for g, c in all_cnt.items() if c > 1)
    lp = sum(h.logprob for h in hyps) / sum(len(h.sequence) for h in hyps)
    return (-repeat, lp)


def rerank(all_beams, ext_inds):
    beam_lists = (all_beams[i : i + n] for i, n in ext_inds if n > 0)
    return list(concat(map(rerank_one, beam_lists)))


def rerank_mp(all_beams, ext_inds):
    beam_lists = [all_beams[i : i + n] for i, n in ext_inds if n > 0]
    with mp.Pool(8) as pool:
        reranked = pool.map(rerank_one, beam_lists)
    return list(concat(reranked))


def decode_more(save_path, model_dir, split, batch_size, beam_size, diverse, max_len, cuda):
    start = time()
    # setup model
    with open(join(model_dir, "meta.json")) as f:
        meta = json.loads(f.read())
    if meta["net_args"]["abstractor"] is None:
        # NOTE: if no abstractor is provided then
        #       the whole model would be extractive summarization
        assert beam_size == 1
        abstractor = identity
    else:
        if beam_size == 1:
            abstractor = Abstractor(join(model_dir, "abstractor"), max_len, cuda)
        else:
            abstractor = BeamAbstractor(join(model_dir, "abstractor"), max_len, cuda)
    extractor = RLExtractor(model_dir, cuda=cuda)
    dataset = DecodeDataset(split)
    n_data = len(dataset)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=4, collate_fn=coll)

    # prepare save paths and logs
    os.makedirs(join(save_path, "output"))
    dec_log = {}
    dec_log["abstractor"] = meta["net_args"]["abstractor"]
    dec_log["extractor"] = meta["net_args"]["extractor"]
    dec_log["rl"] = True
    dec_log["split"] = split
    dec_log["beam"] = beam_size
    dec_log["diverse"] = diverse
    with open(join(save_path, "log.json"), "w") as f:
        json.dump(dec_log, f, indent=4)

    # Decoding
    i = 0
    with torch.no_grad():
        for i_debug, raw_article_batch in enumerate(loader):
            tokenized_article_batch = map(tokenize(None), raw_article_batch)
            ext_arts = []
            ext_inds = []
            for raw_art_sents in tokenized_article_batch:
                ext = extractor(raw_art_sents)[:-1]  # exclude EOE
                if not ext:
                    # use top-5 if nothing is extracted
                    # in some rare cases rnn-ext does not extract at all
                    ext = list(range(5))[: len(raw_art_sents)]
                else:
                    ext = [i.item() for i in ext]
                ext_inds += [(len(ext_arts), len(ext))]
                ext_arts += [raw_art_sents[i] for i in ext]
            if beam_size > 1:
                all_beams = abstractor(ext_arts, beam_size, diverse)
                dec_outs = rerank_mp(all_beams, ext_inds)
            else:
                dec_outs = abstractor(ext_arts)
            assert i == batch_size * i_debug
            for j, n in ext_inds:
                decoded_sents = [" ".join(dec) for dec in dec_outs[j : j + n]]
                with open(join(save_path, "output/{}.dec".format(i)), "w") as f:
                    f.write(make_html_safe("\n".join(decoded_sents)))
                i += 1
                print(
                    "{}/{} ({:.2f}%) decoded in {} seconds\r".format(
                        i, n_data, i / n_data * 100, timedelta(seconds=int(time() - start))
                    ),
                    end="",
                )
    print()


def decode(story: str, model_dir, beam_size, max_len, cuda=False):
    with open(join(model_dir, "meta.json")) as f:
        meta = json.loads(f.read())

    if meta["net_args"]["abstractor"] is None:
        assert beam_size == 1
        abstractor = identity
    else:
        if beam_size == 1:
            abstractor = Abstractor(join(model_dir, "abstractor"), max_len, cuda)
        else:
            abstractor = BeamAbstractor(join(model_dir, "abstractor"), max_len, cuda)
    extractor = RLExtractor(model_dir, cuda=cuda)
    _embedding_article = tokenize_stories(story)
    raw_article_data = get_article(_embedding_article)
    i = 0
    with torch.no_grad():
        _raw_art_sents = map(tokenize(None), [raw_article_data])
        ext_arts = []
        ext_inds = []
        counter = 0
        for raw_art_sents in _raw_art_sents:
            counter += 1
            ext = extractor(raw_art_sents)[:-1]
            if not ext:
                ext = list(range(5))[: len(raw_art_sents)]
            else:
                ext = [i.item() for i in ext]
            ext_inds += [(len(ext_arts), len(ext))]
            ext_arts += [raw_art_sents[i] for i in ext]

        # abstraction
        if beam_size > 1:
            all_beams = abstractor(ext_arts, beam_size, 1.0)
            dec_outs = rerank_mp(all_beams, ext_inds)
        else:
            dec_outs = abstractor(ext_arts)
        j, n = ext_inds[0]
        decoded_sents = [" ".join(dec) for dec in dec_outs[j : j + n]]
        result = make_html_safe("\n".join(decoded_sents))
        return result