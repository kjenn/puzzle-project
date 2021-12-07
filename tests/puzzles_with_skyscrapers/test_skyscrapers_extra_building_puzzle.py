import unittest
from typing import Tuple, Optional, List

from src.components.unsolvable_error import UnsolvableError
from src.puzzles_with_skyscrapers.components.cell_with_skyscraper import CellWithSkyscraper
from src.puzzles_with_skyscrapers.skyscrapers_extra_building_puzzle import SkyscrapersExtraBuildingPuzzle


class TestSkyscrapersExtraBuildingPuzzle(unittest.TestCase):

    def test_flow(self):
        self._test_flow_solvable_no_values()
        self._test_flow_solvable_hint_and_values()
        self._test_flow_unsolvable_no_hints()
        self._test_flow_unsolvable_no_values()
        self._test_flow_unsolvable_hints_and_values()
        self._test_flow_several_solutions_no_hints_no_values()
        self._test_flow_several_solutions_no_hints()
        self._test_flow_several_solutions_no_values()
        self._test_flow_several_solutions_hints_and_values()

    def test_are_puzzle_specifics_valid(self):

        p1 = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 4)] * 4),
                                            tuple([None if i not in {0, 8} else 3 for i in range(16)]))
        self.assertFalse(p1._are_puzzle_specifics_valid())

        p2 = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 4)] * 4),
                                            tuple([None if i not in {4, 12} else 3 for i in range(16)]))
        self.assertFalse(p2._are_puzzle_specifics_valid())

        p3 = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 4)] * 4),
                                            tuple([None if i not in {0, 4, 9, 13} else 3 for i in range(16)]))
        self.assertTrue(p3._are_puzzle_specifics_valid())

        p4 = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 4)] * 4),
                                            tuple([None if i not in {2, 6} else 3 for i in range(8)]
                                                  + [None if i not in {2, 6} else 2 for i in range(8)]))
        self.assertTrue(p4._are_puzzle_specifics_valid())

        p5 = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 4)] * 4),
                                            tuple([None if i not in {0, 4, 8, 12} else 2 for i in range(16)]))
        self.assertTrue(p5._are_puzzle_specifics_valid())

    def test_mark_basic_conclusions(self):
        self._test_mark_basic_conclusions_from_top()
        self._test_mark_basic_conclusions_from_top_generalized()
        self._test_mark_basic_conclusions_from_right()
        self._test_mark_basic_conclusions_from_bottom()
        self._test_mark_basic_conclusions_from_left()

    def test_mark_puzzle_specific_seen_and_unseen(self):
        self._test_mark_unseen()
        self._test_mark_seen()
        self._test_too_many_unseen()
        self._test_too_many_seen()

    def test_mark_cell_illegals_for_seen_status(self):
        self._test_mark_cell_illegals_for_seen()
        self._test_mark_cell_illegals_blocking()
        self._test_mark_cell_illegals_for_unseen_no_data()
        self._test_mark_cell_illegals_for_unseen()

    def _test_flow_solvable_no_values(self):
        p1 = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 5)] * 5),
                                            (None, None, None, None, None,
                                             5, 5, 3, 3, None,
                                             4, None, 3, 1, None,
                                             None, None, None, 3, None))
        sol1 = p1.solve()
        self.assertEqual([[6, 5, 4, 3, 2],
                          [5, 4, 3, 2, 1],
                          [3, 1, 6, 5, 4],
                          [1, 2, 5, 4, 3],
                          [2, 3, 1, 6, 5]],
                         sol1)

        p2 = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 5)] * 5),
                                            (None, None, 3, None, 3,
                                             3, 2, 3, None, None,
                                             3, 4, 3, 3, 2,
                                             2, 3, 3, 5, 4))
        sol2 = p2.solve()
        self.assertEqual([[5, 6, 1, 3, 2],
                          [3, 2, 5, 6, 4],
                          [4, 5, 6, 2, 1],
                          [1, 3, 4, 5, 6],
                          [2, 1, 3, 4, 5]],
                         sol2)

    def _test_flow_solvable_hint_and_values(self):
        p = SkyscrapersExtraBuildingPuzzle(((None, None, None, None, None, None),
                                            (None, None, None, None, None, None),
                                            (None, None, None, None, None, 1),
                                            (None, None, None, None, None, None),
                                            (None, None, None, None, None, 4),
                                            (None, None, None, None, None, None)),
                                           tuple([6, 6, 5, 4, 3, 2] +
                                                 [None] * 6 +
                                                 [None, None, None, None, 4, None] +
                                                 [None, None, None, None, None, 2]))
        sol = p.solve()
        self.assertEqual([[1, 2, 3, 4, 5, 6],
                          [2, 3, 4, 5, 6, 7],
                          [3, 4, 5, 6, 7, 1],
                          [4, 5, 6, 7, 3, 2],
                          [5, 6, 7, 1, 2, 4],
                          [6, 7, 2, 3, 1, 5]],
                         sol)

    def test_can_cells_be_filled(self):
        self._test_row_cannot_be_filled()
        self._test_col_cannot_be_filled()
        self._test_can_be_filled()

    def test_mark_general_seen_and_unseen(self):
        self._test_unseen_all_sides()
        self._test_non_blocked_all_sides()
        self._test_seen_all_sides()

    def test_mark_illegal_clashing_values(self):
        p = SkyscrapersExtraBuildingPuzzle(
            ((None, None, None), (None, None, 2), (None, None, None)), tuple([None] * 12))
        for i in range(3):
            for j in range(3):
                if i != 1 or j != 2:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
        self.assertEqual(2, p.puzzle_to_draw_on[1][2]._value)
        self.assertEqual({1, 3, 4}, p.puzzle_to_draw_on[1][2]._illegal_values)
        p._mark_illegal_clashing_values(1, 2)
        for i in range(3):
            for j in range(3):
                if i == 1 or j == 2:
                    if i == 1 and j == 2:
                        self.assertEqual(2, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual({1, 3, 4}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    else:
                        self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                        self.assertEqual({2}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(None, p.puzzle_to_draw_on[i][j]._value)
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_flow_unsolvable_no_hints(self):
        p = SkyscrapersExtraBuildingPuzzle(((1, None, None, 4, None, None),
                                            (4, 1, None, None, None, None),
                                            (None, 4, 1, None, None, None),
                                            (None, None, 4, 1, None, None),
                                            (None, None, None, None, 2, 3),
                                            (None, None, None, None, 3, 2)),
                                           tuple([None] * 24))
        sol = p.solve()
        self.assertEqual(None, sol)

    def _test_flow_unsolvable_no_values(self):
        p1 = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 5)] * 5),
                                            (2, None, None, None, None,
                                             5, 5, 3, 3, None,
                                             4, None, 3, 1, None,
                                             None, None, None, 3, None))
        sol1 = p1.solve()
        self.assertEqual(None, sol1)

        p2 = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 6)] * 6),
                                            tuple([3, None, None, None, None, None] + [None] * 6
                                                  + [5, None, None, None, None, None] + [None] * 6))
        sol2 = p2.solve()
        self.assertEqual(None, sol2)

    def _test_flow_unsolvable_hints_and_values(self):
        p1 = SkyscrapersExtraBuildingPuzzle(((5, None, None, None, None, None),
                                             (None, None, None, None, None, None),
                                             (None, None, None, None, None, None),
                                             (None, None, None, None, None, None),
                                             (None, None, None, None, None, None),
                                             (None, None, None, None, None, None)),
                                            tuple([4, None, None, None, None, None] + [None] * 18))
        sol1 = p1.solve()
        self.assertEqual(None, sol1)

        p2 = SkyscrapersExtraBuildingPuzzle(((5, None, None, None, None),
                                             (None, None, None, None, None),
                                             (None, None, None, None, None),
                                             (None, None, None, None, None),
                                             (None, None, None, None, None)),
                                            (None, None, None, None, None,
                                             5, 5, 3, 3, None,
                                             4, None, 3, 1, None,
                                             None, None, None, 3, None))
        sol2 = p2.solve()
        self.assertEqual(None, sol2)

    def _test_flow_several_solutions_no_hints_no_values(self):
        p = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 6)] * 6),
                                           tuple([None] * 24))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))

    def _test_flow_several_solutions_no_hints(self):
        p = SkyscrapersExtraBuildingPuzzle(((1, 2, 3, 4, 6, None),
                                            (2, 3, 4, 1, 5, 6),
                                            (3, 4, 5, 6, 1, 2),
                                            (4, 1, 6, 5, 2, 3),
                                            (5, 6, 1, 2, 3, 4),
                                            (6, 5, 2, 3, 4, 1)),
                                           tuple([None] * 24))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))
        self.assertEqual(2, len(sol))
        self.assertIn(
            [[1, 2, 3, 4, 6, 7],
             [2, 3, 4, 1, 5, 6],
             [3, 4, 5, 6, 1, 2],
             [4, 1, 6, 5, 2, 3],
             [5, 6, 1, 2, 3, 4],
             [6, 5, 2, 3, 4, 1]],
            sol)
        self.assertIn(
            [[1, 2, 3, 4, 6, 5],
             [2, 3, 4, 1, 5, 6],
             [3, 4, 5, 6, 1, 2],
             [4, 1, 6, 5, 2, 3],
             [5, 6, 1, 2, 3, 4],
             [6, 5, 2, 3, 4, 1]],
            sol)

    def _test_flow_several_solutions_no_values(self):
        p1 = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 6)] * 6),
                                            tuple([6, 5, 4, 3, 2, 1] + [None] * 18))
        sol1 = p1.solve()
        self.assertTrue(isinstance(sol1, tuple))

        p2 = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 5)] * 5),
                                            (None, None, None, None, None,
                                             None, 5, 3, 3, None,
                                             4, None, 3, 1, None,
                                             None, None, None, 3, None))

        sol2 = p2.solve()
        self.assertTrue(isinstance(sol2, tuple))

    def _test_flow_several_solutions_hints_and_values(self):
        p = SkyscrapersExtraBuildingPuzzle(((None, None, None, None, None, None),
                                            (None, None, None, None, None, None),
                                            (None, None, None, None, None, None),
                                            (None, None, None, None, None, None),
                                            (None, None, None, None, None, None),
                                            (None, None, None, None, 4, None)),
                                           tuple([6, 5, 4, None, None, None] + [None] * 18))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))

    def _test_mark_basic_conclusions_from_top(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 6)] * 6), tuple([None if i != 0 else 4 for i in range(24)]))
        p._mark_basic_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 0 and i == 0:
                    self.assertEqual({5, 6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 1:
                    self.assertEqual({6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 2:
                    self.assertEqual({7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_top_generalized(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 6)] * 6), tuple([None if i != 0 else 4 for i in range(24)]))
        p.puzzle_to_draw_on[1][0].set_seen_from_side(0, False)
        p.puzzle_to_draw_on[2][0].set_seen_from_side(0, False)
        p._mark_basic_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 0 and i == 0:
                    self.assertEqual({5, 6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 1:
                    self.assertEqual({5, 6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 2:
                    self.assertEqual({5, 6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 3:
                    self.assertEqual({6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 4:
                    self.assertEqual({7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_right(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 6)] * 6), tuple([None if i != 7 else 3 for i in range(24)]))
        p._mark_basic_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 5 and i == 1:
                    self.assertEqual({6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 4 and i == 1:
                    self.assertEqual({7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_bottom(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 6)] * 6), tuple([None if i != 14 else 5 for i in range(24)]))
        p._mark_basic_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 2 and i == 5:
                    self.assertEqual({4, 5, 6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 2 and i == 4:
                    self.assertEqual({5, 6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 2 and i == 3:
                    self.assertEqual({6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 2 and i == 2:
                    self.assertEqual({7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_left(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 6)] * 6), tuple([None if i != 21 else 2 for i in range(24)]))
        p._mark_basic_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 0 and i == 3:
                    self.assertEqual({7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_unseen(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 4)] * 4), tuple([None if i != 1 else 3 for i in range(16)]))
        p.puzzle_to_draw_on[2][1]._set_seen((True, None, None, None))
        p.puzzle_to_draw_on[3][1]._set_seen((True, None, None, None))
        p._mark_puzzle_specific_seen_and_unseen(1)
        self._check_seen_unseen_col_1_row_1_unseen_col_1_rest_seen(p.puzzle_to_draw_on)

    def _test_mark_seen(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 4)] * 4), tuple([None if i != 1 else 3 for i in range(16)]))
        p.puzzle_to_draw_on[1][1]._set_seen((False, None, None, None))
        p._mark_puzzle_specific_seen_and_unseen(1)
        self._check_seen_unseen_col_1_row_1_unseen_col_1_rest_seen(p.puzzle_to_draw_on)

    def _test_too_many_unseen(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 4)] * 4), tuple([None if i != 1 else 3 for i in range(16)]))
        p.puzzle_to_draw_on[1][1]._set_seen((False, None, None, None))
        p.puzzle_to_draw_on[2][1]._set_seen((False, None, None, None))
        with self.assertRaises(UnsolvableError):
            p._mark_puzzle_specific_seen_and_unseen(1)

    def _test_too_many_seen(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 4)] * 4), tuple([None if i != 1 else 3 for i in range(16)]))
        p.puzzle_to_draw_on[1][1]._set_seen((True, None, None, None))
        p.puzzle_to_draw_on[2][1]._set_seen((True, None, None, None))
        p.puzzle_to_draw_on[3][1]._set_seen((True, None, None, None))
        with self.assertRaises(UnsolvableError):
            p._mark_puzzle_specific_seen_and_unseen(1)

    def _check_seen_unseen_col_1_row_1_unseen_col_1_rest_seen(self, puzzle_to_draw_on: List[List[CellWithSkyscraper]]):
        for i in range(4):
            for j in range(4):
                if j == 1:
                    if i == 1:
                        self.assertEqual((False, None, None, None), puzzle_to_draw_on[i][j]._seen)
                    elif i == 3:
                        self.assertEqual((True, None, True, None), puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((True, None, None, None), puzzle_to_draw_on[i][j]._seen)
                elif j == 0:
                    if i == 0:
                        self.assertEqual((True, None, None, True), puzzle_to_draw_on[i][j]._seen)
                    elif i == 3:
                        self.assertEqual((None, None, True, True), puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((None, None, None, True), puzzle_to_draw_on[i][j]._seen)
                elif j == 3:
                    if i == 0:
                        self.assertEqual((True, True, None, None), puzzle_to_draw_on[i][j]._seen)
                    elif i == 3:
                        self.assertEqual((None, True, True, None), puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((None, True, None, None), puzzle_to_draw_on[i][j]._seen)
                else:
                    if i == 0:
                        self.assertEqual((True, None, None, None), puzzle_to_draw_on[i][j]._seen)
                    elif i == 3:
                        self.assertEqual((None, None, True, None), puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((None, None, None, None), puzzle_to_draw_on[i][j]._seen)

    def _test_mark_cell_illegals_for_seen(self):
        p = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 8)] * 8), tuple([None] * 32))
        p.puzzle_to_draw_on[2][6].add_illegal_value(1)
        p.puzzle_to_draw_on[2][6].add_illegal_value(2)
        p.puzzle_to_draw_on[2][6].add_illegal_value(3)
        p.puzzle_to_draw_on[2][6].add_illegal_value(4)
        p.puzzle_to_draw_on[2][5]._set_seen((None, True, None, None))
        p._mark_cell_illegals_for_seen_status(10, 2)
        for i in range(8):
            for j in range(8):
                if i == 2 and j == 5:
                    self.assertEqual({1, 2, 3, 4, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif i == 2 and j == 6:
                    self.assertEqual({1, 2, 3, 4}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_cell_illegals_blocking(self):
        p = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 8)] * 8), tuple([None] * 32))
        p.puzzle_to_draw_on[2][6].add_illegal_value(9)
        p.puzzle_to_draw_on[2][6].add_illegal_value(8)
        p.puzzle_to_draw_on[2][6].add_illegal_value(7)
        p.puzzle_to_draw_on[2][6].add_illegal_value(6)
        p.puzzle_to_draw_on[2][6].add_illegal_value(5)
        p.puzzle_to_draw_on[2][6]._set_seen((None, None, None, True))
        p._mark_cell_illegals_for_seen_status(26, 3)
        for i in range(8):
            for j in range(8):
                if i == 2 and j == 3:
                    self.assertEqual({4, 5, 6, 7, 8, 9}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif i == 2 and j == 6:
                    self.assertEqual({5, 6, 7, 8, 9}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_cell_illegals_for_unseen_no_data(self):
        p = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 8)] * 8), tuple([None] * 32))
        p.puzzle_to_draw_on[2][6]._set_seen((None, None, False, None))
        p._mark_cell_illegals_for_seen_status(22, 5)
        for i in range(8):
            for j in range(8):
                if i == 2 and j == 6:
                    self.assertEqual({9}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_cell_illegals_for_unseen(self):
        p = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 8)] * 8), tuple([None] * 32))
        p.puzzle_to_draw_on[1][6].add_illegal_value(9)
        p.puzzle_to_draw_on[1][6].add_illegal_value(8)
        p.puzzle_to_draw_on[0][6].add_illegal_value(9)
        p.puzzle_to_draw_on[2][6]._set_seen((False, None, None, None))
        p._mark_cell_illegals_for_seen_status(6, 2)
        for i in range(8):
            for j in range(8):
                if i == 2 and j == 6:
                    self.assertEqual({8, 9}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif i == 1 and j == 6:
                    self.assertEqual({8, 9}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif i == 0 and j == 6:
                    self.assertEqual({9}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_row_cannot_be_filled(self):
        p = SkyscrapersExtraBuildingPuzzle(((None, None, None, None), (None, None, None, None),
                                            (None, None, None, None), (None, None, None, None)),
                                           tuple([None] * 16))
        p.puzzle_to_draw_on[1][0].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(5)
        p.puzzle_to_draw_on[1][1].add_illegal_value(4)
        p.puzzle_to_draw_on[1][2].add_illegal_value(5)
        p.puzzle_to_draw_on[1][2].add_illegal_value(4)
        p.puzzle_to_draw_on[1][3].add_illegal_value(5)
        p.puzzle_to_draw_on[1][3].add_illegal_value(4)
        self.assertFalse(p._can_cells_be_filled())

    def _test_col_cannot_be_filled(self):
        p = SkyscrapersExtraBuildingPuzzle(((None, None, None, None), (None, None, None, None),
                                            (None, None, None, None), (None, None, None, None)),
                                           tuple([None] * 16))
        p.puzzle_to_draw_on[0][1].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(5)
        p.puzzle_to_draw_on[1][1].add_illegal_value(4)
        p.puzzle_to_draw_on[2][1].add_illegal_value(5)
        p.puzzle_to_draw_on[2][1].add_illegal_value(4)
        p.puzzle_to_draw_on[3][1].add_illegal_value(5)
        p.puzzle_to_draw_on[3][1].add_illegal_value(4)
        self.assertFalse(p._can_cells_be_filled())

    def _test_can_be_filled(self):
        p = SkyscrapersExtraBuildingPuzzle(((None, None, None, None), (None, None, None, None),
                                            (None, None, None, None), (None, None, None, None)),
                                           tuple([None] * 16))

        p.puzzle_to_draw_on[1][0].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(5)
        p.puzzle_to_draw_on[1][2].add_illegal_value(5)
        p.puzzle_to_draw_on[1][3].add_illegal_value(5)
        p.puzzle_to_draw_on[0][1].set_value(1)
        p.puzzle_to_draw_on[1][1].add_illegal_value(5)
        p.puzzle_to_draw_on[2][1].add_illegal_value(5)
        p.puzzle_to_draw_on[3][1].add_illegal_value(5)

        self.assertTrue(p._can_cells_be_filled())

    def _test_unseen_all_sides(self):
        self._test_unseen_from_top()
        self._test_unseen_from_right()
        self._test_unseen_from_bottom()
        self._test_unseen_from_left()

    def _test_non_blocked_all_sides(self):
        self._test_non_blocked_from_top()
        self._test_non_blocked_from_right()
        self._test_non_blocked_from_bottom()
        self._test_non_blocked_from_left()

    def _test_seen_all_sides(self):
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
        p = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 6)] * 6),
                                           tuple([None] * 24))
        p.puzzle_to_draw_on[unseen_row][unseen_col].add_illegal_value(7)
        p.puzzle_to_draw_on[blocking_row][blocking_col].add_illegal_value(5)
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

    def _test_non_blocked(self, hint_index: int, non_blocked_row: int, non_blocked_col: int, non_blocking_row: int,
                          non_blocking_col: int):
        p = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 6)] * 6),
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

    def _test_seen(self, hint_index: int, first_low_row: int, first_low_col: int, second_low_row: int,
                   second_low_col: int, seen_row: int, seen_col: int,
                   seen_cell_tuple: Tuple[Optional[bool], Optional[bool], Optional[bool], Optional[bool]]):
        p = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 6)] * 6),
                                           tuple([None] * 24))
        p.puzzle_to_draw_on[first_low_row][first_low_col].add_illegal_value(7)
        p.puzzle_to_draw_on[second_low_row][second_low_col].add_illegal_value(7)
        p.puzzle_to_draw_on[seen_row][seen_col].add_illegal_value(5)
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


if __name__ == '__main__':
    unittest.main()
