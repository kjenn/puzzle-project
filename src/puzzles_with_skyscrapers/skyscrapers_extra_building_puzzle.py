from src.puzzles_with_skyscrapers.skyscrapers_puzzle import SkyscrapersPuzzle


class SkyscrapersExtraBuildingPuzzle(SkyscrapersPuzzle):

    def _must_all_values_appear(self) -> bool:
        return False

    def _get_highest_possible_value(self) -> int:
        return self.num_of_rows + 1
