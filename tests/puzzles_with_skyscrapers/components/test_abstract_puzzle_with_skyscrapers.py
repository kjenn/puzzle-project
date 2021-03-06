import io
import os
import unittest
from typing import Tuple, Optional
from unittest.mock import patch

from src.components.unsolvable_error import UnsolvableError
from src.puzzles_with_skyscrapers.components.abstract_puzzle_with_skyscrapers import AbstractPuzzleWithSkyscrapers


def mock_num_of_empty_cells(puzzle):
    return 2


def mock_highest_possible_value(puzzle):
    return puzzle.num_of_rows - 2


@patch.object(AbstractPuzzleWithSkyscrapers, '__abstractmethods__', set())
class TestAbstractPuzzleWithSkyscrapers(unittest.TestCase):

    def test_ctor(self):
        self._test_ctor_wrong_num_of_hints()
        self._test_ctor_illegal_hints()
        self._test_ctor_illegal_hints_with_empty_cells()
        self._test_ctor_legit()
        self._test_ctor_legit_with_empty_cells()

    def test_mark_illegal_clashing_values(self):
        self._test_mark_illegal_clashing_values_no_empty_cells()
        self._test_mark_illegal_clashing_values_with_empty_cells()

    def test_fill_only_possible_locations(self):
        self._test_fill_only_possible_location_no_empty_cells()
        self._test_fill_only_possible_location_with_empty_cells()

    def test_mark_general_seen_and_unseen_no_empty_cells(self):
        self._test_unseen(hint_index=2, unseen_row=4, unseen_col=2, blocking_row=1, blocking_col=2,
                          unseen_cell_tuple=(False, None, None, None))
        self._test_unseen(hint_index=8, unseen_row=2, unseen_col=1, blocking_row=2, blocking_col=4,
                          unseen_cell_tuple=(None, False, None, None))
        self._test_unseen(hint_index=14, unseen_row=1, unseen_col=2, blocking_row=4, blocking_col=2,
                          unseen_cell_tuple=(None, None, False, None))
        self._test_unseen(hint_index=20, unseen_row=2, unseen_col=4, blocking_row=2, blocking_col=1,
                          unseen_cell_tuple=(None, None, None, False))

        self._test_non_blocked(hint_index=2, non_blocked_row=4, non_blocked_col=2, non_blocking_row=1,
                               non_blocking_col=2)
        self._test_non_blocked(hint_index=8, non_blocked_row=2, non_blocked_col=1, non_blocking_row=2,
                               non_blocking_col=4)
        self._test_non_blocked(hint_index=14, non_blocked_row=1, non_blocked_col=2, non_blocking_row=4,
                               non_blocking_col=2)
        self._test_non_blocked(hint_index=20, non_blocked_row=2, non_blocked_col=4, non_blocking_row=2,
                               non_blocking_col=1)

        self._test_seen(hint_index=2, first_low_row=0, first_low_col=2, second_low_row=1, second_low_col=2,
                        seen_row=2, seen_col=2, seen_cell_tuple=(True, None, None, None))
        self._test_seen(hint_index=8, first_low_row=2, first_low_col=5, second_low_row=2, second_low_col=4,
                        seen_row=2, seen_col=3, seen_cell_tuple=(None, True, None, None))
        self._test_seen(hint_index=14, first_low_row=5, first_low_col=2, second_low_row=4, second_low_col=2,
                        seen_row=3, seen_col=2, seen_cell_tuple=(None, None, True, None))
        self._test_seen(hint_index=20, first_low_row=2, first_low_col=0, second_low_row=2, second_low_col=1,
                        seen_row=2, seen_col=2, seen_cell_tuple=(None, None, None, True))

    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_num_of_empty_cells', mock_num_of_empty_cells)
    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_highest_possible_value', mock_highest_possible_value)
    def test_mark_general_seen_and_unseen_with_empty_cells(self):

        self._test_first_with_value_seen_with_empty_cells()

        self._test_unseen_with_empty_cells(hint_index=2, unseen_row=4, unseen_col=2, blocking_row=1, blocking_col=2,
                                           unseen_cell_tuple=(False, None, None, None))
        self._test_unseen_with_empty_cells(hint_index=8, unseen_row=2, unseen_col=1, blocking_row=2, blocking_col=4,
                                           unseen_cell_tuple=(None, False, None, None))
        self._test_unseen_with_empty_cells(hint_index=14, unseen_row=1, unseen_col=2, blocking_row=4, blocking_col=2,
                                           unseen_cell_tuple=(None, None, False, None))
        self._test_unseen_with_empty_cells(hint_index=20, unseen_row=2, unseen_col=4, blocking_row=2, blocking_col=1,
                                           unseen_cell_tuple=(None, None, None, False))

        self._test_non_blocked_with_empty_cells(
            hint_index=2, non_blocked_row=4, non_blocked_col=2, non_blocking_row=1, non_blocking_col=2)
        self._test_non_blocked_with_empty_cells(
            hint_index=8, non_blocked_row=2, non_blocked_col=1, non_blocking_row=2, non_blocking_col=4)
        self._test_non_blocked_with_empty_cells(
            hint_index=14, non_blocked_row=1, non_blocked_col=2, non_blocking_row=4, non_blocking_col=2)
        self._test_non_blocked_with_empty_cells(
            hint_index=20, non_blocked_row=2, non_blocked_col=4, non_blocking_row=2, non_blocking_col=1)

        self._test_seen_with_empty_cells(
            hint_index=2, first_low_row=0, first_low_col=2, second_low_row=1, second_low_col=2, seen_row=2, seen_col=2,
            seen_cell_tuple=(True, None, None, None))
        self._test_seen_with_empty_cells(
            hint_index=8, first_low_row=2, first_low_col=5, second_low_row=2, second_low_col=4, seen_row=2, seen_col=3,
            seen_cell_tuple=(None, True, None, None))
        self._test_seen_with_empty_cells(
            hint_index=14, first_low_row=5, first_low_col=2, second_low_row=4, second_low_col=2, seen_row=3, seen_col=2,
            seen_cell_tuple=(None, None, True, None))
        self._test_seen_with_empty_cells(
            hint_index=20, first_low_row=2, first_low_col=0, second_low_row=2, second_low_col=1, seen_row=2, seen_col=2,
            seen_cell_tuple=(None, None, None, True))

    def test_get_puzzle_with_filled_values(self):
        puzzle_grid = [[None, None, None], [1, None, None], [None, 2, None]]
        puzzle_grid_tuples = tuple(tuple(row) for row in puzzle_grid)
        p = AbstractPuzzleWithSkyscrapers(puzzle_grid_tuples, tuple([None] * 12))
        self.assertEqual(puzzle_grid, p._get_puzzle_with_filled_values())

    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_num_of_empty_cells', mock_num_of_empty_cells)
    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_highest_possible_value', mock_highest_possible_value)
    def test_are_values_unique(self):
        self._test_unique_values()
        self._test_value_repeats_in_row()
        self._test_value_repeats_in_col()
        self._test_empty_repeats_in_row_legit()
        self._test_empty_repeats_in_col_legit()
        self._test_empty_repeats_in_row_too_much()
        self._test_empty_repeats_in_col_too_much()

    def test_is_complete(self):
        p = AbstractPuzzleWithSkyscrapers(((1, 2, 3, 4), (2, 3, 4, 1), (3, 4, 1, 2), (4, 1, 2, None)),
                                          tuple([None] * 16))
        self.assertFalse(p._is_complete())
        p.puzzle_to_draw_on[3][3].set_value(3)
        self.assertTrue(p._is_complete())

    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_num_of_empty_cells', mock_num_of_empty_cells)
    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_highest_possible_value', mock_highest_possible_value)
    def test_count_cells_with_value(self):
        p = AbstractPuzzleWithSkyscrapers(((1, 2, 0, 0), (2, 0, 0, 1), (0, 0, 1, 2), (0, 1, 2, None)),
                                          tuple([None] * 16))
        self.assertEqual(15, p._count_filled_cells())
        p.puzzle_to_draw_on[3][3].set_value(0)
        self.assertEqual(16, p._count_filled_cells())

    def test_get_cell_with_distance_from_hint(self):
        p = AbstractPuzzleWithSkyscrapers(((None, 1, None, None), (2, None, None, None),
                                           (None, None, None, 3), (None, None, 4, None)),
                                          tuple([None] * 16))

        self.assertEqual(2, p._get_cell_with_distance_from_hint(0, 1)._value)
        self.assertEqual(1, p._get_cell_with_distance_from_hint(1, 0)._value)
        self.assertEqual(4, p._get_cell_with_distance_from_hint(2, 3)._value)
        self.assertEqual(3, p._get_cell_with_distance_from_hint(3, 2)._value)

        self.assertEqual(1, p._get_cell_with_distance_from_hint(4, 2)._value)
        self.assertEqual(2, p._get_cell_with_distance_from_hint(5, 3)._value)
        self.assertEqual(3, p._get_cell_with_distance_from_hint(6, 0)._value)
        self.assertEqual(4, p._get_cell_with_distance_from_hint(7, 1)._value)

        self.assertEqual(2, p._get_cell_with_distance_from_hint(8, 2)._value)
        self.assertEqual(1, p._get_cell_with_distance_from_hint(9, 3)._value)
        self.assertEqual(4, p._get_cell_with_distance_from_hint(10, 0)._value)
        self.assertEqual(3, p._get_cell_with_distance_from_hint(11, 1)._value)

        self.assertEqual(1, p._get_cell_with_distance_from_hint(12, 1)._value)
        self.assertEqual(2, p._get_cell_with_distance_from_hint(13, 0)._value)
        self.assertEqual(3, p._get_cell_with_distance_from_hint(14, 3)._value)
        self.assertEqual(4, p._get_cell_with_distance_from_hint(15, 2)._value)

    def test_can_cells_be_filled(self):
        self._test_row_cannot_be_filled()
        self._test_col_cannot_be_filled()
        self._test_can_be_filled()
        self._test_row_cannot_be_filled_with_empty_cells()
        self._test_col_cannot_be_filled_with_empty_cells()
        self._test_can_be_filled_with_empty_cells()

    def test_get_puzzle_state_drawing(self):
        grid = ((None, 1, None), (2, None, None), (None, None, 1))
        hints = (2, None, None, 1, None, None, None, None, 2, None, None, 3)
        p = AbstractPuzzleWithSkyscrapers(grid, hints)
        drawing = p.get_puzzle_state_drawing()
        expected = os.linesep + "    2 x x" + os.linesep + os.linesep \
                   + "x   x 1 x   1" + os.linesep \
                   + "x   2 x x   x" + os.linesep \
                   + "3   x x 1   x" + os.linesep + os.linesep \
                   + "    x x 2" + os.linesep
        self.assertEqual(expected, drawing)

    def test_get_hint_side(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([(tuple([None] * 8))] * 8), tuple([None] * 32))

        for i in range(8):
            self.assertEqual(0, p._get_hint_side(i))
        for i in range(8, 16):
            self.assertEqual(1, p._get_hint_side(i))
        for i in range(16, 24):
            self.assertEqual(2, p._get_hint_side(i))
        for i in range(24, 32):
            self.assertEqual(3, p._get_hint_side(i))

    def test_validate_hint_index(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([(tuple([None] * 8))] * 8), tuple([None] * 32))

        for i in range(32):
            p._validate_hint_index(i)
        with self.assertRaises(ValueError):
            p._validate_hint_index(-1)
        with self.assertRaises(ValueError):
            p._validate_hint_index(32)
        with self.assertRaises(ValueError):
            p._validate_hint_index(40)

    def _test_ctor_wrong_num_of_hints(self):
        with self.assertRaises(ValueError):
            AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3), tuple([None] * 16))
        with self.assertRaises(ValueError):
            AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3), tuple([None] * 9))

    def _test_ctor_illegal_hints(self):
        with self.assertRaises(ValueError):
            AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3),
                                          tuple(None if i != 1 else 4 for i in range(12)))
        with self.assertRaises(ValueError):
            AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3),
                                          tuple(None if i != 11 else 0 for i in range(12)))

    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_num_of_empty_cells', mock_num_of_empty_cells)
    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_highest_possible_value', mock_highest_possible_value)
    def _test_ctor_illegal_hints_with_empty_cells(self):
        with self.assertRaises(ValueError):
            AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3),
                                          tuple(None if i != 1 else 2 for i in range(12)))
        with self.assertRaises(ValueError):
            AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3),
                                          tuple(None if i != 11 else 0 for i in range(12)))

    def _test_ctor_legit(self):
        grid = ((None, 1, None), (2, None, None), (None, None, None))
        hints = (2, None, None, None, None, None, None, None, None, None, None, 3)
        seen = (((True, None, None, True), (True, None, None, None), (True, True, None, None)),
                ((None, None, None, True), (None, None, None, None), (None, True, None, None)),
                ((None, None, True, True), (None, None, True, None), (None, True, True, None)))
        p = AbstractPuzzleWithSkyscrapers(grid, hints)
        self.assertEqual(hints, p.hints)
        for i in range(3):
            for j in range(3):
                self.assertEqual(grid[i][j], p.puzzle_to_draw_on[i][j]._value)
                self.assertEqual(seen[i][j], p.puzzle_to_draw_on[i][j]._seen)

    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_num_of_empty_cells', mock_num_of_empty_cells)
    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_highest_possible_value', mock_highest_possible_value)
    def _test_ctor_legit_with_empty_cells(self):
        grid = ((None, 1, None, None), (1, None, None, None), (None, None, None, None), (None, None, None, None))
        hints = (1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 2)
        seen = (
            ((None, None, None, None), (None, None, None, None), (None, None, None, None), (None, None, None, None)),
            ((None, None, None, None), (None, None, None, None), (None, None, None, None), (None, None, None, None)),
            ((None, None, None, None), (None, None, None, None), (None, None, None, None), (None, None, None, None)),
            ((None, None, None, None), (None, None, None, None), (None, None, None, None), (None, None, None, None)))
        p = AbstractPuzzleWithSkyscrapers(grid, hints)
        self.assertEqual(hints, p.hints)
        for i in range(4):
            for j in range(4):
                self.assertEqual(grid[i][j], p.puzzle_to_draw_on[i][j]._value)
                self.assertEqual(seen[i][j], p.puzzle_to_draw_on[i][j]._seen)

    def _test_mark_illegal_clashing_values_no_empty_cells(self):
        p = AbstractPuzzleWithSkyscrapers(((None, None, None), (None, None, 2), (None, None, None)), tuple([None] * 12))
        for i in range(3):
            for j in range(3):
                if i != 1 or j != 2:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
        self.assertEqual(2, p.puzzle_to_draw_on[1][2]._value)
        self.assertEqual({1, 3}, p.puzzle_to_draw_on[1][2]._illegal_values)
        p._mark_illegal_clashing_values(1, 2)
        for i in range(3):
            for j in range(3):
                if i == 1 or j == 2:
                    if i == 1 and j == 2:
                        self.assertEqual(2, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual({1, 3}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    else:
                        self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual({2}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_num_of_empty_cells', mock_num_of_empty_cells)
    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_highest_possible_value', mock_highest_possible_value)
    def _test_mark_illegal_clashing_values_with_empty_cells(self):
        self._test_mark_illegal_clashing_values_with_empty_cells_for_cell_with_value()
        self._test_mark_illegal_clashing_values_with_empty_cells_for_single_empty_cell()
        self._test_mark_illegal_clashing_values_with_empty_cells_for_empty_cells_at_quota_col()
        self._test_mark_illegal_clashing_values_with_empty_cells_for_empty_cells_at_quota_row()

    def _test_mark_illegal_clashing_values_with_empty_cells_for_cell_with_value(self):
        p = AbstractPuzzleWithSkyscrapers(
            ((None, None, None, None), (None, None, 2, None), (None, None, None, None), (None, None, None, None)),
            tuple([None] * 16))
        for i in range(4):
            for j in range(4):
                if i != 1 or j != 2:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
        self.assertEqual(2, p.puzzle_to_draw_on[1][2]._value)
        self.assertEqual({0, 1}, p.puzzle_to_draw_on[1][2]._illegal_values)
        p._mark_illegal_clashing_values(1, 2)
        for i in range(3):
            for j in range(3):
                if i == 1 or j == 2:
                    if i == 1 and j == 2:
                        self.assertEqual(2, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual({0, 1}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    else:
                        self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual({2}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_illegal_clashing_values_with_empty_cells_for_single_empty_cell(self):
        p = AbstractPuzzleWithSkyscrapers(
            ((None, None, None, None), (None, None, 0, None), (None, None, None, None), (None, None, None, None)),
            tuple([None] * 16))
        for i in range(4):
            for j in range(4):
                if i != 1 or j != 2:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
        self.assertEqual(0, p.puzzle_to_draw_on[1][2]._value)
        self.assertEqual({1, 2}, p.puzzle_to_draw_on[1][2]._illegal_values)
        p._mark_illegal_clashing_values(1, 2)
        for i in range(3):
            for j in range(3):
                if i == 1 or j == 2:
                    if i == 1 and j == 2:
                        self.assertEqual(0, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual({1, 2}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    else:
                        self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_illegal_clashing_values_with_empty_cells_for_empty_cells_at_quota_col(self):
        p = AbstractPuzzleWithSkyscrapers(
            ((None, None, None, None), (None, None, 0, None), (None, None, 0, None), (None, None, None, None)),
            tuple([None] * 16))
        for i in range(4):
            for j in range(4):
                if i not in {1, 2} or j != 2:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
        self.assertEqual(0, p.puzzle_to_draw_on[1][2]._value)
        self.assertEqual({1, 2}, p.puzzle_to_draw_on[1][2]._illegal_values)
        p._mark_illegal_clashing_values(1, 2)
        for i in range(3):
            for j in range(3):
                if i in {1, 2} or j == 2:
                    if i in {1, 2} and j == 2:
                        self.assertEqual(0, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual({1, 2}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    elif j == 2:
                        self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual({0}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    else:
                        self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_illegal_clashing_values_with_empty_cells_for_empty_cells_at_quota_row(self):
        p = AbstractPuzzleWithSkyscrapers(
            ((None, None, None, None), (0, None, 0, None), (None, None, None, None), (None, None, None, None)),
            tuple([None] * 16))
        for i in range(4):
            for j in range(4):
                if i != 1 or j not in {0, 2}:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
        self.assertEqual(0, p.puzzle_to_draw_on[1][2]._value)
        self.assertEqual({1, 2}, p.puzzle_to_draw_on[1][2]._illegal_values)
        p._mark_illegal_clashing_values(1, 2)
        for i in range(3):
            for j in range(3):
                if i == 1 or j in {0, 2}:
                    if i == 1 and j in {0, 2}:
                        self.assertEqual(0, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual({1, 2}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    elif i == 1:
                        self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual({0}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    else:
                        self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_fill_only_possible_location_no_empty_cells(self):
        self._test_fill_only_possible_location_row()
        self._test_fill_only_possible_location_row_no_location()
        self._test_fill_only_possible_location_col()
        self._test_fill_only_possible_location_col_no_location()

    def _test_fill_only_possible_location_row(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3), tuple([None] * 12))
        p.puzzle_to_draw_on[0][0].add_illegal_value(2)
        p.puzzle_to_draw_on[0][1].add_illegal_value(2)
        p._fill_only_possible_locations()
        for i in range(3):
            for j in range(3):
                if i != 0 or j != 2:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                else:
                    self.assertEqual(2, p.puzzle_to_draw_on[i][j]._value)

    def _test_fill_only_possible_location_row_no_location(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3), tuple([None] * 12))
        p.puzzle_to_draw_on[0][0].add_illegal_value(2)
        p.puzzle_to_draw_on[0][1].add_illegal_value(2)
        p.puzzle_to_draw_on[0][2].add_illegal_value(2)
        with self.assertRaises(UnsolvableError):
            p._fill_only_possible_locations()

    def _test_fill_only_possible_location_col(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3), tuple([None] * 12))
        p.puzzle_to_draw_on[0][1].add_illegal_value(2)
        p.puzzle_to_draw_on[2][1].add_illegal_value(2)
        p._fill_only_possible_locations()
        for i in range(3):
            for j in range(3):
                if i != 1 or j != 1:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                else:
                    self.assertEqual(2, p.puzzle_to_draw_on[i][j]._value)

    def _test_fill_only_possible_location_col_no_location(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3), tuple([None] * 12))
        p.puzzle_to_draw_on[0][1].add_illegal_value(2)
        p.puzzle_to_draw_on[2][1].add_illegal_value(2)
        p.puzzle_to_draw_on[1][1].add_illegal_value(2)
        with self.assertRaises(UnsolvableError):
            p._fill_only_possible_locations()

    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_num_of_empty_cells', mock_num_of_empty_cells)
    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_highest_possible_value', mock_highest_possible_value)
    def _test_fill_only_possible_location_with_empty_cells(self):
        self._test_fill_only_possible_location_empty_cells()
        self._test_fill_only_possible_location_row_no_location_empty_cells()
        self._test_fill_only_possible_location_col_no_location_empty_cells()

    def _test_fill_only_possible_location_empty_cells(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3), tuple([None] * 12))
        p.puzzle_to_draw_on[0][0].add_illegal_value(0)
        p._fill_only_possible_locations()
        for i in range(3):
            for j in range(3):
                if i == 0 and j == 0:
                    self.assertNotEqual(0, p.puzzle_to_draw_on[i][j]._value)
                elif i == 0 or j == 0:
                    self.assertEqual(0, p.puzzle_to_draw_on[i][j]._value)
                else:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)

    def _test_fill_only_possible_location_row_no_location_empty_cells(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3), tuple([None] * 12))
        p.puzzle_to_draw_on[0][0].add_illegal_value(0)
        p.puzzle_to_draw_on[0][1].add_illegal_value(0)
        with self.assertRaises(UnsolvableError):
            p._fill_only_possible_locations()

    def _test_fill_only_possible_location_col_no_location_empty_cells(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3), tuple([None] * 12))
        p.puzzle_to_draw_on[0][1].add_illegal_value(0)
        p.puzzle_to_draw_on[2][1].add_illegal_value(0)
        with self.assertRaises(UnsolvableError):
            p._fill_only_possible_locations()

    def _test_unseen(self, hint_index: int, unseen_row: int, unseen_col: int, blocking_row: int, blocking_col: int,
                     unseen_cell_tuple: Tuple[Optional[bool], Optional[bool], Optional[bool], Optional[bool]]):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 6)] * 6),
                                          tuple([None] * 24))
        p.puzzle_to_draw_on[unseen_row][unseen_col].add_illegal_value(6)
        p.puzzle_to_draw_on[blocking_row][blocking_col].add_illegal_value(4)
        p.puzzle_to_draw_on[blocking_row][blocking_col].add_illegal_value(3)
        p.puzzle_to_draw_on[blocking_row][blocking_col].add_illegal_value(2)
        p.puzzle_to_draw_on[blocking_row][blocking_col].add_illegal_value(1)
        p._mark_general_seen_and_unseen(hint_index)
        for i in range(6):
            for j in range(6):
                if i == blocking_row and j == blocking_col:
                    self.assertEqual((None, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                elif i == unseen_row and j == unseen_col:
                    self.assertEqual(unseen_cell_tuple, p.puzzle_to_draw_on[i][j]._seen)
                else:
                    # The ctor marks the cells on the edges as seen from that side.
                    self.assertEqual((None if i != 0 else True, None if j != 5 else True,
                                      None if i != 5 else True, None if j != 0 else True),
                                     p.puzzle_to_draw_on[i][j]._seen)

    def _test_unseen_with_empty_cells(
            self, hint_index: int, unseen_row: int, unseen_col: int, blocking_row: int, blocking_col: int,
            unseen_cell_tuple: Tuple[Optional[bool], Optional[bool], Optional[bool], Optional[bool]]):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 6)] * 6),
                                          tuple([None] * 24))
        p.puzzle_to_draw_on[unseen_row][unseen_col].add_illegal_value(4)
        p.puzzle_to_draw_on[blocking_row][blocking_col].add_illegal_value(2)
        p.puzzle_to_draw_on[blocking_row][blocking_col].add_illegal_value(1)
        p.puzzle_to_draw_on[blocking_row][blocking_col].add_illegal_value(0)
        p._mark_general_seen_and_unseen(hint_index)
        for i in range(6):
            for j in range(6):
                if i == blocking_row and j == blocking_col:
                    self.assertEqual((None, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                elif i == unseen_row and j == unseen_col:
                    self.assertEqual(unseen_cell_tuple, p.puzzle_to_draw_on[i][j]._seen)
                else:
                    self.assertEqual((None, None, None, None), p.puzzle_to_draw_on[i][j]._seen)

    def _test_non_blocked(
            self, hint_index: int, non_blocked_row: int, non_blocked_col: int, non_blocking_row: int,
            non_blocking_col: int):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 6)] * 6),
                                          tuple([None] * 24))
        p.puzzle_to_draw_on[non_blocked_row][non_blocked_col].add_illegal_value(6)
        p.puzzle_to_draw_on[non_blocked_row][non_blocked_col].add_illegal_value(1)
        p.puzzle_to_draw_on[non_blocking_row][non_blocking_col].add_illegal_value(6)
        p.puzzle_to_draw_on[non_blocking_row][non_blocking_col].add_illegal_value(1)
        p._mark_general_seen_and_unseen(hint_index)
        for i in range(6):
            for j in range(6):
                # The ctor marks the cells on the edges as seen from that side.
                self.assertEqual((None if i != 0 else True, None if j != 5 else True,
                                  None if i != 5 else True, None if j != 0 else True),
                                 p.puzzle_to_draw_on[i][j]._seen)

    def _test_non_blocked_with_empty_cells(
            self, hint_index: int, non_blocked_row: int, non_blocked_col: int, non_blocking_row: int,
            non_blocking_col: int):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 6)] * 6),
                                          tuple([None] * 24))
        p.puzzle_to_draw_on[non_blocked_row][non_blocked_col].add_illegal_value(4)
        p.puzzle_to_draw_on[non_blocked_row][non_blocked_col].add_illegal_value(1)
        p.puzzle_to_draw_on[non_blocked_row][non_blocked_col].add_illegal_value(0)
        p.puzzle_to_draw_on[non_blocking_row][non_blocking_col].add_illegal_value(4)
        p.puzzle_to_draw_on[non_blocking_row][non_blocking_col].add_illegal_value(1)
        p.puzzle_to_draw_on[non_blocking_row][non_blocking_col].add_illegal_value(0)
        p._mark_general_seen_and_unseen(hint_index)
        for i in range(6):
            for j in range(6):
                self.assertEqual((None, None, None, None), p.puzzle_to_draw_on[i][j]._seen)

    def _test_seen(self, hint_index: int, first_low_row: int, first_low_col: int, second_low_row: int,
                   second_low_col: int, seen_row: int, seen_col: int,
                   seen_cell_tuple: Tuple[Optional[bool], Optional[bool], Optional[bool], Optional[bool]]):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 6)] * 6),
                                          tuple([None] * 24))
        p.puzzle_to_draw_on[first_low_row][first_low_col].add_illegal_value(6)
        p.puzzle_to_draw_on[second_low_row][second_low_col].add_illegal_value(6)
        p.puzzle_to_draw_on[seen_row][seen_col].add_illegal_value(4)
        p.puzzle_to_draw_on[seen_row][seen_col].add_illegal_value(3)
        p.puzzle_to_draw_on[seen_row][seen_col].add_illegal_value(2)
        p.puzzle_to_draw_on[seen_row][seen_col].add_illegal_value(1)
        p._mark_general_seen_and_unseen(hint_index)
        for i in range(6):
            for j in range(6):
                if i == seen_row and j == seen_col:
                    self.assertEqual(seen_cell_tuple, p.puzzle_to_draw_on[i][j]._seen)
                else:
                    # The ctor marks the cells on the edges as seen from that side.
                    self.assertEqual((None if i != 0 else True, None if j != 5 else True,
                                      None if i != 5 else True, None if j != 0 else True),
                                     p.puzzle_to_draw_on[i][j]._seen)

    def _test_seen_with_empty_cells(
            self, hint_index: int, first_low_row: int, first_low_col: int, second_low_row: int,
            second_low_col: int, seen_row: int, seen_col: int,
            seen_cell_tuple: Tuple[Optional[bool], Optional[bool], Optional[bool], Optional[bool]]):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 6)] * 6),
                                          tuple([None] * 24))
        p.puzzle_to_draw_on[first_low_row][first_low_col].add_illegal_value(4)
        p.puzzle_to_draw_on[second_low_row][second_low_col].add_illegal_value(4)
        p.puzzle_to_draw_on[seen_row][seen_col].add_illegal_value(2)
        p.puzzle_to_draw_on[seen_row][seen_col].add_illegal_value(1)
        p.puzzle_to_draw_on[seen_row][seen_col].add_illegal_value(0)
        p._mark_general_seen_and_unseen(hint_index)
        for i in range(6):
            for j in range(6):
                if i == seen_row and j == seen_col:
                    self.assertEqual(seen_cell_tuple, p.puzzle_to_draw_on[i][j]._seen)
                else:
                    self.assertEqual((None, None, None, None), p.puzzle_to_draw_on[i][j]._seen)

    def _test_first_with_value_seen_with_empty_cells(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 6)] * 6),
                                          tuple([None] * 24))
        p.puzzle_to_draw_on[4][0].add_illegal_value(0)
        p._mark_general_seen_and_unseen(22)
        for i in range(6):
            for j in range(6):
                if i == 4 and j == 0:
                    self.assertEqual((None, None, None, True), p.puzzle_to_draw_on[i][j]._seen)
                else:
                    self.assertEqual((None, None, None, None), p.puzzle_to_draw_on[i][j]._seen)

    def _test_unique_values(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 4)] * 4),
                                          tuple([None] * 16))
        p.puzzle_to_draw_on[0][0].set_value(1)
        p.puzzle_to_draw_on[0][2].set_value(2)
        p.puzzle_to_draw_on[2][0].set_value(2)
        p.puzzle_to_draw_on[2][2].set_value(1)
        self.assertTrue(p._are_values_unique())

    def _test_value_repeats_in_row(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 4)] * 4),
                                          tuple([None] * 16))
        p.puzzle_to_draw_on[2][0].set_value(1)
        p.puzzle_to_draw_on[2][2].set_value(1)
        self.assertFalse(p._are_values_unique())

    def _test_value_repeats_in_col(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 4)] * 4),
                                          tuple([None] * 16))
        p.puzzle_to_draw_on[1][3].set_value(1)
        p.puzzle_to_draw_on[3][3].set_value(1)
        self.assertFalse(p._are_values_unique())

    def _test_empty_repeats_in_row_legit(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 4)] * 4),
                                          tuple([None] * 16))
        p.puzzle_to_draw_on[2][0].set_value(0)
        p.puzzle_to_draw_on[2][2].set_value(0)
        self.assertTrue(p._are_values_unique())

    def _test_empty_repeats_in_col_legit(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 4)] * 4),
                                          tuple([None] * 16))
        p.puzzle_to_draw_on[1][3].set_value(0)
        p.puzzle_to_draw_on[3][3].set_value(0)
        self.assertTrue(p._are_values_unique())

    def _test_empty_repeats_in_row_too_much(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 4)] * 4),
                                          tuple([None] * 16))
        p.puzzle_to_draw_on[2][0].set_value(0)
        p.puzzle_to_draw_on[2][2].set_value(0)
        p.puzzle_to_draw_on[2][3].set_value(0)
        self.assertFalse(p._are_values_unique())

    def _test_empty_repeats_in_col_too_much(self):
        p = AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 4)] * 4),
                                          tuple([None] * 16))
        p.puzzle_to_draw_on[1][3].set_value(0)
        p.puzzle_to_draw_on[2][3].set_value(0)
        p.puzzle_to_draw_on[3][3].set_value(0)
        self.assertFalse(p._are_values_unique())

    def _test_row_cannot_be_filled(self):
        p = AbstractPuzzleWithSkyscrapers(((None, None, None, None), (None, None, None, None),
                                           (None, None, None, None), (None, None, None, None)),
                                          tuple([None] * 16))
        p.puzzle_to_draw_on[1][0].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(3)
        p.puzzle_to_draw_on[1][2].add_illegal_value(3)
        p.puzzle_to_draw_on[1][3].add_illegal_value(3)
        self.assertFalse(p._can_cells_be_filled())

    def _test_col_cannot_be_filled(self):
        p = AbstractPuzzleWithSkyscrapers(((None, None, None, None), (None, None, None, None),
                                           (None, None, None, None), (None, None, None, None)),
                                          tuple([None] * 16))
        p.puzzle_to_draw_on[0][1].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(3)
        p.puzzle_to_draw_on[2][1].add_illegal_value(3)
        p.puzzle_to_draw_on[3][1].add_illegal_value(3)
        self.assertFalse(p._can_cells_be_filled())

    def _test_can_be_filled(self):
        p = AbstractPuzzleWithSkyscrapers(((None, None, None, None), (None, None, None, None),
                                           (None, None, None, None), (None, None, None, None)),
                                          tuple([None] * 16))

        p.puzzle_to_draw_on[1][0].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(4)
        p.puzzle_to_draw_on[1][2].add_illegal_value(4)
        p.puzzle_to_draw_on[1][3].add_illegal_value(2)
        p.puzzle_to_draw_on[0][1].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(4)
        p.puzzle_to_draw_on[2][1].add_illegal_value(4)
        p.puzzle_to_draw_on[3][1].add_illegal_value(2)

        self.assertTrue(p._can_cells_be_filled())

    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_num_of_empty_cells', mock_num_of_empty_cells)
    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_highest_possible_value', mock_highest_possible_value)
    def _test_row_cannot_be_filled_with_empty_cells(self):
        p = AbstractPuzzleWithSkyscrapers(((None, None, None, None), (None, None, None, None),
                                           (None, None, None, None), (None, None, None, None)),
                                          tuple([None] * 16))
        p.puzzle_to_draw_on[1][0].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(2)
        p.puzzle_to_draw_on[1][2].add_illegal_value(2)
        p.puzzle_to_draw_on[1][3].add_illegal_value(2)
        self.assertFalse(p._can_cells_be_filled())

    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_num_of_empty_cells', mock_num_of_empty_cells)
    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_highest_possible_value', mock_highest_possible_value)
    def _test_col_cannot_be_filled_with_empty_cells(self):
        p = AbstractPuzzleWithSkyscrapers(((None, None, None, None), (None, None, None, None),
                                           (None, None, None, None), (None, None, None, None)),
                                          tuple([None] * 16))
        p.puzzle_to_draw_on[0][1].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(2)
        p.puzzle_to_draw_on[2][1].add_illegal_value(2)
        p.puzzle_to_draw_on[3][1].add_illegal_value(2)
        self.assertFalse(p._can_cells_be_filled())

    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_num_of_empty_cells', mock_num_of_empty_cells)
    @patch.object(AbstractPuzzleWithSkyscrapers, '_get_highest_possible_value', mock_highest_possible_value)
    def _test_can_be_filled_with_empty_cells(self):
        p = AbstractPuzzleWithSkyscrapers(((None, None, None, None), (None, None, None, None),
                                           (None, None, None, None), (None, None, None, None)),
                                          tuple([None] * 16))

        p.puzzle_to_draw_on[1][0].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(2)
        p.puzzle_to_draw_on[1][2].add_illegal_value(2)
        p.puzzle_to_draw_on[1][3].add_illegal_value(0)
        p.puzzle_to_draw_on[0][1].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(2)
        p.puzzle_to_draw_on[2][1].add_illegal_value(2)
        p.puzzle_to_draw_on[3][1].add_illegal_value(0)

        self.assertTrue(p._can_cells_be_filled())


if __name__ == '__main__':
    unittest.main()
