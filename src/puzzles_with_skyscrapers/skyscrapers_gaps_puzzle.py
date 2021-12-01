from typing import Tuple, Optional

from src.puzzles_with_skyscrapers.components.cell_with_skyscraper import CellWithSkyscraper
from src.puzzles_with_skyscrapers.skyscrapers_puzzle import SkyscrapersPuzzle


class SkyscrapersGapsPuzzle(SkyscrapersPuzzle):

    def _get_highest_possible_value(self) -> int:
        return self.num_of_rows - 1

    def _get_num_of_empty_cells(self) -> int:
        return 1

    # TODO add tests, and also tests for things changed to accommodate 0! Se changes in gituhb
