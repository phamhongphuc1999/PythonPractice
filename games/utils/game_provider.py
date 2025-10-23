from connect4.connect_four import ConnectFour
from tictactoe.tictactoe import TicTacToe


def add_game_argument(parser):
    """Adding a --game argument to the argument parser with the available games

    Args:
        parser (ArgumentParser): The initialized parser
    """
    parser.add_argument(
        "-g",
        "--game",
        required=True,
        choices=["0", "1"],
        help="The type of game. 0: Connect4, 1: TicTacToe",
    )
    parser.add_argument("-s", "--size", required=False)
    parser.add_argument("-ws", "--winSize", required=False)


def get_game(args):
    """Return the game instance specified in args

    Args:
        args: parsed args from ArgumentParser)
    """
    game_type = args.game
    _size = int(args.size) if args.size is not None else 3
    _k_to_win = int(args.winSize) if args.winSize is not None else 3
    print("_size: ", _size, ", k_to_win: ", _k_to_win)
    return ConnectFour() if game_type == "0" else TicTacToe(n=_size, k_to_win=_k_to_win)
