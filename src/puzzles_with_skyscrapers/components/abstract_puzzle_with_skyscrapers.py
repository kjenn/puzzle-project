import copy
import os
from abc import abstractmethod, ABC
from typing import List, Optional, Tuple, Final

from src.components.abstract_grid_puzzle import NUMBER_OF_GRID_SIDES
from src.components.abstract_square_grid_puzzle import AbstractSquareGridPuzzle
import src.components.utils as utils
from src.puzzles_with_skyscrapers.components.cell_with_skyscraper import CellWithSkyscraper
from src.components.unsolvable_error import UnsolvableError


class AbstractPuzzleWithSkyscrapers(AbstractSquareGridPuzzle, ABC):
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
        self.is_solved = False
        self.solution = None
        self.hints: Final = hints
        if len(self.hints) != self.num_of_rows * NUMBER_OF_GRID_SIDES:
            raise ValueError("A wrong number of hints was given")
        if any(x is not None and (x < 1 or x > self.num_of_rows - self._get_num_of_empty_cells()) for x in self.hints):
            raise ValueError(
                f"The hints in the puzzle must be between 1 and {self.num_of_rows - self._get_num_of_empty_cells()}")
        if self._get_num_of_empty_cells() == 0:
            self.puzzle_to_draw_on = [
                [CellWithSkyscraper(self._get_highest_possible_value(), self.puzzle[i][j],
                                    (True if i == 0 else None,
                                     True if j == self.num_of_rows - 1 else None,
                                     True if i == self.num_of_rows - 1 else None,
                                     True if j == 0 else None))
                 for j in range(self.num_of_rows)]
                for i in range(self.num_of_rows)]
        else:
            self.puzzle_to_draw_on = [
                [CellWithSkyscraper(self._get_highest_possible_value(), self.puzzle[i][j],
                                    (None, None, None, None), can_be_empty=True)
                 for j in range(self.num_of_rows)]
                for i in range(self.num_of_rows)]

    def solve(self) -> Optional[List[List[int]] or Tuple[List[List[Optional[int]]], List[List[Optional[int]]]]]:
        if self.is_solved:
            return self.solution
        self.solution = self._solve()
        self.is_solved = True
        return self.solution

    def solve_and_print(self):
        sol = self.solve()
        if sol is None:
            print("The puzzle has no solution.")
        elif isinstance(sol, tuple):
            print("The puzzle has multiple solutions.")
            for option in sol:
                print(self.__class__(option, self.hints).get_puzzle_state_drawing())
                print("************************")
        else:
            print("The puzzle has a single solution!")
            print(self.get_puzzle_state_drawing())
        return sol

    def get_puzzle_state_drawing(self) -> str:
        puzzle_state_drawing = self._get_hints_row_drawing(0) + os.linesep
        for i in range(self.num_of_rows):
            puzzle_state_drawing += utils.str_or_x_for_none(self.hints[self.num_of_rows * 3 + i]) \
                                    + self.SPACES_BETWEEN_HINT_AND_GRID
            puzzle_state_drawing += " ".join([utils.str_or_x_for_none(cell.get_value())
                                              for cell in self.puzzle_to_draw_on[i]])
            puzzle_state_drawing += self.SPACES_BETWEEN_HINT_AND_GRID \
                                    + utils.str_or_x_for_none(self.hints[self.num_of_rows + i]) \
                                    + os.linesep
        puzzle_state_drawing += self._get_hints_row_drawing(2)
        return puzzle_state_drawing

    def is_single_solution(self):
        sol = self.solve()
        return sol is not None and isinstance(sol, list)

    def get_minimal_hints_puzzle(self):
        # TODO add more tests? (with some cells filled, other types of puzzles besides regular skyscrapers)
        if not self.is_single_solution():
            print("Puzzle is not solvable.")
            return None
        minimal = self._get_minimal_hints_puzzle(self.hints)
        if minimal.hints == self.hints:
            print("The puzzle is already minimal!")
        else:
            print("Found a smaller puzzle:")
            print(minimal.get_puzzle_state_drawing())
        return minimal

    def _solve(self):
        try:
            self._validate()
            self._try_solving_basic()
            if self._is_complete():
                return self._get_puzzle_with_filled_values()
            copy_with_necessary_values = copy.deepcopy(self)
            solved_first = self._guess_values(True)
        except UnsolvableError as e:
            print(e)
            return None
        second_copy = copy.deepcopy(copy_with_necessary_values)
        solved_second = second_copy._guess_values(False)  # should not throw exception at this point
        if ((not solved_first) and solved_second) or (solved_first and (not solved_second)):
            raise Exception("This is not supposed to happen.")
        if not solved_first:
            return self._return_multiple_solutions(second_copy)
        if self.puzzle_to_draw_on != second_copy.puzzle_to_draw_on:
            return self._return_multiple_solutions(second_copy)
        another_solution = self._try_finding_another_solution(copy_with_necessary_values)
        if another_solution is not None:
            return self._return_multiple_solutions(another_solution)
        return self._get_puzzle_with_filled_values()

    def _get_minimal_hints_puzzle(self, original_hints):
        for i in range(len(self.hints)):
            if self.hints[i] is not None:
                less_hints = tuple(self.hints[j] if j != i else None for j in range(len(self.hints)))
                smaller_puzzle = self.__class__(self.puzzle, less_hints)
                if smaller_puzzle.is_single_solution():
                    return smaller_puzzle._get_minimal_hints_puzzle(original_hints)
        return self

    def _get_hints_row_drawing(self, hints_row_index: int) -> str:
        hints_in_row = [utils.str_or_x_for_none(self.hints[i + self.num_of_rows * hints_row_index])
                        for i in range(self.num_of_rows)]
        return os.linesep + " " + self.SPACES_BETWEEN_HINT_AND_GRID + " ".join(hints_in_row) + os.linesep

    def _validate(self):
        if (not self._are_values_unique()) or (not self._are_puzzle_specifics_valid()):
            raise UnsolvableError("Puzzle is not solvable.")

    def _try_finding_another_solution(self, copy_with_necessary_values: "AbstractPuzzleWithSkyscrapers") \
            -> Optional["AbstractPuzzleWithSkyscrapers"]:
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
                        print("Did not find a complete second solution.")
                    return another_copy

    def _guess_values(self, from_low: bool = True) -> bool:
        prev_grid = None
        while prev_grid != self.puzzle_to_draw_on and not self._is_complete():
            prev_grid = copy.deepcopy(self.puzzle_to_draw_on)
            for i in range(self.num_of_rows):
                for j in range(self.num_of_rows):
                    if self.puzzle_to_draw_on[i][j].get_value() is None:
                        self._guess_cell_value(i, j, from_low)
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

    def _try_solving_basic(self):
        prev_num_of_cells_with_values = -1
        while self._count_filled_cells() > prev_num_of_cells_with_values:
            prev_num_of_cells_with_values = self._count_filled_cells()
            self._mark_basic_conclusions()
            for i in range(self.num_of_rows):
                for j in range(self.num_of_rows):
                    self._mark_illegal_clashing_values(i, j)
            if self._must_all_values_appear():
                self._fill_only_possible_locations()
            self._mark_nontrivial_seen_and_unseen()
            self._mark_illegals_for_seen_status()
            self._mark_puzzle_specific_rules()
            if not self._can_cells_be_filled():
                raise UnsolvableError("There aren't enough values to fill the grid.")
            if not self._are_values_unique():
                raise UnsolvableError("There is a value repeated in a row or column.")

    def _mark_illegal_clashing_values(self, row: int, col: int):
        cell_value = self.puzzle_to_draw_on[row][col].get_value()

        if cell_value is None:
            return
        if cell_value > 0:
            self._mark_illegal_clashing_values_for_cell_with_value(col, row, cell_value)
        elif cell_value == 0:
            self._mark_illegal_clashing_values_for_empty_cell(col, row, cell_value)
        else:
            raise ValueError("A cell cannot have a negative value.")

    def _fill_only_possible_locations(self):
        prev_num_of_filled_cells = -1
        while self._count_filled_cells() > prev_num_of_filled_cells:
            prev_num_of_filled_cells = self._count_filled_cells()
            for i in range(self._get_lowest_possible_value(), self._get_highest_possible_value() + 1):
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
        cell_next_to_hint = self._get_cell_with_distance_from_hint(hint_index, 0)
        if 0 not in cell_next_to_hint.get_possible_values():
            cell_next_to_hint.set_seen_from_side(self._get_hint_side(hint_index), True)
        for i in range(1, self.num_of_rows):
            if self._is_cell_blocked(hint_index, i):
                self._get_cell_with_distance_from_hint(hint_index, i).set_seen_from_side(
                    self._get_hint_side(hint_index), False)
            if self._is_cell_exposed(hint_index, i):
                self._get_cell_with_distance_from_hint(hint_index, i).set_seen_from_side(
                    self._get_hint_side(hint_index), True)

    def _can_cells_be_filled(self) -> bool:
        for row in self.puzzle_to_draw_on:
            possible_values = set(possible_value
                                  for cell in row
                                  for possible_value in cell.get_possible_values())
            if len(possible_values) < self.num_of_rows - max(0, self._get_num_of_empty_cells() - 1):
                return False

        for i in range(self.num_of_rows):
            possible_values = set(possible_value
                                  for row in self.puzzle_to_draw_on
                                  for possible_value in row[i].get_possible_values())
            if len(possible_values) < self.num_of_rows - max(0, self._get_num_of_empty_cells() - 1):
                return False

        return True

    def _mark_illegal_clashing_values_for_cell_with_value(self, col: int, row: int, cell_value: int):
        for j in range(self.num_of_rows):
            if j != col:
                self.puzzle_to_draw_on[row][j].add_illegal_value(cell_value)
        for i in range(self.num_of_rows):
            if i != row:
                self.puzzle_to_draw_on[i][col].add_illegal_value(cell_value)

    def _mark_illegal_clashing_values_for_empty_cell(self, col: int, row: int, cell_value: int):
        zeroes_in_row = [j for j in range(self.num_of_rows)
                         if self.puzzle_to_draw_on[row][j].get_value() == 0]
        if len(zeroes_in_row) > self._get_num_of_empty_cells():
            raise UnsolvableError("Too many empty cells in the same row.")
        if len(zeroes_in_row) == self._get_num_of_empty_cells():
            for j in range(self.num_of_rows):
                if j not in zeroes_in_row:
                    self.puzzle_to_draw_on[row][j].add_illegal_value(cell_value)

        zeroes_in_col = [i for i in range(self.num_of_rows)
                         if self.puzzle_to_draw_on[i][col].get_value() == 0]
        if len(zeroes_in_col) > self._get_num_of_empty_cells():
            raise UnsolvableError("Too many empty cells in the same column.")
        if len(zeroes_in_col) == self._get_num_of_empty_cells():
            for i in range(self.num_of_rows):
                if i not in zeroes_in_col:
                    self.puzzle_to_draw_on[i][col].add_illegal_value(cell_value)

    def _mark_according_to_possible_locations(self, val, possible_locations):
        if val < 0:
            raise ValueError("A cell's value cannot be negative.")
        elif val > 0:
            if len(possible_locations) == 0:
                raise UnsolvableError("There is no cell for one of the values.")
            if len(possible_locations) == 1:
                possible_locations.pop().set_value(val)
        else:
            if len(possible_locations) < self._get_num_of_empty_cells():
                raise UnsolvableError("There aren't enough cells to leave empty.")
            if len(possible_locations) == self._get_num_of_empty_cells():
                while len(possible_locations) > 0:
                    possible_locations.pop().set_value(val)

    def _get_puzzle_with_filled_values(self) -> List[List[Optional[int]]]:
        return [[cell.get_value() for cell in row] for row in self.puzzle_to_draw_on]

    def _are_values_unique(self) -> bool:
        for row in self.puzzle_to_draw_on:
            values = [x.get_value() for x in row]
            if not self._are_single_row_or_column_values_unique(values):
                return False
        for i in range(self.num_of_rows):
            values = [row[i].get_value() for row in self.puzzle_to_draw_on]
            if not self._are_single_row_or_column_values_unique(values):
                return False
        return True

    def _are_single_row_or_column_values_unique(self, values: List[Optional[int]]):
        values_without_nones_and_zeroes = [v for v in values if v]
        if len(set(values_without_nones_and_zeroes)) != len(values_without_nones_and_zeroes):
            return False
        num_of_zeroes = values.count(0)
        if num_of_zeroes > self._get_num_of_empty_cells():
            return False
        return True

    def _is_complete(self) -> bool:
        return self._count_filled_cells() == self.num_of_rows ** 2

    def _count_filled_cells(self) -> int:
        return len(
            set((i, j) for i in range(self.num_of_rows) for j in range(self.num_of_rows) if
                self.puzzle_to_draw_on[i][j].get_value() is not None))

    def _get_cell_with_distance_from_hint(self, hint_index: int, distance: int) -> CellWithSkyscraper:
        self._validate_hint_index(hint_index)
        if not 0 <= distance < self.num_of_rows:
            raise ValueError("Wrong distance.")
        is_col_hint = self._get_hint_side(hint_index) % 2 == 0
        is_backwards = self._get_hint_side(hint_index) in {1, 2}
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

    def _get_lowest_possible_value(self) -> int:
        return 0 if self._get_num_of_empty_cells() > 0 else 1

    def _get_hint_side(self, hint_index: int) -> int:
        return int(hint_index / self.num_of_rows)

    def _validate_hint_index(self, hint_index: int):
        number_of_hints = NUMBER_OF_GRID_SIDES * self.num_of_rows
        if not 0 <= hint_index < number_of_hints:
            raise ValueError(f"There are only {number_of_hints} possible hints.")

    def _return_multiple_solutions(self, second_copy: "AbstractPuzzleWithSkyscrapers"):
        return self._get_puzzle_with_filled_values(), second_copy._get_puzzle_with_filled_values()

    @abstractmethod
    def _are_puzzle_specifics_valid(self) -> bool:
        raise NotImplementedError("_are_puzzle_specifics_valid not implemented.")

    @abstractmethod
    def _mark_basic_conclusions(self):
        raise NotImplementedError("_mark_basic_conclusions not implemented.")

    @abstractmethod
    def _mark_puzzle_specific_seen_and_unseen(self, hint_index: int):
        raise NotImplementedError("_mark_puzzle_specific_seen_and_unseen not implemented.")

    @abstractmethod
    def _mark_cell_illegals_for_seen_status(self, hint_index: int, distance_from_hint: int):
        raise NotImplementedError("_mark_cell_illegals_for_seen_status not implemented.")

    @abstractmethod
    def _mark_puzzle_specific_rules(self):
        raise NotImplementedError("_mark_puzzle_specific_rules not implemented.")

    def _get_num_of_empty_cells(self) -> int:
        return 0

    def _get_highest_possible_value(self) -> int:
        return self.num_of_rows

    def _must_all_values_appear(self) -> bool:
        return True

    # TODO document, readme, copyrights, etc.
    # TODO draw more nicely
    # TODO add equals?!
