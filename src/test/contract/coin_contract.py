import asyncio
import threading

from web3 import Web3
from src.config import ContractConfig, Config


class Coin:
    def __init__(self):
        self.count = 0
        sub_concurrency = ContractConfig.SUB_CURRENCY_CONTRACT
        self.web3 = web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        self.contract = web3.eth.contract(abi=sub_concurrency['abi'], bytecode=sub_concurrency['bytecode'])

    def deploy_new_contract(self):
        tx_hash = self.contract.constructor().buildTransaction({
            "from": Config.ACCOUNT_ADDRESS,
            "nonce": self.web3.eth.getTransactionCount(Config.ACCOUNT_ADDRESS),
        })
        tx_create = self.web3.eth.account.signTransaction(tx_hash, Config.PRIVATE_KEY)

        tx_hash = self.web3.eth.sendRawTransaction(tx_create.rawTransaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt

    def get_minter(self):
        return self.contract.functions.get_minter().call()

    def get_balances(self, account_address):
        return self.contract.functions.get_balances(account_address).call()

    def send(self, receiver, amount):
        build_func = self.contract.functions.send(receiver, amount).buildTransaction(
            {"nonce": self.web3.eth.getTransactionCount(Config.ACCOUNT_ADDRESS)})
        signed_tx = self.web3.eth.account.signTransaction(build_func, Config.PRIVATE_KEY)
        event_tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(event_tx_hash)
        return tx_receipt

    def mint(self, receiver, amount):
        build_func = self.contract.functions.mint(receiver, amount).buildTransaction({
            "nonce": self.web3.eth.getTransactionCount(Config.ACCOUNT_ADDRESS)
        })
        signed_tx = self.web3.eth.account.signTransaction(build_func, Config.PRIVATE_KEY)
        event_tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(event_tx_hash)
        return tx_receipt

    def _get_event(self):
        event_filter = self.contract.events.Sent.createFilter(fromBlock=self.count, toBlock="latest")
        for event in event_filter.get_all_entries():
            self.count = event['blockNumber']
            print(event)

    async def schedule_event_update(self):
        while True:
            event_update_thread = threading.Thread(target=self._get_event)
            event_update_thread.start()
            await asyncio.sleep(200)
