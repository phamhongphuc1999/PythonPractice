import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from stable_ethereum_rpc.stable_web3 import StableWeb3

from bep20_contract import Bep20Contract
from config import BscConfig, FtmConfig, EthConfig
from service.logger_service import app_logger
from service.range_block_service import RangeBlockService
from service.telegram_service import send_telegram_message


class EventLogTest:
    def __init__(self, bot_id: str, chat_id: str, config, _id: str):
        self._stable_web3 = StableWeb3(web3_list=config.WEB3_LIST, chain_id=config.CHAIN_ID)
        self._web3 = self._stable_web3.web3()
        self.bot_id = bot_id
        self.chat_id = chat_id
        self.config = config
        self.id = _id
        self.range_block = RangeBlockService(self._stable_web3, self.config.MAXIMUM_RANGE_BLOCK)
        self._contract = Bep20Contract(self.config.TOKEN_ADDRESS, self._stable_web3)

    def _get_event_log(self, from_block: int, to_block: int):
        global event_filter
        error_counter = 0
        transfer_signature_hash = self._contract.get_transfer_event_signature_hash()
        while True:
            try:
                event_filter = self._web3.eth.filter(
                    {
                        "address": self._contract.address,
                        "topics": [[transfer_signature_hash]],
                        "fromBlock": from_block,
                        "toBlock": to_block,
                    }
                )
                filter_log = self._web3.eth.get_filter_logs(event_filter.filter_id)
                result = []
                for filter_item in filter_log:
                    signature_hash = filter_item.topics[0].hex()
                    _log_decode = None
                    if signature_hash == transfer_signature_hash:
                        _log_decode = self._contract.process_transfer_event_log(filter_item)
                        if _log_decode:
                            result.append(_log_decode)
                return result
            except Exception as error:
                error_counter += 1
                if error_counter >= 50:
                    self._web3.eth.uninstall_filter(event_filter.filter_id)
                    result1 = self._stable_web3.set_best_web3()
                    _message = f"{self.id}-rpc: {result1['rpc'].provider_url}"
                    if "currentRpc" in result1:
                        _message += f", Current RPC: {result1['currentRpc'].provider_url}"
                    send_telegram_message(_message, self.bot_id, self.chat_id)
                    return None
                time.sleep(1)

    def run(self):
        _data = self.range_block.update_block_range()
        if _data:
            from_block = _data["from"]
            to_block = _data["to"]
            _filter_log_list = self._get_event_log(from_block, to_block)
            if len(_filter_log_list) > 0:
                send_telegram_message(f"{self.id} event: {len(_filter_log_list)}", self.bot_id, self.chat_id)

    def run_task(self):
        while True:
            try:
                self.run()
            except Exception as error:
                send_telegram_message(f"{self.id}: {str(error)}", self.bot_id, self.chat_id)
            finally:
                time.sleep(3)


class RunClass:
    def __init__(self, bot_id: str, chat_id: str):
        _max_workers = min(32, os.cpu_count() + 4)
        self._executor = ThreadPoolExecutor(max_workers=_max_workers)
        self.bot_id = bot_id
        self.chat_id = chat_id

    def submit(self):
        _bsc_event_log = EventLogTest(self.bot_id, self.chat_id, BscConfig, "bsc")
        _ftm_event_log = EventLogTest(self.bot_id, self.chat_id, FtmConfig, "ftm")
        _eth_event_log = EventLogTest(self.bot_id, self.chat_id, EthConfig, "eth")
        self._executor.submit(_bsc_event_log.run_task)
        self._executor.submit(_ftm_event_log.run_task)
        self._executor.submit(_eth_event_log.run_task)


if __name__ == "__main__":
    _arg = sys.argv
    _run = RunClass(_arg[1], _arg[2])
    _run.submit()
