from abc import ABC
from typing import Tuple

from src.components.abstract_grid_puzzle import AbstractGridPuzzle


class AbstractSquareGridPuzzle(AbstractGridPuzzle, ABC):

    def __init__(self, puzzle: Tuple[Tuple, ...]):
        super().__init__(puzzle)
        if self.num_of_rows != self.num_of_cols:
            raise ValueError("The number of rows must be the same as the number of columns in the puzzle.")
