import copy
import os
from abc import abstractmethod
from typing import List, Optional, Tuple, Final

from src.components.abstract_grid_puzzle import NUMBER_OF_GRID_SIDES
from src.components.abstract_square_grid_puzzle import AbstractSquareGridPuzzle
from src.components.utils import str_or_x_for_none
from src.puzzles_with_skyscrapers.components.cell_with_skyscraper import CellWithSkyscraper
from src.components.unsolvable_error import UnsolvableError
from src.puzzles_with_skyscrapers.components.hint_for_puzzle_with_skyscrapers import validate_hint_index, get_hint_side


class AbstractPuzzleWithSkyscrapers(AbstractSquareGridPuzzle):
    SPACES_BETWEEN_HINT_AND_GRID: Final = "   "

    def __init__(self, puzzle_grid: Tuple[Tuple[Optional[int], ...], ...], hints: Tuple[Optional[int], ...]):
        super().__init__(puzzle_grid)
        """
        the hints are given in the following order: 
        - the top hints, from left to right
        - then the right hints, from top to bottom
        - then the bottom hints, from left to right
        - then the left hints, from top to bottom
        """
        self.hints: Final = hints
        if len(self.hints) != self.num_of_rows * NUMBER_OF_GRID_SIDES:
            raise ValueError("A wrong number of hints was given")
        if any(x is not None and (x < 1 or x > self.num_of_rows) for x in self.hints):
            raise ValueError(f"The hints in the puzzle must be between 1 and {self.num_of_rows}")
        self.puzzle_to_draw_on = [
            [CellWithSkyscraper(self._get_highest_possible_value(), self.puzzle[i][j],
                                (True if i == 0 else None,
                                 True if j == self.num_of_rows - 1 else None,
                                 True if i == self.num_of_rows - 1 else None,
                                 True if j == 0 else None))
             for j in range(self.num_of_rows)]
            for i in range(self.num_of_rows)]

    def solve(self) -> Optional[List[List[int]] or Tuple[List[List[Optional[int]]], List[List[Optional[int]]]]]:
        try:
            self._validate()
            self._fill_necessarily_correct_values()
            if self._is_complete():
                print("The puzzle has a single solution!")
                return self._get_puzzle_with_filled_values()
            copy_with_necessary_values = copy.deepcopy(self)
            solved_first = self._guess_values(True)
        except UnsolvableError as e:
            print(e)
            print("The puzzle has no solution.")
            return None
        second_copy = copy.deepcopy(copy_with_necessary_values)
        solved_second = second_copy._guess_values(False)  # should not throw exception at this point
        if ((not solved_first) and solved_second) or (solved_first and (not solved_second)):
            raise Exception("This is not supposed to happen.")
        if not solved_first:
            print("The puzzle seems to have multiple solutions.")
            return self._print_and_return_multiple_solutions(second_copy)
        if self.puzzle_to_draw_on != second_copy.puzzle_to_draw_on:
            print("The puzzle has multiple solutions.")
            return self._print_and_return_multiple_solutions(second_copy)
        another_solution = self._try_finding_another_solution(copy_with_necessary_values)
        if another_solution is not None:
            print("The puzzle has multiple solutions.")
            return self._print_and_return_multiple_solutions(another_solution)
        print("The puzzle has a single solution!")
        print(self.get_puzzle_state_drawing())
        return self._get_puzzle_with_filled_values()

    def get_puzzle_state_drawing(self) -> str:
        puzzle_state_drawing = self._get_hints_row_drawing(0) + os.linesep
        for i in range(self.num_of_rows):
            puzzle_state_drawing += str_or_x_for_none(self.hints[self.num_of_rows * 3 + i]) \
                                    + self.SPACES_BETWEEN_HINT_AND_GRID
            puzzle_state_drawing += " ".join([str_or_x_for_none(cell.get_value())
                                              for cell in self.puzzle_to_draw_on[i]])
            puzzle_state_drawing += self.SPACES_BETWEEN_HINT_AND_GRID \
                                    + str_or_x_for_none(self.hints[self.num_of_rows + i]) \
                                    + os.linesep
        puzzle_state_drawing += self._get_hints_row_drawing(2)
        return puzzle_state_drawing

    def _get_hints_row_drawing(self, hints_row_index: int) -> str:
        hints_in_row = [str_or_x_for_none(self.hints[i + self.num_of_rows * hints_row_index])
                        for i in range(self.num_of_rows)]
        return os.linesep + " " + self.SPACES_BETWEEN_HINT_AND_GRID + " ".join(hints_in_row) + os.linesep

    def _validate(self):
        if (not self._are_values_unique()) or (not self._are_puzzle_specifics_valid()):
            raise UnsolvableError("Puzzle is not solvable.")

    def _fill_necessarily_correct_values(self):
        self._mark_initial_conclusions()
        self._try_solving_basic()

    def _try_solving_basic(self):
        prev_num_of_cells_with_values = -1
        num_of_cells_with_values = self._count_cells_with_value()
        while num_of_cells_with_values > prev_num_of_cells_with_values:
            for i in range(self.num_of_rows):
                for j in range(self.num_of_rows):
                    self._mark_illegal_clashing_values(i, j)
            if self._must_all_values_appear():
                self._fill_only_possible_locations()
            self._mark_nontrivial_seen_and_unseen()
            self._mark_illegals_for_seen_status()
            self._mark_puzzle_specific_rules()
            if not self._are_values_unique():
                raise UnsolvableError("There is a value repeated in a row or column.")
            prev_num_of_cells_with_values = num_of_cells_with_values
            num_of_cells_with_values = self._count_cells_with_value()

    def _guess_values(self, from_low: bool = True) -> bool:
        prev_grid = None
        while prev_grid != self.puzzle_to_draw_on and not self._is_complete():
            for i in range(self.num_of_rows):
                for j in range(self.num_of_rows):
                    if self.puzzle_to_draw_on[i][j].get_value() is None:
                        self._guess_cell_value(i, j, from_low)
            prev_grid = copy.deepcopy(self.puzzle_to_draw_on)
        return self._is_complete()

    def _guess_cell_value(self, row: int, col: int, from_low: bool):
        values_to_try = self.puzzle_to_draw_on[row][col].get_possible_values()
        while len(values_to_try) > 0:
            curr_val_to_try = min(values_to_try) if from_low else max(values_to_try)
            values_to_try.discard(curr_val_to_try)
            copy_puzzle_to_draw_on = copy.deepcopy(self)
            copy_puzzle_to_draw_on.puzzle_to_draw_on[row][col].set_value(curr_val_to_try)
            try:
                copy_puzzle_to_draw_on._try_solving_basic()
                if copy_puzzle_to_draw_on._is_complete():
                    self.puzzle_to_draw_on = copy_puzzle_to_draw_on.puzzle_to_draw_on
                    return
            except UnsolvableError:
                self.puzzle_to_draw_on[row][col].add_illegal_value(curr_val_to_try)

    def _try_finding_another_solution(
            self, copy_with_necessary_values: "AbstractPuzzleWithSkyscrapers") -> "AbstractPuzzleWithSkyscrapers":
        if type(copy_with_necessary_values) is not type(self):
            raise ValueError(f"Trying to create a puzzle of type {type(self)} from a puzzle of type "
                             f"{type(copy_with_necessary_values)}.")
        for i in range(self.num_of_rows):
            for j in range(self.num_of_rows):
                another_copy = copy.deepcopy(copy_with_necessary_values)
                if another_copy.puzzle_to_draw_on[i][j].get_value() is None:
                    another_copy.puzzle_to_draw_on[i][j].add_illegal_value(self.puzzle_to_draw_on[i][j].get_value())
                    try:
                        was_single_solution_found = another_copy._guess_values()
                    except UnsolvableError:
                        continue
                    if not was_single_solution_found:
                        raise Exception("This is not supposed to happen either.")
                    return another_copy

    def _mark_illegal_clashing_values(self, row: int, col: int):
        cell_value = self.puzzle_to_draw_on[row][col].get_value()
        if cell_value is None:
            return
        for j in range(self.num_of_rows):
            if j != col:
                self.puzzle_to_draw_on[row][j].add_illegal_value(cell_value)
        for i in range(self.num_of_rows):
            if i != row:
                self.puzzle_to_draw_on[i][col].add_illegal_value(cell_value)

    def _fill_only_possible_locations(self):
        prev_num_of_filled_cells = -1
        while self._count_cells_with_value() > prev_num_of_filled_cells:
            prev_num_of_filled_cells = self._count_cells_with_value()
            for i in range(1, self._get_highest_possible_value() + 1):
                for row in self.puzzle_to_draw_on:
                    possible_in_row = [cell for cell in row if i in cell.get_possible_values()]
                    self._mark_according_to_possible_locations(i, possible_in_row)
                for col_index in range(self.num_of_rows):
                    possible_in_col = [self.puzzle_to_draw_on[row_index][col_index]
                                       for row_index in range(self.num_of_rows)
                                       if i in self.puzzle_to_draw_on[row_index][col_index].get_possible_values()]
                    self._mark_according_to_possible_locations(i, possible_in_col)

    def _mark_nontrivial_seen_and_unseen(self):
        for hint_index in range(len(self.hints)):
            self._mark_general_seen_and_unseen(hint_index)
            self._mark_puzzle_specific_seen_and_unseen(hint_index)

    def _mark_illegals_for_seen_status(self):
        for hint_index in range(len(self.hints)):
            if self.hints[hint_index] is not None:
                for i in range(self.num_of_rows):
                    self._mark_cell_illegals_for_seen_status(hint_index, i)

    def _mark_general_seen_and_unseen(self, hint_index: int):
        for i in range(1, self.num_of_rows):
            if self._is_cell_blocked(hint_index, i):
                self._get_cell_with_distance_from_hint(hint_index, i).set_seen_from_direction(
                    get_hint_side(hint_index, self.num_of_rows), False)
            if self._is_cell_exposed(hint_index, i):
                self._get_cell_with_distance_from_hint(hint_index, i).set_seen_from_direction(
                    get_hint_side(hint_index, self.num_of_rows), True)

    @staticmethod
    def _mark_according_to_possible_locations(val, possible_locations):
        if len(possible_locations) == 0:
            raise UnsolvableError("There is no cell for one of the values.")
        if len(possible_locations) == 1:
            possible_locations.pop().set_value(val)

    def _get_puzzle_with_filled_values(self) -> List[List[Optional[int]]]:
        return [[cell.get_value() for cell in row] for row in self.puzzle_to_draw_on]

    def _are_values_unique(self) -> bool:
        for row in self.puzzle_to_draw_on:
            row_without_nones = [x.get_value() for x in row if x.get_value() is not None]
            if len(set(row_without_nones)) != len(row_without_nones):
                return False
        for i in range(self.num_of_rows):
            col_without_nones = [row[i].get_value() for row in self.puzzle_to_draw_on if row[i].get_value() is not None]
            if len(set(col_without_nones)) != len(col_without_nones):
                return False
        return True

    def _is_complete(self) -> bool:
        return self._count_cells_with_value() == self.num_of_rows ** 2

    def _count_cells_with_value(self) -> int:
        return len(
            set((i, j) for i in range(self.num_of_rows) for j in range(self.num_of_rows) if
                self.puzzle_to_draw_on[i][j].get_value()))

    def _get_cell_with_distance_from_hint(self, hint_index: int, distance: int) -> CellWithSkyscraper:
        validate_hint_index(hint_index, self.num_of_rows)
        if not 0 <= distance < self.num_of_rows:
            raise ValueError("Wrong distance.")
        is_col_hint = get_hint_side(hint_index, self.num_of_rows) % 2 == 0
        is_backwards = get_hint_side(hint_index, self.num_of_rows) in {1, 2}
        row = self.num_of_rows - 1 - distance if is_backwards else distance
        col = hint_index % self.num_of_rows
        if not is_col_hint:
            row, col = col, row
        return self.puzzle_to_draw_on[row][col]

    def _is_cell_blocked(self, hint_index: int, cell_distance_from_hint: int) -> bool:
        return (max(min(self._get_cell_with_distance_from_hint(hint_index, j).get_possible_values())
                    for j in range(cell_distance_from_hint)) >=
                max(self._get_cell_with_distance_from_hint(hint_index, cell_distance_from_hint).get_possible_values()))

    def _is_cell_exposed(self, hint_index: int, cell_distance_from_hint: int) -> bool:
        return (max(max(self._get_cell_with_distance_from_hint(hint_index, j).get_possible_values())
                    for j in range(cell_distance_from_hint)) <=
                min(self._get_cell_with_distance_from_hint(hint_index, cell_distance_from_hint).get_possible_values()))

    def _print_and_return_multiple_solutions(self, second_copy: "AbstractPuzzleWithSkyscrapers"):
        print(self.get_puzzle_state_drawing())
        print("************************")
        print(second_copy.get_puzzle_state_drawing())
        return self._get_puzzle_with_filled_values(), second_copy._get_puzzle_with_filled_values()

    def _get_highest_possible_value(self) -> bool:
        return self.num_of_rows

    @abstractmethod
    def _are_puzzle_specifics_valid(self):
        pass

    @abstractmethod
    def _mark_initial_conclusions(self):
        pass

    @abstractmethod
    def _must_all_values_appear(self) -> bool:
        pass

    @abstractmethod
    def _mark_puzzle_specific_seen_and_unseen(self, hint_index: int):
        pass

    @abstractmethod
    def _mark_cell_illegals_for_seen_status(self, hint_index: int, distance_from_hint: int):
        pass

    @abstractmethod
    def _mark_puzzle_specific_rules(self):
        pass

    # TODO document, readme, copyrights, etc.
    # TODO draw more nicely
    # TODO add skyscrapers gaps, skyscrpaers building heights +1
