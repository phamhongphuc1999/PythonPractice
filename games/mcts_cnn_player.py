import copy
from typing import List, Literal, Optional
from caro_predictor import CaroPredictor
from game_board import GameBoard
from mcts_player import MCTSPlayer
from mcts_node import MCTSNode
from utils.type import MemoryType
import numpy as np

class MctsCnnPlayer(CaroPredictor, MCTSPlayer):
  def __init__(self, size: Literal[10, 20], trained_model_path: str, num_simulations: int = 100, c_param: float = 1.4):
    super().__init__(size, trained_model_path, num_simulations=num_simulations, c_param=c_param)
    self.memory: List[MemoryType] = []

  def run(self, root_state: GameBoard) -> Optional[int]:
    root = MCTSNode(state=copy.deepcopy(root_state))
    for _ in range(self.num_simulations):
      node = root

      # 1. Selection
      while node.children:
        node = node.best_ai_child(self.c_param)

      # 2. Evaluation (use NN)
      policy, value, _, _ = self.evaluate(node.state)

      # 3. Expansion (add NN policy to children)
      if not node.state.is_terminal():
        node.ai_expand(policy)

      # 4. Backpropagation
      self.backpropagate(node, value)
    
    # Build policy vector (normalized visit counts)
    total_visits = sum(child.visits for child in root.children)
    policy = np.zeros(root_state.number_of_rows * root_state.number_of_columns)
    for child in root.children:
      policy[child.action] = child.visits / total_visits

    self.memory.append({
      "steps": copy.deepcopy(root_state.steps),
      "policy": policy,
      "player": root_state.current_player
    })

    if not root.children:
      return None
    
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.action
  
  # def backpropagate(self, node: Optional[MCTSNode], result: float) -> None:
  #   while node is not None:
  #     node.visits += 1
  #     node.wins += result
  #     node = node.parent

  # def record_game_result(self, result: float):
  #   """Call this at the end of the game"""
  #   for entry in self.memory:
  #     # value = +1 if same as winner, -1 if loser
  #     entry["value"] = result if entry["player"] == 1 else -result
