from typing import Dict, Literal
from utils import GameStatusMode, WinStateType, check_win

class GameBoard:
  number_of_columns: int
  number_of_rows: int
  steps: Dict[int, Literal[1, 2]]
  current_player: Literal[1, 2]
  winMode: WinStateType
  status: GameStatusMode

  def __init__(self, number_of_rows: int, number_of_columns: int):
    self._reset(number_of_rows=number_of_rows, number_of_columns=number_of_columns)

  def _reset(self, number_of_rows: int = None, number_of_columns: int = None):
    if number_of_rows is not None:
      self.number_of_rows = number_of_rows
    if number_of_columns is not None:
      self.number_of_columns = number_of_columns
    self.steps = {}
    self.current_player = 1
    self.winMode = {"locations": {}, "winMode": []}
    self.status = 'playing'

  def move(self, location: int) -> bool:
    self.steps[location] = self.current_player
    _win_state = check_win({
      "steps": self.steps,
      "currentStep": location,
      "currentPlayer": self.current_player,
      "numberOfRows": self.number_of_rows,
      "numberOfColumns": self.number_of_columns,
    })
    print("_win_state_win_state", _win_state)
    if len(_win_state['winMode']) > 0:
      self.winMode = _win_state
      return True
    else:
      self.current_player = 2 if self.current_player == 1 else 1
      return False

  def draw_board(self):
    print('--------------------------')
    for row in range(self.number_of_rows):
      for col in range(self.number_of_columns):
        index = row * self.number_of_columns + col
        if index in self.steps:
          print(f" {self.steps[index]} ", end="")
        else:
          print(" 0 ", end="")
      print()
    print('--------------------------')

  def print_win_state(self):
    if len(self.winMode) > 0:
      print(f"Player {self.current_player} wins!")
      print("Winning positions:", self.winMode['locations'])
      print("Winning modes:", self.winMode['winMode'])
    else:
      print("No winner yet.")
