import copy
import random
from typing import Optional
from mcts_node import MCTSNode
from game_board import GameBoard
from typing import Literal

class MCTSPlayer:
  def __init__(self, num_simulations: int = 1000, c_param: float = 1.4) -> None:
    self.num_simulations = num_simulations
    self.c_param = c_param

  def run(self, root_state: GameBoard) -> Optional[int]:
    root = MCTSNode(state=copy.deepcopy(root_state))

    for _ in range(self.num_simulations):
      node = root

      # 1) Selection
      while not node.state.is_terminal() and node.is_fully_expanded():
        node = node.best_child(self.c_param)

      # 2) Expansion
      if not node.state.is_terminal() and node.untried_moves:
        node = node.expand()

      # 3) Simulation
      result = self.simulate(node, root_state.current_player)

      # 4) Backpropagation
      self.backpropagate(node, result)

    # Choose the move with most visits
    if not root.children:
      return None
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.action

  def simulate(self, node: MCTSNode, root_player: Literal[1, 2]) -> float:
    """
    Rollout policy: random playout until terminal.
    Return +1 if root_player wins, 0 draw, -1 loss.
    """
    current = copy.deepcopy(node.state)
    while not current.is_terminal():
      legal = current.get_legal_moves()
      if not legal:
        break
      mv = random.choice(legal)
      current.move(mv)

    # Determine result
    # if winMode non-empty, GameBoard.move (as provided) keeps current_player as the player who last moved and won
    if len(current.winMode.get("winMode", [])) > 0:
      winner = current.current_player
      return 1.0 if winner == root_player else -1.0
    # draw
    return 0.0

  def backpropagate(self, node: Optional[MCTSNode], result: float) -> None:
    """
    Propagate the result up to the root.
    We measure wins from the perspective of the root player implicitly by how 'result' is defined:
    result == +1 => root_player won the simulation; internal wins counts accumulate that value.
    """
    while node is not None:
      node.visits += 1
      node.wins += result
      # invert result for parent's perspective? No need if we keep result as root_player perspective,
      # but if you want wins to be from node.state.current_player's perspective, you'd flip.
      node = node.parent
