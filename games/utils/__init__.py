from typing import Dict, Literal
import numpy as np

def board_to_tensor(number_of_rows: int, number_of_columns: int, steps: Dict[int, Literal[1, 2]], current_player: int) -> np.ndarray:
    tensor = np.zeros((2, number_of_rows, number_of_columns), dtype=np.float32)

    for pos, player in steps.items():
      row, col = divmod(pos, number_of_columns)
      tensor[player - 1, row, col] = 1.0

    # Optionally add a plane for current player (helps NN know whose turn it is)
    player_plane = np.full((1, number_of_rows, number_of_columns), 1.0 if current_player == 1 else -1.0)
    return np.concatenate([tensor, player_plane], axis=0)