from typing import Dict, Tuple, Union
from IPython.display import clear_output
from game_types import Matrix


def draw_matrix(matrix: Matrix):
    print("--------------------------------")
    for row in matrix:
        for cell in row:
            if cell == 1:
                print(f"\033[92m{cell}\033[0m", end=" ")
            elif cell == 0:
                print(f"\033[91m{cell}\033[0m", end=" ")
            else:
                print(cell, end=" ")
        print()
    print("--------------------------------")


def cls():
    clear_output(wait=True)


def update_counts(
    counts_dict: Dict, key: Union[str, Tuple[str, str]], counts: Tuple[int, int, int]
) -> None:
    """Update counts_dict with win, lose, draw from counts if key exist.
    Else initialize new entry with 0, 0, 0
    Key can be a string representing a model name, or a tuple representing
    2 dueling models

    Args:
        counts_dict (Dict): Dictionary that keep track of wins, losses, and draws
        key (Union[str, Tuple[str, str]])
        counts (Tuple[int, int, int]): Win, Losses, and Draws
    """
    v = counts_dict.get(key, (0, 0, 0))
    res = (v[0] + counts[0], v[1] + counts[1], v[2] + counts[2])
    counts_dict[key] = res
