from web3 import Web3


class BaseContract:
    def __init__(self, address: str, abi, web3: Web3):
        self.web3 = web3
        self.address = Web3.to_checksum_address(address)
        self.contract = web3.eth.contract(address=self.address, abi=abi)
