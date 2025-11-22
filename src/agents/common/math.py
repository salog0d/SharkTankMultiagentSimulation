import math
from typing import Union

Number = Union[int, float]


def sigmoid(x: Number) -> float:
    x = float(x)
    return 1.0 / (1.0 + math.exp(-x))


def clamp(x: Number, lo: Number = -3.0, hi: Number = 3.0) -> float:
    x = float(x)
    return float(max(min(x, hi), lo))
