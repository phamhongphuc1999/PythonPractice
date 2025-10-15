import math
from typing import Callable, Dict, List, Literal, Optional, TypedDict
from enum import Enum

BlockMode = Optional[Literal["opposite", "wall"]]
GameStatusMode = Literal["playing", "ended"]

class CaroWinType(str, Enum):
    LEFT_DIAGONAL = "leftDiagonal"
    RIGHT_DIAGONAL = "rightDiagonal"
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class ParamsType(TypedDict):
    steps: Dict[int, int]
    currentStep: int
    currentPlayer: int
    numberOfRows: int
    numberOfColumns: int


class SideReturnType(TypedDict):
    cells: List[int]
    blockMode: BlockMode


class WinStateType(TypedDict):
    locations: Dict[int, Dict[str, bool]]
    winMode: List[CaroWinType]

def caro_check(
    params: ParamsType,
    step_should_be_check_func: Callable[[ParamsType], int],
    checking_step_func: Callable[[ParamsType, int], int],
) -> SideReturnType:
    steps = params["steps"]
    current_step = params["currentStep"]
    current_player = params["currentPlayer"]

    steps_should_be_check = step_should_be_check_func(params)
    checking_step = current_step
    counter = 0
    result: List[int] = []
    block_mode: BlockMode = None

    while steps_should_be_check > counter:
        checking_step = checking_step_func(params, checking_step)
        if steps.get(checking_step) == current_player:
            counter += 1
            result.append(checking_step)
        else:
            if checking_step in steps:
                block_mode = "opposite"
            break

    if counter >= steps_should_be_check:
        block_mode = "wall"

    return {"cells": result, "blockMode": block_mode}

def check_top_left_diagonal(params: ParamsType):
    return caro_check(
        params,
        lambda p: min(p["currentStep"] % p["numberOfColumns"], math.floor(p["currentStep"] / p["numberOfColumns"])),
        lambda p, checking_step: checking_step - (p["numberOfColumns"] + 1),
    )


def check_top_vertical(params: ParamsType):
    return caro_check(
        params,
        lambda p: math.floor(p["currentStep"] / p["numberOfColumns"]),
        lambda p, checking_step: checking_step - p["numberOfColumns"],
    )


def check_top_right_diagonal(params: ParamsType):
    return caro_check(
        params,
        lambda p: min(
            p["numberOfColumns"] - (p["currentStep"] % p["numberOfColumns"]) - 1,
            math.floor(p["currentStep"] / p["numberOfColumns"]),
        ),
        lambda p, checking_step: checking_step - p["numberOfColumns"] + 1,
    )


def check_bottom_left_diagonal(params: ParamsType):
    return caro_check(
        params,
        lambda p: min(
            p["currentStep"] % p["numberOfColumns"],
            p["numberOfRows"] - math.floor(p["currentStep"] / p["numberOfColumns"]) - 1,
        ),
        lambda p, checking_step: checking_step + p["numberOfColumns"] - 1,
    )


def check_bottom_vertical(params: ParamsType):
    return caro_check(
        params,
        lambda p: p["numberOfRows"] - math.floor(p["currentStep"] / p["numberOfColumns"]) - 1,
        lambda p, checking_step: checking_step + p["numberOfColumns"],
    )


def check_bottom_right_diagonal(params: ParamsType):
    return caro_check(
        params,
        lambda p: min(
            p["numberOfColumns"] - (p["currentStep"] % p["numberOfColumns"]) - 1,
            p["numberOfRows"] - math.floor(p["currentStep"] / p["numberOfColumns"]) - 1,
        ),
        lambda p, checking_step: checking_step + p["numberOfColumns"] + 1,
    )


def check_left_horizontal(params: ParamsType):
    return caro_check(
        params,
        lambda p: p["currentStep"] % p["numberOfColumns"],
        lambda _, checking_step: checking_step - 1,
    )


def check_right_horizontal(params: ParamsType):
    return caro_check(
        params,
        lambda p: p["numberOfColumns"] - (p["currentStep"] % p["numberOfColumns"]) - 1,
        lambda _, checking_step: checking_step + 1,
    )

config: Dict[CaroWinType, Dict[str, Callable[[ParamsType], SideReturnType]]] = {
    CaroWinType.LEFT_DIAGONAL: {
        "side1Func": check_top_left_diagonal,
        "side2Func": check_bottom_right_diagonal,
    },
    CaroWinType.RIGHT_DIAGONAL: {
        "side1Func": check_top_right_diagonal,
        "side2Func": check_bottom_left_diagonal,
    },
    CaroWinType.VERTICAL: {
        "side1Func": check_top_vertical,
        "side2Func": check_bottom_vertical,
    },
    CaroWinType.HORIZONTAL: {
        "side1Func": check_left_horizontal,
        "side2Func": check_right_horizontal,
    },
}

def _analytic_step(type_: CaroWinType, params: ParamsType, number_to_win: int):
    side1 = config[type_]["side1Func"](params)
    side2 = config[type_]["side2Func"](params)

    total_len = len(side1["cells"]) + len(side2["cells"])
    is_win = total_len >= number_to_win - 1 and (
        side1["blockMode"] != "opposite" or side2["blockMode"] != "opposite"
    )

    return {"isWin": is_win, "arr": side1["cells"] + side2["cells"]}


def check_win(params: ParamsType, number_to_win: int) -> WinStateType:
    left_diagonal = _analytic_step(CaroWinType.LEFT_DIAGONAL, params, number_to_win)
    right_diagonal = _analytic_step(CaroWinType.RIGHT_DIAGONAL, params, number_to_win)
    vertical = _analytic_step(CaroWinType.VERTICAL, params, number_to_win)
    horizontal = _analytic_step(CaroWinType.HORIZONTAL, params, number_to_win)
    current_step = params["currentStep"]

    locations: Dict[int, Dict[str, bool]] = {}
    win_mode: List[CaroWinType] = []

    def mark_locations(result, win_type: CaroWinType):
        nonlocal locations
        win_mode.append(win_type)
        for loc in result["arr"] + [current_step]:
            if loc not in locations:
                locations[loc] = {}
            locations[loc][win_type.value] = True

    if left_diagonal["isWin"]:
        mark_locations(left_diagonal, CaroWinType.LEFT_DIAGONAL)
    if right_diagonal["isWin"]:
        mark_locations(right_diagonal, CaroWinType.RIGHT_DIAGONAL)
    if vertical["isWin"]:
        mark_locations(vertical, CaroWinType.VERTICAL)
    if horizontal["isWin"]:
        mark_locations(horizontal, CaroWinType.HORIZONTAL)

    return {"locations": locations, "winMode": win_mode}
