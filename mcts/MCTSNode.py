import math
import random


class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state                    # Current board
        self.parent = parent                  # Parent node
        self.action = action                  # Move leading to this node
        self.children = []                    # List of children
        self.visits = 0                       # Visit count
        self.wins = 0                         # Win count
        self.untried_actions = self.get_actions()  # Available moves

    def get_actions(self):
        """Return all empty cells."""
        return [(i, j) for i in range(3) for j in range(3) if self.state[i][j] == 0]

    def is_terminal(self):
        """Check if the game has ended."""
        return self.check_winner() is not None or not self.get_actions()

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def check_winner(self):
        """Find winner (1 or 2) or None."""
        for i in range(3):
            if self.state[i][0] == self.state[i][1] == self.state[i][2] != 0:
                return self.state[i][0]
            if self.state[0][i] == self.state[1][i] == self.state[2][i] != 0:
                return self.state[0][i]
        if self.state[0][0] == self.state[1][1] == self.state[2][2] != 0:
            return self.state[0][0]
        if self.state[0][2] == self.state[1][1] == self.state[2][0] != 0:
            return self.state[0][2]
        return None
    
    def expand(self):
        """Add one of the remaining actions as a child."""
        action = self.untried_actions.pop()
        new_state = [row[:] for row in self.state]
        player = self.get_current_player()
        new_state[action[0]][action[1]] = player
        child = MCTSNode(new_state, parent=self, action=action)
        self.children.append(child)
        return child

    def get_current_player(self):
        """Find whose turn it is."""
        x_count = sum(row.count(1) for row in self.state)
        o_count = sum(row.count(2) for row in self.state)
        return 1 if x_count == o_count else 2

    def best_child(self, c=1.4):
        """Select child with best UCB1 score."""
        return max(self.children, key=lambda child:
                   (child.wins / child.visits) +
                   c * math.sqrt(math.log(self.visits) / child.visits))

    def rollout(self):
        """Play random moves until the game ends."""
        state = [row[:] for row in self.state]
        player = self.get_current_player()

        while True:
            winner = self.check_winner_for_state(state)
            if winner: return 1 if winner == 1 else 0

            actions = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0]
            if not actions: return 0.5  # Draw

            move = random.choice(actions)
            state[move[0]][move[1]] = player
            player = 1 if player == 2 else 2

    def check_winner_for_state(self, state):
        """Same winner check for rollout."""
        return MCTSNode(state).check_winner()

    def backpropagate(self, result):
        """Update stats up the tree."""
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)
