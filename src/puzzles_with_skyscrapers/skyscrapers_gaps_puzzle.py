from typing import Tuple, Optional

from src.puzzles_with_skyscrapers.components.cell_with_skyscraper import CellWithSkyscraper
from src.puzzles_with_skyscrapers.skyscrapers_puzzle import SkyscrapersPuzzle


class SkyscrapersGapsPuzzle(SkyscrapersPuzzle):

    def __init__(self, puzzle_grid: Tuple[Tuple[Optional[int], ...], ...], hints: Tuple[Optional[int], ...]):
        super().__init__(puzzle_grid, hints)
        self.puzzle_to_draw_on = [
            [CellWithSkyscraper(self._get_highest_possible_value(), self.puzzle[i][j],
                                (None, None, None, None), can_be_empty=True)
             for j in range(self.num_of_rows)]
            for i in range(self.num_of_rows)]

    def _get_highest_possible_value(self) -> bool:
        return self.num_of_rows - 1

    def _get_num_of_empty_cells(self):
        return 1
