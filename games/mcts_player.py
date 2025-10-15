import copy
import random
from typing import Literal
from mcts_node import MCTSNode


class MCTSPlayer:
  def __init__(self, num_simulations=10):
    self.num_simulations = num_simulations

  def run(self, number_of_rows = 3, number_of_columns = 3, number_to_win = 3):
    root = MCTSNode(number_of_rows=number_of_rows, number_of_columns=number_of_columns, number_to_win=number_to_win)

    for _ in range(self.num_simulations):
      node = root

      # 1. Selection
      while not node.state.is_terminal() and node.is_fully_expanded():
        node = node.best_child()

      # 2. Expansion
      if not node.state.is_terminal() and node.untried_moves:
        move = node.untried_moves.pop()
        new_state = node.state.next_state(move)
        child_node = MCTSNode(new_state, parent=node, move=move)
        node.children.append(child_node)
        node = child_node

      # 3. Simulation (rollout)
      result = self.simulate(node)

      # 4. Backpropagation
      self.backpropagate(node, result, node.current_player)

    # choose move with most visits
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.action
  
  def simulate(self, node: MCTSNode):
    currentNode = copy.deepcopy(node)
    while not currentNode.is_terminal():
        move = random.choice(currentNode.get_legal_moves())
        currentNode.move(move)
    # evaluate from the viewpoint of the *root player* (1 or 2)
    return currentNode.get_result(currentNode.current_player)
  
  def backpropagate(self, node: MCTSNode, result: Literal[0, 1, -1], root_player: Literal[1, 2]):
    while node is not None:
      node.visits += 1
      reward = result if node.state.current_player != root_player else -result
      node.wins += reward
      node = node.parent