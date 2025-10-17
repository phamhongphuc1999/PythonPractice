import torch.nn as nn
import torch.nn.functional as F

class CaroNet(nn.Module):
  def __init__(self, board_size):
    super().__init__()
    self.conv = nn.Sequential(
      nn.Conv2d(3, 64, 3, padding=1),
      nn.ReLU(),
      nn.Conv2d(64, 64, 3, padding=1),
      nn.ReLU(),
    )
    self.policy_head = nn.Sequential(
      nn.Conv2d(64, 2, 1),
      nn.Flatten(),
      nn.Linear(2 * board_size * board_size, board_size * board_size)
    )
    self.value_head = nn.Sequential(
      nn.Conv2d(64, 1, 1),
      nn.Flatten(),
      nn.Linear(board_size * board_size, 64),
      nn.ReLU(),
      nn.Linear(64, 1),
      nn.Tanh()
    )

  def forward(self, x):
    x = self.conv(x)
    p = self.policy_head(x)
    v = self.value_head(x)
    return F.log_softmax(p, dim=1), v
