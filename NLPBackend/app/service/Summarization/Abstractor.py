import json
import pickle as pkl
from itertools import starmap
from os.path import join

import torch
from cytoolz import curry

from app.data.batcher import conver2id, pad_batch_tensorize
from app.models.CopySum import CopySumm
from app.service import load_best_ckpt
from app.service.make_token import UNK, PAD, START, END


class Abstractor(object):
    def __init__(self, abs_dir, max_len=30, cuda=False):
        abs_meta = json.load(open(join(abs_dir, "meta.json")))
        assert abs_meta["net"] == "base_abstractor"
        abs_args = abs_meta["net_args"]
        abs_ckpt = load_best_ckpt(abs_dir)
        word2id = pkl.load(open(join(abs_dir, "vocab.pkl"), "rb"))
        abstractor = CopySumm(**abs_args)
        abstractor.load_state_dict(abs_ckpt)
        self._device = torch.device("cuda" if cuda else "cpu")
        self._net = abstractor.to(self._device)
        self._word2id = word2id
        self._id2word = {i: w for w, i in word2id.items()}
        self._max_len = max_len

    def _prepro(self, raw_article_sents):
        ext_word2id = dict(self._word2id)
        ext_id2word = dict(self._id2word)
        for raw_words in raw_article_sents:
            for w in raw_words:
                if not w in ext_word2id:
                    ext_word2id[w] = len(ext_word2id)
                    ext_id2word[len(ext_id2word)] = w
        articles = conver2id(UNK, self._word2id, raw_article_sents)
        art_lens = [len(art) for art in articles]
        article = pad_batch_tensorize(articles, PAD, cuda=False).to(self._device)
        extend_arts = conver2id(UNK, ext_word2id, raw_article_sents)
        extend_art = pad_batch_tensorize(extend_arts, PAD, cuda=False).to(self._device)
        extend_vsize = len(ext_word2id)
        dec_args = (article, art_lens, extend_art, extend_vsize, START, END, UNK, self._max_len)
        return dec_args, ext_id2word

    def __call__(self, raw_article_sents):
        self._net.eval()
        dec_args, id2word = self._prepro(raw_article_sents)
        decs, attns = self._net.batch_decode(*dec_args)

        def argmax(arr, keys):
            return arr[max(range(len(arr)), key=lambda i: keys[i].item())]

        dec_sents = []
        for i, raw_words in enumerate(raw_article_sents):
            dec = []
            for id_, attn in zip(decs, attns):
                if id_[i] == END:
                    break
                elif id_[i] == UNK:
                    dec.append(argmax(raw_words, attn[i]))
                else:
                    dec.append(id2word[id_[i].item()])
            dec_sents.append(dec)
        return dec_sents


@curry
def _process_beam(id2word, beam, art_sent):
    def process_hyp(hyp):
        seq = []
        for i, attn in zip(hyp.sequence[1:], hyp.attns[:-1]):
            if i == UNK:
                copy_word = art_sent[max(range(len(art_sent)), key=lambda j: attn[j].item())]
                seq.append(copy_word)
            else:
                seq.append(id2word[i])
        hyp.sequence = seq
        del hyp.hists
        del hyp.attns
        return hyp

    return list(map(process_hyp, beam))


class BeamAbstractor(Abstractor):
    def __call__(self, raw_article_sents, beam_size=5, diverse=1.0):
        self._net.eval()
        dec_args, id2word = self._prepro(raw_article_sents)
        dec_args = (*dec_args, beam_size, diverse)
        all_beams = self._net.batched_beamsearch(*dec_args)
        all_beams = list(starmap(_process_beam(id2word), zip(all_beams, raw_article_sents)))
        return all_beams
