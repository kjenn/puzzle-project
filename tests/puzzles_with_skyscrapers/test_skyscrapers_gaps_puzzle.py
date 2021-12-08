import unittest

from src.components.unsolvable_error import UnsolvableError
from src.puzzles_with_skyscrapers.skyscrapers_gaps_puzzle import SkyscrapersGapsPuzzle


class TestSkyscrapersGapsPuzzle(unittest.TestCase):

    def test_flow(self):
        self._test_flow_solvable_no_hints()
        self._test_flow_solvable_no_values()
        self._test_flow_solvable_hint_and_values()
        self._test_flow_unsolvable_no_hints()
        self._test_flow_unsolvable_no_values()
        self._test_flow_unsolvable_hints_and_values()
        self._test_flow_several_solutions_no_hints_no_values()
        self._test_flow_several_solutions_no_hints()
        self._test_flow_several_solutions_no_values()
        self._test_flow_several_solutions_hints_and_values()
        self._test_flow_single_solution_more_complex()
        self._test_flow_no_solution_more_complex()
        self._test_flow_several_solutions_more_complex()

    def test_are_puzzle_specifics_valid(self):

        p1 = SkyscrapersGapsPuzzle(tuple([tuple([None] * 4)] * 4),
                                   tuple([None if i not in {0, 8} else 3 for i in range(16)]))
        self.assertFalse(p1._are_puzzle_specifics_valid())

        p2 = SkyscrapersGapsPuzzle(tuple([tuple([None] * 4)] * 4),
                                   tuple([None if i not in {4, 12} else 3 for i in range(16)]))
        self.assertFalse(p2._are_puzzle_specifics_valid())

        p3 = SkyscrapersGapsPuzzle(tuple([tuple([None] * 4)] * 4),
                                   tuple([None if i not in {0, 4, 9, 13} else 3 for i in range(16)]))
        self.assertTrue(p3._are_puzzle_specifics_valid())

        p4 = SkyscrapersGapsPuzzle(tuple([tuple([None] * 4)] * 4),
                                   tuple([None if i not in {2, 6} else 3 for i in range(8)]
                                         + [None if i not in {2, 6} else 2 for i in range(8)]))
        self.assertFalse(p4._are_puzzle_specifics_valid())

        p5 = SkyscrapersGapsPuzzle(tuple([tuple([None] * 4)] * 4),
                                   tuple([None if i not in {0, 4, 8, 12} else 2 for i in range(16)]))
        self.assertTrue(p5._are_puzzle_specifics_valid())

    def test_mark_basic_conclusions(self):
        self._test_mark_basic_conclusions_from_top()
        self._test_mark_basic_conclusions_from_top_generalized()
        self._test_mark_basic_conclusions_from_right()
        self._test_mark_basic_conclusions_from_bottom()
        self._test_mark_basic_conclusions_from_left()
        self._test_mark_basic_conclusions_from_left_generalized()

    def test_mark_puzzle_specific_seen_and_unseen(self):
        self._test_mark_unseen()
        self._test_mark_seen()
        self._test_too_many_unseen()
        self._test_too_many_seen()

    def test_mark_cell_illegals_for_seen_status(self):
        self._test_mark_cell_illegals_for_seen()
        self._test_mark_cell_illegals_for_seen_no_data()
        self._test_mark_cell_illegals_for_seen_no_data_cell_next_to_hint()
        self._test_mark_cell_illegals_blocking()
        self._test_mark_cell_illegals_for_unseen_no_data()
        self._test_mark_cell_illegals_for_unseen()
        self._test_mark_cell_illegals_for_unseen_next_to_hint()

    def _test_flow_solvable_no_hints(self):
        p = SkyscrapersGapsPuzzle(((1, 2, 3, 4, 5, None),
                                   (2, 3, 4, 5, None, None),
                                   (3, 4, 5, None, None, None),
                                   (4, 5, None, None, None, None),
                                   (5, None, None, None, None, None),
                                   (None, None, None, None, None, None)),
                                  tuple([None] * 24))
        sol = p.solve()
        self.assertEqual([[1, 2, 3, 4, 5, 0],
                          [2, 3, 4, 5, 0, 1],
                          [3, 4, 5, 0, 1, 2],
                          [4, 5, 0, 1, 2, 3],
                          [5, 0, 1, 2, 3, 4],
                          [0, 1, 2, 3, 4, 5]],
                         sol)

    def _test_flow_solvable_no_values(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                                  tuple([5, 4, 3, 2, 1, None] + [None] * 17 + [5]))
        sol = p.solve()
        self.assertEqual([[1, 2, 3, 4, 5, 0],
                          [2, 3, 4, 5, 0, 1],
                          [3, 4, 5, 0, 1, 2],
                          [4, 5, 0, 1, 2, 3],
                          [5, 0, 1, 2, 3, 4],
                          [0, 1, 2, 3, 4, 5]],
                         sol)

    def _test_flow_solvable_hint_and_values(self):
        p = SkyscrapersGapsPuzzle(((None, None, None, None, 5, None),
                                   (None, None, None, 5, None, None),
                                   (None, None, 5, None, None, None),
                                   (None, 5, None, None, None, None),
                                   (5, None, None, None, None, None),
                                   (None, None, None, None, None, 5)),
                                  tuple([5, 4, 3, 2, 1, 5] + [None] * 18))
        sol = p.solve()
        self.assertEqual([[1, 2, 3, 4, 5, 0],
                          [2, 3, 4, 5, 0, 1],
                          [3, 4, 5, 0, 1, 2],
                          [4, 5, 0, 1, 2, 3],
                          [5, 0, 1, 2, 3, 4],
                          [0, 1, 2, 3, 4, 5]],
                         sol)

    def _test_flow_unsolvable_no_hints(self):
        p = SkyscrapersGapsPuzzle(((1, None, None, None, None, None),
                                   (None, 1, None, None, None, None),
                                   (None, None, 1, None, None, None),
                                   (None, None, None, 1, None, None),
                                   (None, None, None, None, 2, 3),
                                   (None, None, None, None, 3, 2)),
                                  tuple([None] * 24))
        sol = p.solve()
        self.assertEqual(None, sol)

    def _test_flow_unsolvable_no_values(self):
        p1 = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                                   tuple([5, 5, 5, None, None, None] + [None] * 18))
        sol1 = p1.solve()
        self.assertEqual(None, sol1)

        p2 = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                                   tuple([3, None, None, None, None, None] + [None] * 6
                                         + [4, None, None, None, None, None] + [None] * 6))
        sol2 = p2.solve()
        self.assertEqual(None, sol2)

        p3 = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                                   tuple([1, 1, 1, None, None, None] + [None] * 18))
        sol3 = p3.solve()
        self.assertEqual(None, sol3)

    def _test_flow_unsolvable_hints_and_values(self):
        p = SkyscrapersGapsPuzzle(((4, None, None, None, None, None),
                                   (None, None, None, None, None, None),
                                   (None, None, None, None, None, None),
                                   (None, None, None, None, None, None),
                                   (None, None, None, None, None, None),
                                   (None, None, None, None, None, None)),
                                  tuple([3, None, None, None, None, None] + [None] * 18))
        sol = p.solve()
        self.assertEqual(None, sol)

    def _test_flow_several_solutions_no_hints_no_values(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                                  tuple([None] * 24))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))

    def _test_flow_several_solutions_no_hints(self):
        p = SkyscrapersGapsPuzzle(((1, 2, 3, 4, None, None),
                                   (2, 3, 4, 1, None, None),
                                   (3, 4, 5, 0, 1, 2),
                                   (4, 1, 0, 5, 2, 3),
                                   (5, 0, 1, 2, 3, 4),
                                   (0, 5, 2, 3, 4, 1)),
                                  tuple([None] * 24))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))
        self.assertEqual(2, len(sol))
        self.assertIn(
            [[1, 2, 3, 4, 5, 0],
             [2, 3, 4, 1, 0, 5],
             [3, 4, 5, 0, 1, 2],
             [4, 1, 0, 5, 2, 3],
             [5, 0, 1, 2, 3, 4],
             [0, 5, 2, 3, 4, 1]],
            sol)
        self.assertIn(
            [[1, 2, 3, 4, 0, 5],
             [2, 3, 4, 1, 5, 0],
             [3, 4, 5, 0, 1, 2],
             [4, 1, 0, 5, 2, 3],
             [5, 0, 1, 2, 3, 4],
             [0, 5, 2, 3, 4, 1]],
            sol)

    def _test_flow_several_solutions_no_values(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                                  tuple([None, 5, 4, 3, 2, 1] + [None] * 18))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))

    def _test_flow_several_solutions_hints_and_values(self):
        p = SkyscrapersGapsPuzzle(((None, None, None, None, None, None),
                                   (None, None, None, None, None, None),
                                   (None, None, None, None, None, None),
                                   (None, None, None, None, None, None),
                                   (None, None, None, None, None, None),
                                   (None, None, None, None, 4, None)),
                                  tuple([5, 5, 4, None, None, None] + [None] * 18))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))

    def _test_flow_single_solution_more_complex(self):
        p1 = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                                   (3, None, 1, 4, 1, 5,
                                    None, 3, None, None, None, None,
                                    None, None, None, None, None, None,
                                    None, 3, None, 1, 4, None))
        sol1 = p1.solve()
        self.assertEqual([[3, 4, 0, 2, 5, 1],
                          [1, 3, 5, 0, 4, 2],
                          [4, 5, 2, 1, 0, 3],
                          [5, 0, 1, 3, 2, 4],
                          [0, 2, 3, 4, 1, 5],
                          [2, 1, 4, 5, 3, 0]],
                         sol1)

        p2 = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                                   (4, 3, 2, 2, None, None,
                                    None, 2, 3, None, 3, 2,
                                    None, None, 3, None, None, None,
                                    2, None, 3, 4, None, None))
        sol2 = p2.solve()
        self.assertEqual([[0, 3, 2, 1, 5, 4],
                          [2, 4, 5, 0, 1, 3],
                          [3, 0, 4, 5, 2, 1],
                          [1, 2, 0, 4, 3, 5],
                          [4, 5, 1, 3, 0, 2],
                          [5, 1, 3, 2, 4, 0]],
                         sol2)

        p3 = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                                   (2, None, 1, 3, None, 4,
                                    None, 4, 3, None, None, 2,
                                    None, 2, 3, None, 4, None,
                                    3, 2, None, 4, 2, 3))
        sol3 = p3.solve()
        self.assertEqual([[3, 4, 0, 2, 5, 1],
                          [1, 0, 5, 4, 3, 2],
                          [5, 1, 2, 0, 4, 3],
                          [2, 3, 4, 1, 0, 5],
                          [4, 5, 1, 3, 2, 0],
                          [0, 2, 3, 5, 1, 4]],
                         sol3)

    def _test_flow_no_solution_more_complex(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                                  (3, None, 1, 4, 1, 5,
                                   None, 3, 3, None, None, None,
                                   None, None, None, None, None, None,
                                   None, 3, None, 1, 4, None))
        sol = p.solve()
        self.assertEqual(None, sol)

    def _test_flow_several_solutions_more_complex(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                                  (3, None, 1, 4, None, None,
                                   None, 3, None, None, None, None,
                                   None, None, None, None, None, None,
                                   None, 3, None, 1, 4, None))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))

    def _test_mark_basic_conclusions_from_top(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6), tuple([None if i != 0 else 4 for i in range(24)]))
        p._mark_basic_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 0 and i == 0:
                    self.assertEqual({3, 4, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 1:
                    self.assertEqual({4, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 2:
                    self.assertEqual({5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_top_generalized(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6), tuple([None if i != 0 else 4 for i in range(24)]))
        p.puzzle_to_draw_on[1][0].set_seen_from_side(0, False)
        p.puzzle_to_draw_on[2][0].set_seen_from_side(0, False)
        p._mark_basic_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 0 and i == 0:
                    self.assertEqual({3, 4, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 1:
                    self.assertEqual({3, 4, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 2:
                    self.assertEqual({3, 4, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 3:
                    self.assertEqual({4, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 0 and i == 4:
                    self.assertEqual({5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_right(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6), tuple([None if i != 7 else 3 for i in range(24)]))
        p._mark_basic_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 5 and i == 1:
                    self.assertEqual({4, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 4 and i == 1:
                    self.assertEqual({5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_bottom(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6), tuple([None if i != 14 else 5 for i in range(24)]))
        p._mark_basic_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 2 and i == 5:
                    self.assertEqual({2, 3, 4, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 2 and i == 4:
                    self.assertEqual({3, 4, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 2 and i == 3:
                    self.assertEqual({4, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 2 and i == 2:
                    self.assertEqual({5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_left(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6), tuple([None if i != 21 else 2 for i in range(24)]))
        p._mark_basic_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 0 and i == 3:
                    self.assertEqual({5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_left_generalized(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6), tuple([None if i != 21 else 2 for i in range(24)]))
        p.puzzle_to_draw_on[3][0].add_illegal_value(5)
        p.puzzle_to_draw_on[3][1].add_illegal_value(5)
        p.puzzle_to_draw_on[3][2].add_illegal_value(5)
        p.puzzle_to_draw_on[3][3].add_illegal_value(5)
        p._mark_basic_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 0 and i == 3:
                    self.assertEqual({1, 2, 5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif i == 3 and j in {1, 2, 3}:
                    self.assertEqual({5}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_unseen(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 4)] * 4), tuple([None if i != 1 else 2 for i in range(16)]))
        p.puzzle_to_draw_on[0][1]._set_seen((True, None, None, None))
        p.puzzle_to_draw_on[1][1]._set_seen((True, None, None, None))
        p._mark_puzzle_specific_seen_and_unseen(1)
        for i in range(4):
            for j in range(4):
                if j == 1 and i in {0, 1}:
                    self.assertEqual((True, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                elif j == 1:
                    self.assertEqual((False, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                else:
                    self.assertEqual((None, None, None, None), p.puzzle_to_draw_on[i][j]._seen)

    def _test_mark_seen(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 4)] * 4), tuple([None if i != 1 else 2 for i in range(16)]))
        p.puzzle_to_draw_on[1][1]._set_seen((False, None, None, None))
        p.puzzle_to_draw_on[2][1]._set_seen((False, None, None, None))
        p._mark_puzzle_specific_seen_and_unseen(1)
        for i in range(4):
            for j in range(4):
                if j == 1 and i in {1, 2}:
                    self.assertEqual((False, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                elif j == 1:
                    self.assertEqual((True, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                else:
                    self.assertEqual((None, None, None, None), p.puzzle_to_draw_on[i][j]._seen)

    def _test_too_many_unseen(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 4)] * 4), tuple([None if i != 1 else 3 for i in range(16)]))
        p.puzzle_to_draw_on[1][1]._set_seen((False, None, None, None))
        p.puzzle_to_draw_on[2][1]._set_seen((False, None, None, None))
        with self.assertRaises(UnsolvableError):
            p._mark_puzzle_specific_seen_and_unseen(1)

    def _test_too_many_seen(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 4)] * 4), tuple([None if i != 1 else 2 for i in range(16)]))
        p.puzzle_to_draw_on[1][1]._set_seen((True, None, None, None))
        p.puzzle_to_draw_on[2][1]._set_seen((True, None, None, None))
        p.puzzle_to_draw_on[3][1]._set_seen((True, None, None, None))
        with self.assertRaises(UnsolvableError):
            p._mark_puzzle_specific_seen_and_unseen(1)

    def _test_mark_cell_illegals_for_seen(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 8)] * 8), tuple([None] * 32))
        p.puzzle_to_draw_on[2][6].add_illegal_value(0)
        p.puzzle_to_draw_on[2][6].add_illegal_value(1)
        p.puzzle_to_draw_on[2][6].add_illegal_value(2)
        p.puzzle_to_draw_on[2][6].add_illegal_value(3)
        p.puzzle_to_draw_on[2][5]._set_seen((None, True, None, None))
        p._mark_cell_illegals_for_seen_status(10, 2)
        for i in range(8):
            for j in range(8):
                if i == 2 and j == 5:
                    self.assertEqual({0, 1, 2, 3, 4}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif i == 2 and j == 6:
                    self.assertEqual({0, 1, 2, 3}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_cell_illegals_for_seen_no_data(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 8)] * 8), tuple([None] * 32))
        p.puzzle_to_draw_on[2][6]._set_seen((None, True, None, None))
        p._mark_cell_illegals_for_seen_status(10, 1)
        for i in range(8):
            for j in range(8):
                if i == 2 and j == 6:
                    self.assertEqual({0}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_cell_illegals_for_seen_no_data_cell_next_to_hint(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 8)] * 8), tuple([None] * 32))
        p.puzzle_to_draw_on[2][7]._set_seen((None, True, None, None))
        p._mark_cell_illegals_for_seen_status(10, 0)
        for i in range(8):
            for j in range(8):
                if i == 2 and j == 7:
                    self.assertEqual({0}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_cell_illegals_blocking(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 8)] * 8), tuple([None] * 32))
        p.puzzle_to_draw_on[2][6].add_illegal_value(7)
        p.puzzle_to_draw_on[2][6].add_illegal_value(6)
        p.puzzle_to_draw_on[2][6].add_illegal_value(5)
        p.puzzle_to_draw_on[2][6].add_illegal_value(4)
        p.puzzle_to_draw_on[2][6]._set_seen((None, None, None, True))
        p._mark_cell_illegals_for_seen_status(26, 3)
        for i in range(8):
            for j in range(8):
                if i == 2 and j == 3:
                    self.assertEqual({3, 4, 5, 6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif i == 2 and j == 6:
                    self.assertEqual({0, 4, 5, 6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_cell_illegals_for_unseen_no_data(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 8)] * 8), tuple([None] * 32))
        p.puzzle_to_draw_on[2][6]._set_seen((None, None, False, None))
        p._mark_cell_illegals_for_seen_status(22, 5)
        for i in range(8):
            for j in range(8):
                if i == 2 and j == 6:
                    self.assertEqual({7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_cell_illegals_for_unseen(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 8)] * 8), tuple([None] * 32))
        p.puzzle_to_draw_on[1][6].add_illegal_value(7)
        p.puzzle_to_draw_on[1][6].add_illegal_value(6)
        p.puzzle_to_draw_on[0][6].add_illegal_value(7)
        p.puzzle_to_draw_on[2][6]._set_seen((False, None, None, None))
        p._mark_cell_illegals_for_seen_status(6, 2)
        for i in range(8):
            for j in range(8):
                if i == 2 and j == 6:
                    self.assertEqual({6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif i == 1 and j == 6:
                    self.assertEqual({6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif i == 0 and j == 6:
                    self.assertEqual({7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_cell_illegals_for_unseen_next_to_hint(self):
        p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 8)] * 8), tuple([None] * 32))
        p.puzzle_to_draw_on[0][1]._set_seen((False, None, None, None))
        p._mark_cell_illegals_for_seen_status(1, 0)
        for i in range(8):
            for j in range(8):
                if i == 0 and j == 1:
                    self.assertEqual(0, p.puzzle_to_draw_on[i][j]._value)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)


if __name__ == '__main__':
    unittest.main()

