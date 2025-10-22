from IPython.display import clear_output
from game_types import Matrix


def draw_matrix(matrix: Matrix):
  print("--------------------------------")
  for row in matrix:
    for cell in row:
      if cell == 1:
        print(f"\033[92m{cell}\033[0m", end=" ")
      elif cell == 0:
        print(f"\033[91m{cell}\033[0m", end=" ")
      else:
        print(cell, end=" ")
    print()
  print("--------------------------------")

def cls():
  clear_output(wait=True)
