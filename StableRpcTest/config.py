from stable_ethereum_rpc.config import ChainId

BEP20_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    }
]


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
    TOKEN_ADDRESS = "0x0391bE54E72F7e001f6BBc331777710b4f2999Ef"


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
    TOKEN_ADDRESS = "0x477a9D5dF9bedA06F6b021136a2efe7BE242fCC9"


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
    TOKEN_ADDRESS = "0x186D0Ba3dfC3386C464eECd96A61fBB1E2dA00bf"
