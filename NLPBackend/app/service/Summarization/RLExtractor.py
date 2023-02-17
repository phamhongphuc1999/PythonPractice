import json
from os.path import join
import pickle as pkl

import torch

from app.data.batcher import pad_batch_tensorize, conver2id
from app.models.extract import PtrExtractSumm
from app.models.rl import ActorCritic
from app.service import load_best_ckpt
from app.service.make_token import UNK, PAD


class ArticleBatcher(object):
    def __init__(self, word2id, cuda=True):
        self._device = torch.device("cuda" if cuda else "cpu")
        self._word2id = word2id
        self._device = torch.device("cuda" if cuda else "cpu")

    def __call__(self, raw_article_sents):
        articles = conver2id(UNK, self._word2id, raw_article_sents)
        article = pad_batch_tensorize(articles, PAD, cuda=False).to(self._device)
        return article


class RLExtractor(object):
    def __init__(self, ext_dir, cuda=False):
        ext_meta = json.load(open(join(ext_dir, "meta.json")))
        assert ext_meta["net"] == "rnn-ext_abs_rl"
        ext_args = ext_meta["net_args"]["extractor"]["net_args"]
        word2id = pkl.load(open(join(ext_dir, "agent_vocab.pkl"), "rb"))
        extractor = PtrExtractSumm(**ext_args)
        agent = ActorCritic(
            extractor._sent_enc, extractor._art_enc, extractor._extractor, ArticleBatcher(word2id, cuda)
        )
        ext_ckpt = load_best_ckpt(ext_dir, reverse=True)
        agent.load_state_dict(ext_ckpt)
        self._device = torch.device("cuda" if cuda else "cpu")
        self._net = agent.to(self._device)
        self._word2id = word2id
        self._id2word = {i: w for w, i in word2id.items()}

    def __call__(self, raw_article_sents):
        self._net.eval()
        indices = self._net(raw_article_sents)
        return indices
