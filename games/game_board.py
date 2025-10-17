from typing import Dict, Literal
from utils.caro_board_utils import GameStatusMode, WinStateType, check_win

class GameBoard:
  number_of_columns: int
  number_of_rows: int
  number_to_win: int
  steps: Dict[int, Literal[1, 2]]
  current_player: Literal[1, 2]
  winMode: WinStateType
  status: GameStatusMode

  def __init__(self, number_of_rows: int, number_of_columns: int, number_to_win = 5):
    self._reset(number_of_rows=number_of_rows, number_of_columns=number_of_columns, number_to_win=number_to_win)

  def _reset(self, number_of_rows: int = None, number_of_columns: int = None, number_to_win = 5):
    if number_of_rows is not None:
      self.number_of_rows = 3 if number_of_rows < 3 else number_of_rows
    if number_of_columns is not None:
      self.number_of_columns = 3 if number_of_columns < 3 else number_of_columns
    self.number_to_win = min(5, self.number_of_rows, self.number_of_columns, max(3, number_to_win))
    self.steps = {}
    self.current_player = 1
    self.winMode = {"locations": {}, "winMode": []}
    self.status = 'playing'

  def check_move(self, location: int) -> bool:
    return location not in self.steps and 0 <= location < self.number_of_rows * self.number_of_columns and self.status == 'playing'
  
  def get_legal_moves(self):
    """Return list of valid positions that can still be played"""
    return [i for i in range(self.number_of_rows * self.number_of_columns)
            if self.check_move(i)]

  def move(self, location: int) -> bool:
    if not self.check_move(location):
      raise ValueError("Invalid move")
    self.steps[location] = self.current_player
    _win_state = check_win({
      "steps": self.steps,
      "currentStep": location,
      "currentPlayer": self.current_player,
      "numberOfRows": self.number_of_rows,
      "numberOfColumns": self.number_of_columns,
    }, number_to_win=self.number_to_win)
    if len(_win_state['winMode']) > 0:
      self.winMode = _win_state
      return True
    else:
      self.current_player = 2 if self.current_player == 1 else 1
      return False
    
  def is_terminal(self) -> bool:
    if len(self.winMode['winMode']) > 0:
      return True
    if len(self.steps) == self.number_of_rows * self.number_of_columns:
      return True
    return False

  def __str__(self):
    _str = '--------------------------\n'
    for row in range(self.number_of_rows):
      for col in range(self.number_of_columns):
        index = row * self.number_of_columns + col
        if index in self.steps:
          color = "\033[31m" if self.steps[index] == 1 else "\033[32m"
          _str += f"{color}{self.steps[index]}\033[0m "
        else:
          _str += " . "
      _str += '\n'
    _str += '--------------------------\n'
    return _str

  def print_win_state(self):
    if len(self.winMode["winMode"]) > 0:
      print(f"Player {self.current_player} wins!")
      print("Winning positions:", self.winMode['locations'])
      print("Winning modes:", self.winMode['winMode'])
    else:
      print("No winner yet.")
