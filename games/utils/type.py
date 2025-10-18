from typing import Dict, Literal, TypedDict
import numpy as np

class MemoryType(TypedDict):
    steps: Dict[int, Literal[1, 2]]
    policy: np.ndarray[tuple[int], np.dtype[np.float64]]
    current_player: Literal[1, 2]
