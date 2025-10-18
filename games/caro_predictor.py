import numpy as np
import torch
from caro_net import CaroNet
from game_board import GameBoard
from utils.caro_prepare_training import CaroPrepareTraining

class CaroPredictor:
  def __init__(self, number_of_rows: int, number_of_columns: int, trained_model_path: str):
    self.number_of_rows = number_of_rows
    self.number_of_columns = number_of_columns
    self.model = CaroNet(number_of_rows, number_of_columns)
    self.model.load_state_dict(torch.load(trained_model_path))
    self.model.eval()

  def evaluate(self, board: GameBoard):
    board_tensor = CaroPrepareTraining.board_to_tensor(self.number_of_rows, self.number_of_columns, board.steps, board.current_player)
    x = torch.tensor(board_tensor, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
      predicted_policy, predicted_value = self.model(x)
      policy = torch.exp(predicted_policy).squeeze(0).numpy()
      value = predicted_value.item()

      legal_moves = board.get_legal_moves()
      masked_policy = np.zeros(board.number_of_rows * board.number_of_columns)
      max_percent = 0
      max_move = -1
      for move in legal_moves:
        row, col = divmod(move, board.number_of_columns)
        standard_move = row * self.number_of_columns + col
        masked_policy[move] = policy[standard_move]
        if policy[standard_move] > max_percent:
          max_percent = policy[standard_move]
          max_move = move

      if masked_policy.sum() > 0:
        masked_policy /= masked_policy.sum()
      else:
        masked_policy = np.ones_like(masked_policy) / len(policy)

      return masked_policy, value, max_move, masked_policy[max_move]
