import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ACCOUNT_ADDRESS = "0xd4e94CBA2d3B456ea5a94C62fCaCDedC547367f5"
    PRIVATE_KEY = "0x0d11affeee11621a73ea27348b5420d1a346e02783208a6ec9214aacbed5a072"


class ContractConfig:
    SIMPLE_CONTRACT = json.loads(open(f"{basedir}/contract/abi/simple-contract.json").read())
    SUB_CURRENCY_CONTRACT = json.loads(open(f"{basedir}/contract/abi/sub_currency.json").read())
