import sys
import time
from stable_ethereum_rpc.stable_web3 import StableWeb3
from config import BscConfig, FtmConfig, BEP20_ABI, EthConfig
from service.logger_service import get_logger
from service.telegram_service import send_telegram_message


def _tracking(message: str, app_logger, bot_id, chat_id):
    app_logger.info(message)
    send_telegram_message(message, bot_id, chat_id)


def run(_stable_web3, token_address, text: str, app_logger, bot_id, chat_id):
    app_logger.info(
        f"{text} Set best web3======================================================="
    )
    result1 = _stable_web3.set_best_web3()
    bep_contract = _stable_web3.web3().eth.contract(
        address=token_address, abi=BEP20_ABI
    )
    token_balance = bep_contract.functions.balanceOf(
        "0x871DBcE2b9923A35716e7E83ee402B535298538E"
    ).call()
    _message = f"{text}-balance: {token_balance}, rpc: {result1['rpc'].provider_url}"
    if "currentRpc" in result1:
        _message += f", Current RPC: {result1['currentRpc'].provider_url}"
    _tracking(_message, app_logger, bot_id, chat_id)


if __name__ == "__main__":
    _arg = sys.argv
    _config = None
    _text = ""
    if _arg[1] == "bsc":
        _config = BscConfig
        _text = "BSC"
    elif _arg[1] == "ftm":
        _config = FtmConfig
        _text = "FTM"
    elif _arg[1] == "eth":
        _config = EthConfig
        _text = "ETH"
    if _config is not None:
        _app_logger = get_logger(_text, f"{_text.lower()}.log")
        stable_web3_entity = StableWeb3(
            web3_list=_config.WEB3_LIST, chain_id=_config.CHAIN_ID
        )
        while True:
            try:
                run(
                    stable_web3_entity,
                    _config.TOKEN_ADDRESS,
                    _text,
                    _app_logger,
                    _arg[2],
                    _arg[3],
                )
            except Exception as error:
                print(error)
            finally:
                time.sleep(300)
