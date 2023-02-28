from stable_ethereum_rpc.stable_web3 import StableWeb3

from config import BEP20_ABI


class Bep20Contract:
    def __init__(self, address, web3: StableWeb3):
        self.web3 = web3.web3()
        self.address = web3.web3().toChecksumAddress(address)
        self.contract = web3.web3().eth.contract(address=self.address, abi=BEP20_ABI)

    def get_transfer_event_signature_hash(self):
        return self.web3.keccak(text="Transfer(address,address,uint256)").hex()

    def process_transfer_event_log(self, transaction_log):
        try:
            return self.contract.events.Transfer().processLog(transaction_log)
        except Exception as error:
            return None
