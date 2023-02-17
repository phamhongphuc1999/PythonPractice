from sanic import Blueprint, Request

from app import AppConfig
from app.apis import require_params
from app.apis.api_response import bad_request_json, ok_json
from app.config.constant import Network
from app.contract.bep20_contract import Bep20Contract

bep20_blueprint = Blueprint("bep20_blueprint", url_prefix="/bep20")


@bep20_blueprint.get("/networks")
async def get_network(request: Request):
    try:
        return ok_json(Network)
    except Exception as error:
        return bad_request_json(str(error))


@bep20_blueprint.get("/data")
async def get_data(request: Request):
    try:
        require_params(request, ["address"])
        token_address = request.args.get("address")
        _network = request.args.get("network")
        _web3 = None
        if _network is None:
            _web3 = AppConfig.Network.BSC_MAINNET.Provider.PROVIDER1
            _network = Network.BSC_MAINNET
        else:
            _web3 = AppConfig.Network.config(_network).Provider.PROVIDER1
        bep20_contract = Bep20Contract(token_address, _web3)
        _decimal = bep20_contract.decimals()
        _name = bep20_contract.name()
        return ok_json({"data": {"decimal": _decimal, "name": _name}, "network": _network})
    except Exception as error:
        return bad_request_json(str(error))


@bep20_blueprint.get("/balance")
async def get_balance(request: Request):
    try:
        require_params(request, ["address", "account"])
        token_address = request.args.get("address")
        account_address = request.args.get("account")
        _network = request.args.get("network")
        _web3 = None
        if _network is None:
            _web3 = AppConfig.Network.BSC_MAINNET.Provider.PROVIDER1
            _network = Network.BSC_MAINNET
        else:
            _web3 = AppConfig.Network.config(_network).Provider.PROVIDER1
        bep20_contract = Bep20Contract(token_address, _web3)
        account_balance = bep20_contract.balance_of(account_address)
        _decimal = bep20_contract.decimals()
        return ok_json({"balance": account_balance / (10**_decimal), "network": _network})
    except Exception as error:
        return bad_request_json(str(error))
