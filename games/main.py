from tictactoe.tictactoe import TicTacToe


if __name__ == "__main__":
    caro_board = TicTacToe()
    board = caro_board.initial_state
    board, won = caro_board.move(board, 0, 0)
    print(
        "caro_board.convert_mcts_state_to_list_state(board)",
        caro_board.convert_mcts_state_to_list_state(board),
        won,
    )
    board, won = caro_board.move(board, 1, 1)
    print(
        "caro_board.convert_mcts_state_to_list_state(board)",
        caro_board.convert_mcts_state_to_list_state(board),
        won,
    )
    board, won = caro_board.move(board, 3, 0)
    print(
        "caro_board.convert_mcts_state_to_list_state(board)",
        caro_board.convert_mcts_state_to_list_state(board),
        won,
    )
    board, won = caro_board.move(board, 5, 1)
    print(
        "caro_board.convert_mcts_state_to_list_state(board)",
        caro_board.convert_mcts_state_to_list_state(board),
        won,
    )
    board, won = caro_board.move(board, 6, 0)
    print(
        "caro_board.convert_mcts_state_to_list_state(board)",
        caro_board.convert_mcts_state_to_list_state(board),
        won,
    )
