from stable_ethereum_rpc.stable_web3 import StableWeb3


class RangeBlockService:
    def __init__(self, _web3: StableWeb3, max_range: int):
        self.web3 = _web3
        self.max_range = max_range
        _init_block = self.web3.web3().eth.get_block("latest")["number"]
        self._old_current_block = _init_block
        self._old_block = _init_block

    def update_block_range(self):
        current_block = self.web3.web3().eth.get_block("latest")["number"]
        if self._old_current_block != current_block:
            self._old_current_block = current_block
            if self._old_block < current_block:
                _from_block = self._old_block + 1
                _to_block = current_block
                if _to_block - _from_block > self.max_range:
                    _from_block = _to_block
                self._old_block = _to_block
                return {"from": _from_block, "to": _to_block}
        return False
