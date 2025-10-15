from __future__ import annotations
import math
from typing import Dict, List, Literal
from game_board import GameBoard
import copy


class MCTSNode(GameBoard):
  children: List[MCTSNode]

  def __init__(self, number_of_rows: int, number_of_columns: int, steps: Dict[int, Literal[1, 2]] = {}, parent: MCTSNode = None, action: int = None, number_to_win = 5):
    super().__init__(number_of_rows=number_of_rows, number_of_columns=number_of_columns, number_to_win=number_to_win)
    self.steps = steps
    self.parent = parent
    self.children = []
    self.action = action
    self.visits = 0
    self.wins = 0
    self.untried_actions = self.get_legal_moves()

  def get_legal_moves(self):
    """Return list of valid positions that can still be played"""
    return [i for i in range(self.number_of_rows * self.number_of_columns)
            if self.check_move(i)]
  
  def next_state(self, move):
    """Return a *new* GameBoard after applying this move."""
    new_state = copy.deepcopy(self)
    new_state.move(move)
    return new_state
  
  def is_terminal(self):
    """Return True if the game has ended (win or full board)."""
    if len(self.winMode["winMode"]) > 0:
      return True
    if len(self.steps) == self.number_of_rows * self.number_of_columns:
      return True
    return False
  
  def get_result(self, player):
    """Return +1 if `player` won, -1 if lost, 0 for draw."""
    if len(self.winMode["winMode"]) == 0 and len(self.steps) < self.number_of_rows * self.number_of_columns:
      return None  # game not finished yet
    if len(self.winMode["winMode"]) == 0:
      return 0  # draw
    # someone won
    return 1 if self.current_player == player else -1
  
  def is_fully_expanded(self):
    return len(self.untried_moves) == 0
  
  def best_child(self, c_param=1.4):
    choices = []
    for child in self.children:
      exploitation = child.wins / (child.visits + 1e-6)
      exploration = c_param * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
      choices.append(exploitation + exploration)
    return self.children[choices.index(max(choices))]
