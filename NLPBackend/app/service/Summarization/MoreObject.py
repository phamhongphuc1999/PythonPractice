from app.config.constants import AppConfig
from app.data.data import CnnDmDataset


class DecodeDataset(CnnDmDataset):
    """get the article sentences only (for decoding use)"""

    def __init__(self, split):
        assert split in ["val", "test"]
        super().__init__(split, AppConfig.DATA_DIR)

    def __getitem__(self, i):
        js_data = super().__getitem__(i)
        art_sents = js_data["article"]
        return art_sents
