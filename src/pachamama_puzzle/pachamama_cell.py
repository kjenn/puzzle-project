from typing import Optional

from src.pachamama_puzzle.pachamama_shape import PachamamaShape


class PachamamaCell:

    MAX_REGION_SIZE = 5

    def __init__(self, number: Optional[int], shape: Optional[PachamamaShape]):
        if number is not None and (number <= 0 or number > self.MAX_REGION_SIZE):
            raise ValueError(f"A value in a filled cell must be between 1 and {self.MAX_REGION_SIZE}.")
        self.number = number
        self.shape = shape

    def __eq__(self, other):
        if not isinstance(other, PachamamaCell):
            return False
        return self.number == other.number and self.shape == other.shape
