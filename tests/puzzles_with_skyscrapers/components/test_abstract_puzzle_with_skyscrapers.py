import io
import os
import unittest
from typing import Tuple, Optional
from unittest.mock import patch

from src.puzzles_with_skyscrapers.components.abstract_puzzle_with_skyscrapers import AbstractPuzzleWithSkyscrapers


@patch.object(AbstractPuzzleWithSkyscrapers, '__abstractmethods__', set())
class TestCellWithSkyscraper(unittest.TestCase):

    def test_ctor(self):
        self._test_ctor_legit()

    def test_mark_illegal_clashing_values(self):
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

    def test_fill_only_possible_locations(self):
        self._test_fill_only_possible_location_row()
        self._test_fill_only_possible_location_col()

    def test_mark_general_seen_and_unseen(self):
        self._test_unseen_all_directions()
        self._test_non_blocked_all_directions()
        self._test_seen_all_directions()

    def test_get_puzzle_with_filled_values(self):
        puzzle_grid = [[None, None, None], [1, None, None], [None, 2, None]]
        puzzle_grid_tuples = tuple(tuple(row) for row in puzzle_grid)
        p = AbstractPuzzleWithSkyscrapers(puzzle_grid_tuples, tuple([None] * 12))
        self.assertEqual(puzzle_grid, p._get_puzzle_with_filled_values())

    def test_are_values_unique(self):
        self._test_unique_values()
        self._test_value_repeats_in_row()
        self._test_value_repeats_in_col()

    def test_is_complete(self):
        p = AbstractPuzzleWithSkyscrapers(((1, 2, 3, 4), (2, 3, 4, 1), (3, 4, 1, 2), (4, 1, 2, None)),
                                          tuple([None] * 16))
        self.assertFalse(p._is_complete())
        p.puzzle_to_draw_on[3][3].set_value(3)
        self.assertTrue(p._is_complete())

    def test_count_cells_with_value(self):
        p = AbstractPuzzleWithSkyscrapers(((1, 2, 3, 4), (2, 3, 4, 1), (3, 4, 1, 2), (4, 1, 2, None)),
                                          tuple([None] * 16))
        self.assertEqual(15, p._count_cells_with_value())
        p.puzzle_to_draw_on[3][3].set_value(3)
        self.assertEqual(16, p._count_cells_with_value())

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

    def _test_ctor_wrong_num_of_hints(self):
        with self.assertRaises(ValueError):
            AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3), tuple([None] * 16))
        with self.assertRaises(ValueError):
            AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3), tuple([None] * 9))

    def _test_ctor_illegal_hints(self):
        self._test_ctor_wrong_num_of_hints()
        with self.assertRaises(ValueError):
            AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3),
                                          tuple(None if i != 1 else 4 for i in range(12)))
        with self.assertRaises(ValueError):
            AbstractPuzzleWithSkyscrapers(tuple([tuple([None] * 3)] * 3),
                                          tuple(None if i != 11 else 0 for i in range(12)))

    def _test_ctor_legit(self):
        self._test_ctor_illegal_hints()
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

    def _test_unseen_all_directions(self):
        self._test_unseen_from_top()
        self._test_unseen_from_right()
        self._test_unseen_from_bottom()
        self._test_unseen_from_left()

    def _test_non_blocked_all_directions(self):
        self._test_non_blocked_from_top()
        self._test_non_blocked_from_right()
        self._test_non_blocked_from_bottom()
        self._test_non_blocked_from_left()

    def _test_seen_all_directions(self):
        self._test_seen_from_top()
        self._test_seen_from_right()
        self._test_seen_from_bottom()
        self._test_seen_from_left()

    def _test_unseen_from_top(self):
        self._test_unseen(hint_index=2, unseen_row=4, unseen_col=2, blocking_row=1, blocking_col=2,
                          unseen_cell_tuple=(False, None, None, None))

    def _test_unseen_from_right(self):
        self._test_unseen(hint_index=8, unseen_row=2, unseen_col=1, blocking_row=2, blocking_col=4,
                          unseen_cell_tuple=(None, False, None, None))

    def _test_unseen_from_bottom(self):
        self._test_unseen(hint_index=14, unseen_row=1, unseen_col=2, blocking_row=4, blocking_col=2,
                          unseen_cell_tuple=(None, None, False, None))

    def _test_unseen_from_left(self):
        self._test_unseen(hint_index=20, unseen_row=2, unseen_col=4, blocking_row=2, blocking_col=1,
                          unseen_cell_tuple=(None, None, None, False))

    def _test_non_blocked_from_top(self):
        self._test_non_blocked(hint_index=2, non_blocked_row=4, non_blocked_col=2, non_blocking_row=1,
                               non_blocking_col=2)

    def _test_non_blocked_from_right(self):
        self._test_non_blocked(hint_index=8, non_blocked_row=2, non_blocked_col=1, non_blocking_row=2,
                               non_blocking_col=4)

    def _test_non_blocked_from_bottom(self):
        self._test_non_blocked(hint_index=14, non_blocked_row=1, non_blocked_col=2, non_blocking_row=4,
                               non_blocking_col=2)

    def _test_non_blocked_from_left(self):
        self._test_non_blocked(hint_index=20, non_blocked_row=2, non_blocked_col=4, non_blocking_row=2,
                               non_blocking_col=1)

    def _test_seen_from_top(self):
        self._test_seen(hint_index=2, first_low_row=0, first_low_col=2, second_low_row=1, second_low_col=2,
                        seen_row=2, seen_col=2, seen_cell_tuple=(True, None, None, None))

    def _test_seen_from_right(self):
        self._test_seen(hint_index=8, first_low_row=2, first_low_col=5, second_low_row=2, second_low_col=4,
                        seen_row=2, seen_col=3, seen_cell_tuple=(None, True, None, None))

    def _test_seen_from_bottom(self):
        self._test_seen(hint_index=14, first_low_row=5, first_low_col=2, second_low_row=4, second_low_col=2,
                        seen_row=3, seen_col=2, seen_cell_tuple=(None, None, True, None))

    def _test_seen_from_left(self):
        self._test_seen(hint_index=20, first_low_row=2, first_low_col=0, second_low_row=2, second_low_col=1,
                        seen_row=2, seen_col=2, seen_cell_tuple=(None, None, None, True))

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
                    # The ctor marks the cells on the edges as seen from that direction.
                    self.assertEqual((None if i != 0 else True, None if j != 5 else True,
                                      None if i != 5 else True, None if j != 0 else True),
                                     p.puzzle_to_draw_on[i][j]._seen)

    def _test_non_blocked(self, hint_index: int, non_blocked_row: int, non_blocked_col: int, non_blocking_row: int,
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
                # The ctor marks the cells on the edges as seen from that direction.
                self.assertEqual((None if i != 0 else True, None if j != 5 else True,
                                  None if i != 5 else True, None if j != 0 else True),
                                 p.puzzle_to_draw_on[i][j]._seen)

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
                    # The ctor marks the cells on the edges as seen from that direction.
                    self.assertEqual((None if i != 0 else True, None if j != 5 else True,
                                      None if i != 5 else True, None if j != 0 else True),
                                     p.puzzle_to_draw_on[i][j]._seen)

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


if __name__ == '__main__':
    unittest.main()
