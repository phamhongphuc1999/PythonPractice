from web3 import Web3
from src.config import ContractConfig, Config


def run_contract():
    simple_interface = ContractConfig.SIMPLE_CONTRACT

    # get provider
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    contract = web3.eth.contract(abi=simple_interface['abi'], bytecode=simple_interface['bytecode'])

    tx_hash = contract.constructor().buildTransaction({
        "from": Config.ACCOUNT_ADDRESS,
        "nonce": web3.eth.getTransactionCount(Config.ACCOUNT_ADDRESS),
    })

    tx_create = web3.eth.account.signTransaction(tx_hash, Config.PRIVATE_KEY)

    tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    print("tx receipt", tx_receipt)
    print("contract address", tx_receipt['contractAddress'])
