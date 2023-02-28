import json
import os

from stable_ethereum_rpc.config import ChainId

basedir = os.path.abspath(os.path.dirname(__file__))

BEP20_ABI = json.loads(open(f"{basedir}/resources/bep20_abi.json", "r").read())


class BscConfig:
    WEB3_LIST = [
        "https://bsc-dataseed234567.ninicoin.io",
        "https://bsc-dataseed.binance.org",
        "https://bsc-dataseed1.binance.org",
        "https://bsc-dataseed1.defibit.io",
        "https://bsc-dataseed2.defibit.io",
        "https://bsc-dataseed1.ninicoin.io",
        "https://bsc-dataseed2.ninicoin.io",
        "https://bsc.blockpi.network/v1/rpc/public",
        "https://endpoints.omniatech.io/v1/bsc/mainnet/public",
    ]
    CHAIN_ID = ChainId.BSC_MAINNET
    TOKEN_ADDRESS = "0x55d398326f99059fF775485246999027B3197955"
    MAXIMUM_RANGE_BLOCK = 100


class FtmConfig:
    WEB3_LIST = [
        "https://rpc.ankr.com/fantom",
        "https://fantom.blockpi.network/v1/rpc/public",
        "https://rpc.ftm.tools",
        "https://rpc.fantom.network",
        "https://rpc2.fantom.network",
        "https://rpc3.fantom.network",
        "https://fantom-mainnet.public.blastapi.io",
    ]
    CHAIN_ID = ChainId.FTM_MAINNET
    TOKEN_ADDRESS = "0xe1146b9AC456fCbB60644c36Fd3F868A9072fc6E"
    MAXIMUM_RANGE_BLOCK = 300


class EthConfig:
    WEB3_LIST = [
        "https://eth.llamarpc.com",
        "https://singapore.rpc.blxrbdn.com",
        "https://ethereum.blockpi.network/v1/rpc/public",
        "https://eth-mainnet-public.unifra.io",
        "https://virginia.rpc.blxrbdn.com",
        "https://uk.rpc.blxrbdn.com",
    ]
    CHAIN_ID = ChainId.ETH_MAINNET
    TOKEN_ADDRESS = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    MAXIMUM_RANGE_BLOCK = 20
