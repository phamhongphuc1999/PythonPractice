import os
from os.path import join
import re

import torch


def make_html_safe(s):
    """Rouge use html, has to make output html safe"""
    return s.replace("<", "&lt;").replace(">", "&gt;")


def load_best_ckpt(model_dir, reverse=False):
    """reverse=False->loss, reverse=True->reward/score"""
    ckpts = os.listdir(join(model_dir, "ckpt"))
    ckpt_matcher = re.compile("^ckpt-.*-[0-9]*")
    ckpts = sorted(
        [c for c in ckpts if ckpt_matcher.match(c)],
        key=lambda c: float(c.split("-")[1]),
        reverse=reverse,
    )
    ckpt = torch.load(
        join(model_dir, "ckpt/{}".format(ckpts[0])), map_location=torch.device("cpu")
    )["state_dict"]
    return ckpt
