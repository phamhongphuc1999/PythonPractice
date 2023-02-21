from web3 import Web3
from web3.middleware import geth_poa_middleware

from app.config.constant import Network


def create_http_provider(provider_uri):
    _web3 = Web3(Web3.HTTPProvider(provider_uri))
    _web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return _web3


class BscMainnetConfig:
    class Provider:
        PROVIDER1 = create_http_provider("https://bsc-dataseed1.defibit.io/")


class FtmMainnetConfig:
    class Provider:
        PROVIDER1 = create_http_provider("https://rpc.ftm.tools/")


class BscTestnetConfig:
    class Provider:
        PROVIDER1 = create_http_provider(
            "https://data-seed-prebsc-1-s3.binance.org:8545/"
        )


class NetworkConfig:
    def __init__(self):
        self.BSC_MAINNET = BscMainnetConfig()
        self.FTM_MAINNET = FtmMainnetConfig()
        self.BSC_TESTNET = BscTestnetConfig()

    def config(self, _network: Network):
        if _network == Network.BSC_MAINNET:
            return self.BSC_MAINNET
        elif _network == Network.FTM_MAINNET:
            return self.FTM_MAINNET
        elif _network == Network.BSC_TESTNET:
            return self.BSC_TESTNET
        else:
            raise Exception(f"Not found {_network} network config")
