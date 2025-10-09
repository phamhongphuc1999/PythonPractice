import random
from MCTSNode import MCTSNode


def mcts_search(root_state, iterations=500):
    root = MCTSNode(root_state)

    for _ in range(iterations):
        node = root

        # Selection
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()

        # Expansion
        if not node.is_terminal():
            node = node.expand()

        # Simulation
        result = node.rollout()

        # Backpropagation
        node.backpropagate(result)

    return root.best_child(c=0).action  # Return best move


def main():
    board = [[0]*3 for _ in range(3)]
    current_player = 1

    print("MCTS Tic-Tac-Toe Demo")
    print("0 = empty, 1 = X, 2 = O\n")

    for _ in range(9):
        for row in board: print(row)
        print()

        if current_player == 1:
            move = mcts_search(board, iterations=500)
            print(f"MCTS plays: {move}")
        else:
            empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 0]
            move = random.choice(empty)
            print(f"Random plays: {move}")

        board[move[0]][move[1]] = current_player

        if MCTSNode(board).check_winner():
            for row in board: print(row)
            print(f"Player {current_player} wins!")
            return

        current_player = 1 if current_player == 2 else 2

    print("Draw!")

if __name__ == "__main__":
    main()