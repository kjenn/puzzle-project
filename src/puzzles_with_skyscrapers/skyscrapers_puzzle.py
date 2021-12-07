from src.components.unsolvable_error import UnsolvableError
from src.puzzles_with_skyscrapers.components.abstract_puzzle_with_skyscrapers import AbstractPuzzleWithSkyscrapers


class SkyscrapersPuzzle(AbstractPuzzleWithSkyscrapers):

    def _are_puzzle_specifics_valid(self) -> bool:
        return self._are_hints_across_possibly_solvable()

    def _mark_initial_conclusions(self):
        self._mark_initial_illegal_blocking_values()

    def _mark_puzzle_specific_seen_and_unseen(self, hint_index: int):
        if self.hints[hint_index] is None:
            return
        if self.hints[hint_index] + self._count_cells_with_seen_status(hint_index, False) == self.num_of_rows:
            self._set_unmarked_cells_seen_status(hint_index, True)
        if self.hints[hint_index] + self._count_cells_with_seen_status(hint_index, False) > self.num_of_rows:
            raise UnsolvableError("Too many cells hidden from hint.")
        if self.hints[hint_index] == self._count_cells_with_seen_status(hint_index, True):
            self._set_unmarked_cells_seen_status(hint_index, False)
        if self.hints[hint_index] < self._count_cells_with_seen_status(hint_index, True):
            raise UnsolvableError("Too many cells seen by hint.")

    def _mark_cell_illegals_for_seen_status(self, hint_index: int, distance_from_hint: int):
        if self._should_ensure_seen_status(hint_index, distance_from_hint, True):
            self._mark_blocked_values_illegal(hint_index, distance_from_hint)
        if distance_from_hint < self.num_of_rows - 1:
            self._mark_blocking_values_illegal(hint_index, distance_from_hint)
        if self._should_ensure_seen_status(hint_index, distance_from_hint, False):
            self._mark_unblockable_values_illegal(hint_index, distance_from_hint)

    def _mark_puzzle_specific_rules(self):
        pass

    def _are_hints_across_possibly_solvable(self) -> bool:
        hints_half_index = int(len(self.hints) / 2)
        for i in range(hints_half_index):
            first_hint = self.hints[i] if self.hints[i] is not None else 0
            hint_across = self.hints[hints_half_index + i] if self.hints[hints_half_index + i] is not None else 0
            if first_hint + hint_across > self.num_of_rows + 1 - self._get_num_of_empty_cells():
                return False
        return True

    def _mark_initial_illegal_blocking_values(self):
        # TODO test changes!!! change function name
        for i in range(len(self.hints)):
            if self.hints[i] is not None:
                cell_indices_possibly_seen_from_hint = [
                    d for d in range(self.num_of_rows)
                    if self._get_cell_with_distance_from_hint(i, d).get_seen_from_side(
                        self._get_hint_side(i)) is not False
                ]
                for first_distance_where_legal, illegal_value in \
                        zip(range(self.hints[i] - 1, -1, -1), range(self._get_highest_possible_value(), -1, -1)):
                    for j in range(cell_indices_possibly_seen_from_hint[first_distance_where_legal]):
                        self._get_cell_with_distance_from_hint(i, j).add_illegal_value(illegal_value)

    def _count_cells_with_seen_status(self, hint_index: int, seen_status: bool) -> int:
        return len(
            [self._get_cell_with_distance_from_hint(hint_index, i)
             for i in range(self.num_of_rows)
             if self._get_cell_with_distance_from_hint(hint_index, i).get_seen_from_side(
                self._get_hint_side(hint_index)) is seen_status])

    def _set_unmarked_cells_seen_status(self, hint_index: int, seen_status: bool):
        for i in range(self.num_of_rows):
            if self._get_cell_with_distance_from_hint(hint_index, i).get_seen_from_side(
                    self._get_hint_side(hint_index)) is None:
                self._get_cell_with_distance_from_hint(hint_index, i).set_seen_from_side(
                    self._get_hint_side(hint_index), seen_status)

    def _mark_blocking_values_illegal(self, hint_index: int, distance_from_hint: int):
        largest_possible_for_seen_cells = [max(
            self._get_cell_with_distance_from_hint(hint_index, j).get_possible_values())
            for j in range(distance_from_hint + 1, self.num_of_rows)
            if self._get_cell_with_distance_from_hint(hint_index, j).get_seen_from_side(
                self._get_hint_side(hint_index)) is True]
        if len(largest_possible_for_seen_cells) > 0:
            smallest_to_not_block = min(largest_possible_for_seen_cells)
            for k in range(smallest_to_not_block, self._get_highest_possible_value() + 1):
                self._get_cell_with_distance_from_hint(hint_index, distance_from_hint).add_illegal_value(k)

    def _mark_unblockable_values_illegal(self, hint_index: int, distance_from_hint: int):
        if distance_from_hint == 0:
            self._get_cell_with_distance_from_hint(hint_index, distance_from_hint).set_value(0)
        else:
            largest_possible_blocking = max([
                max(self._get_cell_with_distance_from_hint(hint_index, j).get_possible_values())
                for j in range(distance_from_hint)])
            for k in range(largest_possible_blocking, self._get_highest_possible_value() + 1):
                self._get_cell_with_distance_from_hint(hint_index, distance_from_hint).add_illegal_value(k)

    def _mark_blocked_values_illegal(self, hint_index: int, distance_from_hint: int):
        cell = self._get_cell_with_distance_from_hint(hint_index, distance_from_hint)

        if distance_from_hint == 0:
            if cell.can_be_empty:
                cell.add_illegal_value(0)
            return

        for k in range(self._get_lowest_possible_value(),
                       self._get_lower_bound_in_front_of_cell(hint_index, distance_from_hint) + 1):
            cell.add_illegal_value(k)

    def _get_lower_bound_in_front_of_cell(self, hint_index: int, cell_distance_from_hint: int) -> int:
        return max([
            min(self._get_cell_with_distance_from_hint(hint_index, j).get_possible_values())
            for j in range(cell_distance_from_hint)])

    def _should_ensure_seen_status(self, hint_index: int, distance_from_hint: int, seen_status: bool) -> bool:
        cell = self._get_cell_with_distance_from_hint(hint_index, distance_from_hint)
        return cell.get_seen_from_side(self._get_hint_side(hint_index)) is seen_status
