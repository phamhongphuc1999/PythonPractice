from web3 import Web3
from src.web3.config import ContractConfig, Config

contract_address = "0x4dbCAf20808da752D0aD337ad44de05d0A678093"

# get provider
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


# create and send transaction for set data from smart contract
def set_data(simple_contract, data):
    set_hash = simple_contract.functions.set_data(data).buildTransaction(
        {"nonce": web3.eth.getTransactionCount(Config.ACCOUNT_ADDRESS)}
    )
    signed_tx = web3.eth.account.signTransaction(set_hash, Config.PRIVATE_KEY)
    set_tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(set_tx_hash)
    return tx_receipt


# create and send transaction for call event
def send_event(simple_contract):
    event_hash = simple_contract.functions.increase().buildTransaction(
        {"nonce": web3.eth.getTransactionCount(Config.ACCOUNT_ADDRESS)}
    )
    signed_tx = web3.eth.account.signTransaction(event_hash, Config.PRIVATE_KEY)
    event_tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(event_tx_hash)
    return tx_receipt


def run_interact_contract():
    simple_interface = ContractConfig.SIMPLE_CONTRACT
    simple_contract = web3.eth.contract(
        address=contract_address, abi=simple_interface["abi"]
    )
    set_data(simple_contract, 100)

    # get data from smart contract
    print(simple_contract.functions.get_data().call())

    result = send_event(simple_contract)
    print(result)

    # listen event
    increase_event = simple_contract.events.Increase.createFilter(
        fromBlock=0, toBlock="latest"
    )
    print("event", increase_event)
    increase_event = increase_event.get_all_entries()
    for event in increase_event:
        print(event)
