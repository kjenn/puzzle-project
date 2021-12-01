from typing import Optional, Set, Tuple

from src.components.abstract_grid_puzzle import NUMBER_OF_GRID_SIDES
from src.components.unsolvable_error import UnsolvableError


class CellWithSkyscraper:

    def __init__(
            self, highest_possible_value: int, value: Optional[int] = None,
            seen: Tuple[Optional[bool], Optional[bool], Optional[bool], Optional[bool]] = (None, None, None, None),
            can_be_empty: bool = False):
        # TODO add test if there isn't, and also with possible empty values
        self.highest_possible_value = highest_possible_value
        self.can_be_empty = can_be_empty
        self.lowest_possible_value = 0 if can_be_empty else 1
        self._seen = (None, None, None, None)
        self._set_seen(seen)
        self._value = None
        self._illegal_values = set()
        if value is not None:
            self.set_value(value)

    def get_possible_values(self) -> Set[int]:
        # TODO add test with empty cells
        if self._value is not None:
            return {self._value}
        return set(i for i in range(self.lowest_possible_value, self.highest_possible_value + 1)
                   if i not in self._illegal_values)

    def get_value(self):
        return self._value

    def set_value(self, value_to_set: int):
        # TODO add test for empty cell
        if value_to_set not in range(self.lowest_possible_value, self.highest_possible_value + 1):
            raise ValueError("Trying to set the value of a cell to an out of range number.")
        if self._value == value_to_set:
            return
        if self._value is not None:
            raise UnsolvableError("Trying to set the value of a cell that already has a different value.")
        if value_to_set in self._illegal_values:
            raise UnsolvableError("Trying to set the value of a cell to an illegal value.")
        self._value = value_to_set
        self._illegal_values = set(i for i in range(self.lowest_possible_value, self.highest_possible_value + 1)
                                   if i != self._value)
        if self._value == self.highest_possible_value:
            self._set_seen((True, True, True, True))
        if self._value == 0:
            self._set_seen((False, False, False, False))

    def add_illegal_value(self, illegal_value: int):
        # TODO add test for empty cell
        if illegal_value not in range(self.lowest_possible_value, self.highest_possible_value + 1):
            raise ValueError("Trying to set an illegal value to an out of range number.")
        if self._value == illegal_value:
            raise UnsolvableError("Trying to set an illegal value that is the same as the value.")
        self._illegal_values.add(illegal_value)
        if len(self._illegal_values) == self.highest_possible_value - self.lowest_possible_value + 1:
            raise UnsolvableError("There are no legal values left for the cell.")
        if len(self._illegal_values) == self.highest_possible_value - self.lowest_possible_value:
            self.set_value(self.get_possible_values().pop())

    def set_seen_from_side(self, hint_side: int, is_seen: bool):
        self._validate_hint_side(hint_side)
        self._set_seen(tuple(None if i != hint_side else is_seen for i in range(NUMBER_OF_GRID_SIDES)))

    def get_seen_from_side(self, hint_side: int) -> bool:
        self._validate_hint_side(hint_side)
        return self._seen[hint_side]

    def _set_seen(self, is_seen: Tuple[Optional[bool], Optional[bool], Optional[bool], Optional[bool]]):
        # TODO add test for empty cell
        if not isinstance(is_seen, tuple) or len(is_seen) != NUMBER_OF_GRID_SIDES:
            raise ValueError(f"Every cell has exactly {NUMBER_OF_GRID_SIDES} sides.")
        for i in range(len(self._seen)):
            if self._seen[i] is not None and is_seen[i] is not None and is_seen[i] != self._seen[i]:
                raise UnsolvableError("A cell's seen status cannot change.")
        new_seen = []
        for i in range(len(is_seen)):
            if is_seen[i] is not None:
                new_seen.append(is_seen[i])
            else:
                new_seen.append(self._seen[i])
        self._seen = tuple(new_seen)
        if self.can_be_empty:
            for i in range(len(self._seen)):
                if self._seen[i] is True:
                    self.add_illegal_value(0)

    @staticmethod
    def _validate_hint_side(hint_side: int):
        if not 0 <= hint_side < NUMBER_OF_GRID_SIDES:
            raise ValueError(f"There are only {NUMBER_OF_GRID_SIDES} possible hint sides.")

    def __eq__(self, other):
        if not isinstance(other, CellWithSkyscraper):
            return False
        return (self.highest_possible_value == other.highest_possible_value and self._value == other._value
                and self._seen == other._seen and self._illegal_values == other._illegal_values)
