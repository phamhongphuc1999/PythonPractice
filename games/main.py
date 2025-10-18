from caro_predictor import CaroPredictor
from game_board import GameBoard

if __name__ == '__main__':
  number_of_rows = 3
  number_of_columns = 3

  board = GameBoard(number_of_rows=number_of_rows, number_of_columns=number_of_columns, number_to_win=3)
  ai_player = CaroPredictor(10, 10, "trained/caronet_weights_1760763011.pth")

  board.move(0)
  masked_policy, value, move, percent = ai_player.evaluate(board)
  print("move: ",value, move, percent)
  for i in range(0, number_of_rows):
    for j in range(0, number_of_columns):
      print(masked_policy[i * number_of_columns + j])
    print('\n')

  print("masked_policy: ", masked_policy)
