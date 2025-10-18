import random
from typing import Literal
from game_board import GameBoard
from mcts_cnn_player import MctsCnnPlayer
from mcts_player import MCTSPlayer


class CaroPlaySimulation:
  @staticmethod
  def play_random_game(number_of_rows=3, number_of_columns=3, number_to_win=3, num_simulations=300):
    board = GameBoard(number_of_rows=number_of_rows, number_of_columns=number_of_columns, number_to_win=number_to_win)
    mcts = MCTSPlayer(num_simulations=num_simulations)
    print(f"=== Caro ({board.number_of_rows}x{board.number_of_columns}) Demo: MCTS vs Random ===")
    print(board)

    while not board.is_terminal():
      if board.current_player == 1:
        # MCTS plays
        print("MCTS thinking...")
        move = mcts.run(board)
        if move is None:
          print("No move possible (draw).")
          break
      else:
        # Random plays
        move = random.choice(board.get_legal_moves())

      board.move(move)
      print(f"\nPlayer {board.current_player} made move at index {move}")

      # check if someone won
      if len(board.winMode["winMode"]) > 0:
        print(board)
        board.print_win_state()
        break
      elif len(board.steps) == board.number_of_rows * board.number_of_columns:
        print("It's a draw!")
        break

  def play_game(number_of_rows=3, number_of_columns=3, number_to_win=3, num_simulations=300, size: Literal[10, 20] = None, trained_model_path: str = None):
    board = GameBoard(number_of_rows=number_of_rows, number_of_columns=number_of_columns, number_to_win=number_to_win)
    mcts = MCTSPlayer(num_simulations=num_simulations) if size is None or trained_model_path is None else MctsCnnPlayer(size, trained_model_path, num_simulations=num_simulations)
    print(f"=== Caro ({board.number_of_rows}x{board.number_of_columns}) Demo: MCTS vs Random ===")

    while not board.is_terminal():
      if board.current_player == 1:
        move = mcts.run(board)
        if move is None:
          print("No move possible (draw).")
          break
      else:
        row = int(input(f"Player {board.current_player}, enter your move row (0-{board.number_of_rows - 1}): "))
        col = int(input(f"Player {board.current_player}, enter your move column (0-{board.number_of_columns - 1}): "))
        move = row * board.number_of_columns + col
        if move not in board.get_legal_moves():
          print("Invalid move. Try again.")
          continue
      board.move(move)
      print(board)

      if len(board.winMode["winMode"]) > 0:
        board.print_win_state()
        break
      elif len(board.steps) == board.number_of_rows * board.number_of_columns:
        print("It's a draw!")
        break

  def play_mcts_game(number_of_rows=3, number_of_columns=3, number_to_win=3, num_simulations=300):
    board = GameBoard(number_of_rows=number_of_rows, number_of_columns=number_of_columns, number_to_win=number_to_win)
    mcts1 = MCTSPlayer(num_simulations=num_simulations)
    mcts2 = MCTSPlayer(num_simulations=num_simulations)
    print(board)
    print(f"=== Caro ({board.number_of_rows}x{board.number_of_columns}) Demo: MCTS vs Random ===")

    while not board.is_terminal():
      if board.current_player == 1:
        move = mcts1.run(board)
        if move is None:
          print("No move possible (draw).")
          break
      else:
        move = mcts2.run(board)
        if move is None:
          print("No move possible (draw).")
          break
      
      board.move(move)

      if len(board.winMode["winMode"]) > 0:
        print(board)
        board.print_win_state()
        break
      elif len(board.steps) == board.number_of_rows * board.number_of_columns:
        print("It's a draw!")
        break
