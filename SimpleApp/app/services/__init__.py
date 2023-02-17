import sys

from app.config import EnvironmentType


def get_env():
    _args = sys.argv
    if len(_args) < 2:
        raise Exception("environment is required")
    elif _args[1] == "development":
        return EnvironmentType.DEVELOPMENT
    elif _args[1] == "dev_docker":
        return EnvironmentType.DEV_DOCKER
    elif _args[1] == "basic":
        return EnvironmentType.BASIC
    else:
        raise Exception(f"Not found {_args[1]}")
