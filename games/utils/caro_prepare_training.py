from typing import Dict, List, Literal
from game_board import GameBoard
import numpy as np

from mcts_player import MCTSPlayer, MemoryType

class CaroPrepareTraining:
  @staticmethod
  def board_to_tensor(number_of_rows: int, number_of_columns: int, steps: Dict[int, Literal[1, 2]], current_player: int) -> np.ndarray:
    tensor = np.zeros((2, number_of_rows, number_of_columns), dtype=np.float32)

    for pos, player in steps.items():
      row, col = divmod(pos, number_of_columns)
      tensor[player - 1, row, col] = 1.0

    # Optionally add a plane for current player (helps NN know whose turn it is)
    player_plane = np.full((1, number_of_rows, number_of_columns), 1.0 if current_player == 1 else -1.0)
    return np.concatenate([tensor, player_plane], axis=0)

  @staticmethod
  def self_play(number_of_rows: int, number_of_columns: int, number_to_win = 5, num_games=10):
    dataset: List[MemoryType] = []
    for _ in range(num_games):
      board = GameBoard(number_of_rows=number_of_rows, number_of_columns=number_of_columns, number_to_win=number_to_win)
      mcts = MCTSPlayer(num_simulations=100)
      while not board.is_terminal():
        action = mcts.run(board)
        board.move(action)
      if len(board.winMode["winMode"]) > 0:
        result = 1.0 if board.current_player == 1 else -1.0
      else:
        result = 0.0
      mcts.record_game_result(result)
      dataset.extend(mcts.memory)
    return dataset

  @staticmethod
  def prepare_training_data(number_of_rows: int, number_of_columns: int, num_games=50):
    data = CaroPrepareTraining.self_play(number_of_rows, number_of_columns, num_games=num_games)

    X = np.array([CaroPrepareTraining.board_to_tensor(number_of_rows, number_of_columns, d["steps"], d["player"]) for d in data])
    Y_policy = np.array([d["policy"] for d in data])
    Y_value = np.array([[d["value"]] for d in data])
    return X, Y_policy, Y_value, data
