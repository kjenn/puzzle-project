from abc import ABC
from typing import Final, Tuple

NUMBER_OF_GRID_SIDES: Final = 4


class AbstractGridPuzzle(ABC):

    def __init__(self, puzzle: Tuple[Tuple, ...]):
        if puzzle is None or len(puzzle) == 0:
            raise ValueError("Puzzle must have at least one row.")
        row_iterator = iter(puzzle)
        first_row = next(row_iterator)
        if first_row is None:
            raise ValueError("Puzzle must have at least one column.")
        row_len = len(first_row)
        if row_len == 0:
            raise ValueError("Puzzle must have at least one column.")
        if any(len(row) != row_len for row in row_iterator):
            raise ValueError("All rows must have the same length.")

        self.num_of_rows: Final = len(puzzle)
        self.num_of_cols: Final = row_len
        self.puzzle: Final = puzzle

