from web3 import Web3


def run_provider():
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    # check is connected of provider
    print("check is connected of provider", web3.isConnected())

    # get a block by number
    print("get a block by number", web3.eth.get_block(1))

    # get a block by it's hash
    print(
        "get a block by it's hash",
        web3.eth.get_block(
            "0x05c7011215ba400f41d13856fac57043d6a3c8a9eb1fe8fa66730d1e6f1c6b9b"
        ),
    )

    # get account balance
    balance = web3.eth.get_balance("0xfdA7F1F58f7f5e9A1F409028f28B89D2aD56670b")
    print("get account balance", balance)

    # convert wei to eth
    print("convert wei to eth", Web3.fromWei(balance, "ether"))
