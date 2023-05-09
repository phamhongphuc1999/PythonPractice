from web3 import Web3

from app import AppConfig
from app.contract import BaseContract


class Bep20Contract(BaseContract):
    def __init__(self, address: str, web3: Web3):
        super().__init__(address, AppConfig.Global.ABI.BEP20_ABI, web3)

    def decimals(self):
        return self.contract.functions.decimals().call()

    def name(self):
        return self.contract.functions.name().call()

    def balance_of(self, account_address: str, block_identifier=None):
        checksum_account_address = Web3.toChecksumAddress(account_address)
        if block_identifier is not None:
            return self.contract.functions.balanceOf(checksum_account_address).call(block_identifier=block_identifier)
        return self.contract.functions.balanceOf(checksum_account_address).call()
