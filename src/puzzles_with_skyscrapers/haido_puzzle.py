from src.components.unsolvable_error import UnsolvableError
from src.puzzles_with_skyscrapers.components.abstract_puzzle_with_skyscrapers import AbstractPuzzleWithSkyscrapers


class HaidoPuzzle(AbstractPuzzleWithSkyscrapers):

    def _are_puzzle_specifics_valid(self) -> bool:
        for i in range(int(len(self.hints) / 2)):
            if self.hints[i] is not None and self.hints[i] != self.num_of_rows \
                    and self.hints[i] == self.hints[int(len(self.hints) / 2) + i]:
                return False
        return True

    def _mark_basic_conclusions(self):
        for i in range(len(self.hints)):
            if self.hints[i] is not None:
                for j in range(self.hints[i], self.num_of_rows):
                    self._get_cell_with_distance_from_hint(i, j).add_illegal_value(self.hints[i])
        self._mark_puzzle_specific_rules()

    def _mark_puzzle_specific_seen_and_unseen(self, hint_index: int):
        if self.hints[hint_index] is None:
            return
        for i in range(self.num_of_rows):
            cell = self._get_cell_with_distance_from_hint(hint_index, i)
            if cell.get_value() == self.hints[hint_index]:
                cell.set_seen_from_side(self._get_hint_side(hint_index), True)

    def _mark_cell_illegals_for_seen_status(self, hint_index: int, distance_from_hint: int):
        cell = self._get_cell_with_distance_from_hint(hint_index, distance_from_hint)
        if cell.get_seen_from_side(self._get_hint_side(hint_index)) is False:
            cell.add_illegal_value(self.hints[hint_index])  # self.hints[hint_index] is not None

    def _mark_puzzle_specific_rules(self):
        for i in range(len(self.hints)):
            if self.hints[i] is not None:
                cells_where_hint_is_possible = [
                    j for j in range(self.num_of_rows)
                    if self.hints[i] in self._get_cell_with_distance_from_hint(i, j).get_possible_values()]
                if len(cells_where_hint_is_possible) == 0:
                    raise UnsolvableError("There is no possible location for a value.")
                first_cell_where_hint_is_possible = min(cells_where_hint_is_possible)
                for j in range(first_cell_where_hint_is_possible + 1):
                    for k in range(self.hints[i] + 1, self.num_of_rows + 1):
                        self._get_cell_with_distance_from_hint(i, j).add_illegal_value(k)
