from __future__ import annotations
import math
from typing import List, Optional

from game_board import GameBoard
import copy

EPS = 1e-6

class MCTSNode:
  def __init__(self, state: GameBoard, parent: Optional["MCTSNode"] = None, action: Optional[int] = None, prior_prob: float = 1.0):
    self.state: GameBoard = state
    self.parent: Optional[MCTSNode] = parent
    self.action: Optional[int] = action
    self.children: List[MCTSNode] = []
    self.visits: int = 0
    self.wins: float = 0.0
    self.untried_moves: List[int] = list(state.get_legal_moves())
    self.prior_prob = prior_prob
  
  def is_fully_expanded(self) -> bool:
    return len(self.untried_moves) == 0
  
  def expand(self) -> "MCTSNode":
    """Pop one untried move, apply it, create child node and return it."""
    move = self.untried_moves.pop()
    new_state = copy.deepcopy(self.state)
    new_state.move(move)
    child = MCTSNode(state=new_state, parent=self, action=move)
    self.children.append(child)
    return child
  
  def ai_expand(self, masked_policy: List[float]):
    """Expand node using NN policy probabilities for legal moves."""
    for move in self.state.get_legal_moves():
      prob = masked_policy[move]
      new_state = copy.deepcopy(self.state)
      new_state.move(move)
      child = MCTSNode(state=new_state, parent=self, action=move, prior_prob=prob)
      self.children.append(child)
  
  def best_child(self, c_param: float = 1.4) -> "MCTSNode":
    """Return child with highest UCB1 score."""
    if len(self.children) == 0:
      raise ValueError("No children to select from")
    parent_visits = max(1, self.visits)
    scores = []
    for child in self.children:
      exploitation = child.wins / (child.visits + EPS)
      exploration = c_param * math.sqrt(2 * math.log(parent_visits) / (child.visits + EPS))
      scores.append(exploitation + exploration)
    best_idx = scores.index(max(scores))
    return self.children[best_idx]
  
  def best_ai_child(self, c_param: float = 1.4) -> "MCTSNode":
    total_visits = sum(child.visits for child in self.children) + EPS
    best_score = -float('inf')
    best_child = None
    for child in self.children:
      q_value = child.wins / (child.visits + EPS)
      u_value = c_param * child.prior_prob * math.sqrt(total_visits) / (1 + child.visits)
      score = q_value + u_value
      if score > best_score:
        best_score = score
        best_child = child
    return best_child
