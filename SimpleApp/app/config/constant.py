class EnvironmentType:
    DEV_DOCKER = "dev_docker"  # connect to local docker database and build project to docker container
    DEVELOPMENT = "development"  # connect to local database without docker
    BASIC = "basic"  # run project directly without docker or database


class Network:
    BSC_MAINNET = "bsc_mainnet"
    FTM_MAINNET = "ftm_mainnet"
    BSC_TESTNET = "bsc_testnet"


TELEGRAM_GET_METHODS = ["getChat", "getMe", "getMyCommands"]
ALL_METHODS = ["getUpdates", "setMyCommands", "getWebhookInfo", "setWebhook"]
ALL_METHODS.extend(TELEGRAM_GET_METHODS)
