from web3 import Web3


def run_icp_provider():
    web3 = Web3(Web3.IPCProvider("~/Library/Ethereum/geth.ipc"))

    print(web3.isConnected())
