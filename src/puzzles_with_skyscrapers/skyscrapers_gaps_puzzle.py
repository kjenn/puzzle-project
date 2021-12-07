from src.puzzles_with_skyscrapers.skyscrapers_puzzle import SkyscrapersPuzzle


class SkyscrapersGapsPuzzle(SkyscrapersPuzzle):

    def _get_highest_possible_value(self) -> int:
        return self.num_of_rows - 1

    def _get_num_of_empty_cells(self) -> int:
        return 1

