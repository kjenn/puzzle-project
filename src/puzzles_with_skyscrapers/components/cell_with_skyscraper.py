from typing import Optional, Set, Tuple

from src.components.abstract_grid_puzzle import NUMBER_OF_GRID_SIDES
from src.components.unsolvable_error import UnsolvableError
from src.puzzles_with_skyscrapers.components.hint_for_puzzle_with_skyscrapers import get_hint_side, validate_hint_index


class CellWithSkyscraper:

    def __init__(
            self, num_of_rows: int, value: Optional[int] = None,
            seen: Tuple[Optional[bool], Optional[bool], Optional[bool], Optional[bool]] = (None, None, None, None)):
        self.highest_possible_value = num_of_rows
        self._seen = (None, None, None, None)
        self.set_seen(seen)
        self._value = None
        self._illegal_values = set()
        if value is not None:
            self.set_value(value)

    def get_possible_values(self) -> Set[int]:
        if self._value is not None:
            return {self._value}
        return set(i for i in range(1, self.highest_possible_value + 1) if i not in self._illegal_values)

    def get_value(self):
        return self._value

    def set_value(self, value_to_set: int):
        if value_to_set not in range(1, self.highest_possible_value + 1):
            raise ValueError("Trying to set the value of a cell to an out of range number.")
        if self._value == value_to_set:
            return
        if self._value is not None:
            raise UnsolvableError("Trying to set the value of a cell that already has a different value.")
        if value_to_set in self._illegal_values:
            raise UnsolvableError("Trying to set the value of a cell to an illegal value.")
        self._value = value_to_set
        self._illegal_values = set(i for i in range(1, self.highest_possible_value + 1) if i != self._value)
        if self._value == self.highest_possible_value:
            self.set_seen((True, True, True, True))

    def add_illegal_value(self, illegal_value: int):
        if illegal_value not in range(1, self.highest_possible_value + 1):
            raise ValueError("Trying to set an illegal value to an out of range number.")
        if self._value == illegal_value:
            raise UnsolvableError("Trying to set an illegal value that is the same as the value.")
        self._illegal_values.add(illegal_value)
        if len(self._illegal_values) == self.highest_possible_value:
            raise UnsolvableError("There are no legal values left for the cell.")
        if len(self._illegal_values) == self.highest_possible_value - 1:
            self.set_value(self.get_possible_values().pop())

    def set_seen(self, is_seen: Tuple[Optional[bool], Optional[bool], Optional[bool], Optional[bool]]):
        if not isinstance(is_seen, tuple) or len(is_seen) != NUMBER_OF_GRID_SIDES:
            raise ValueError(f"Every cell has exactly {NUMBER_OF_GRID_SIDES} directions.")
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

    def set_seen_from_hint(self, hint_index: int, is_seen: bool):
        validate_hint_index(hint_index, self.highest_possible_value)
        self.set_seen(tuple(None if i != get_hint_side(hint_index, self.highest_possible_value) else is_seen
                            for i in range(NUMBER_OF_GRID_SIDES)))

    def get_seen_from_hint(self, hint_index: int) -> bool:
        validate_hint_index(hint_index, self.highest_possible_value)
        return self._seen[get_hint_side(hint_index, self.highest_possible_value)]

    def __eq__(self, other):
        if not isinstance(other, CellWithSkyscraper):
            return False
        return (self.highest_possible_value == other.highest_possible_value and self._value == other._value
                and self._seen == other._seen and self._illegal_values == other._illegal_values)
