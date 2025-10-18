from typing import Dict, List, Literal
from game_board import GameBoard
import numpy as np

from utils import board_to_tensor
from mcts_cnn_player import MctsCnnPlayer
from utils.type import MemoryType
from mcts_player import MCTSPlayer

class CaroPrepareTraining:
  @staticmethod
  def self_play(number_of_rows: int, number_of_columns: int, size: Literal[10, 20] = None, trained_model_path: str = None, number_to_win = 5, num_games = 10):
    dataset: List[MemoryType] = []
    for _ in range(num_games):
      board = GameBoard(number_of_rows=number_of_rows, number_of_columns=number_of_columns, number_to_win=number_to_win)
      mcts = MCTSPlayer(num_simulations=100) if size is None or trained_model_path is None else MctsCnnPlayer(size, trained_model_path, num_simulations=100)
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
  def prepare_training_data(number_of_rows: int, number_of_columns: int, size: Literal[10, 20] = None, trained_model_path: str = None, number_to_win = 5, num_games = 10):
    data = CaroPrepareTraining.self_play(number_of_rows, number_of_columns, size, trained_model_path, number_to_win=number_to_win, num_games=num_games)

    X = np.array([board_to_tensor(number_of_rows, number_of_columns, d["steps"], d["player"]) for d in data])
    Y_policy = np.array([d["policy"] for d in data])
    Y_value = np.array([[d["value"]] for d in data])
    return X, Y_policy, Y_value, data
