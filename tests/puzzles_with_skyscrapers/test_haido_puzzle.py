import unittest

from src.puzzles_with_skyscrapers.haido_puzzle import HaidoPuzzle


class TestHaidoPuzzle(unittest.TestCase):

    def test_flow(self):
        self._test_flow_solvable_no_values()
        self._test_flow_solvable_values_and_hints()
        self._test_flow_solvable_no_hints()
        self._test_flow_unsolvable_no_hints()
        self._test_flow_unsolvable_no_values()
        self._test_flow_unsolvable_no_values_simple()
        self._test_flow_unsolvable_values_and_hints()
        self._test_flow_unsolvable_values_and_hints_simple()
        self._test_flow_several_solutions_no_hints_no_values()
        self._test_flow_several_solutions_no_hints()
        self._test_flow_several_solutions_no_values()
        self._test_flow_several_solutions_values_and_hints()

    def test_are_puzzle_specifics_valid(self):
        p1 = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                         tuple([None if i not in {0, 8} else 3 for i in range(16)]))
        self.assertFalse(p1._are_puzzle_specifics_valid())

        p2 = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                         tuple([None if i not in {4, 12} else 3 for i in range(16)]))
        self.assertFalse(p2._are_puzzle_specifics_valid())

        p3 = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                         tuple([None if i not in {0, 4, 9, 13} else 3 for i in range(16)]))
        self.assertTrue(p3._are_puzzle_specifics_valid())

        p4 = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                         tuple([None if i not in {2, 6} else 3 for i in range(8)]
                               + [None if i not in {2, 6} else 2 for i in range(8)]))
        self.assertTrue(p4._are_puzzle_specifics_valid())

        p5 = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                         tuple([None if i not in {0, 4, 8, 12} else 2 for i in range(16)]))
        self.assertFalse(p5._are_puzzle_specifics_valid())

    def test_mark_basic_conclusions(self):
        self._test_mark_basic_conclusions_from_top()
        self._test_mark_basic_conclusions_from_right()
        self._test_mark_basic_conclusions_from_bottom()
        self._test_mark_basic_conclusions_from_left()

    def test_mark_puzzle_specific_seen_and_unseen(self):
        self._test_mark_seen()
        self._test_do_not_mark_seen()

    def test_mark_cell_illegals_for_seen_status(self):
        p1 = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                         tuple([None if i != 5 else 2 for i in range(16)]))
        p1.puzzle_to_draw_on[1][2]._set_seen((None, True, None, None))
        p1._mark_cell_illegals_for_seen_status(5, 1)
        self.assertEqual(set(), p1.puzzle_to_draw_on[1][2]._illegal_values)

        p2 = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                         tuple([None if i != 5 else 2 for i in range(16)]))
        p2.puzzle_to_draw_on[1][2]._set_seen((None, False, None, None))
        p2._mark_cell_illegals_for_seen_status(5, 1)
        self.assertEqual({2, 4}, p2.puzzle_to_draw_on[1][2]._illegal_values)

    def test_mark_puzzle_specific_rules(self):
        p = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                        tuple([None if i != 10 else 2 for i in range(16)]))
        p._mark_puzzle_specific_rules()
        for i in range(4):
            for j in range(4):
                if j == 2:
                    if i == 3:
                        self.assertEqual({3, 4}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    else:
                        self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_flow_solvable_no_values(self):
        p = HaidoPuzzle(tuple([tuple([None] * 6)] * 6),
                        (2, 3, None, None, 5, 3,
                         None, None, 2, 2, None, None,
                         4, None, 4, 5, 3, 4,
                         2, None, None, None, 2, 3))
        sol = p.solve()
        self.assertEqual([[2, 1, 6, 4, 5, 3],
                          [5, 3, 1, 2, 4, 6],
                          [6, 4, 5, 3, 2, 1],
                          [4, 5, 3, 1, 6, 2],
                          [1, 2, 4, 6, 3, 5],
                          [3, 6, 2, 5, 1, 4]],
                         sol)

    def _test_flow_solvable_values_and_hints(self):
        p = HaidoPuzzle((tuple([None] * 6),
                         tuple([None] * 6),
                         tuple([None] * 6),
                         (None, None, None, None, None, 2),
                         tuple([None] * 6),
                         tuple([None] * 6)),
                        (2, 3, None, None, 5, 3,
                         None, None, 2, None, None, None,
                         4, None, 4, 5, 3, 4,
                         2, None, None, None, 2, 3))
        sol = p.solve()
        self.assertEqual([[2, 1, 6, 4, 5, 3],
                          [5, 3, 1, 2, 4, 6],
                          [6, 4, 5, 3, 2, 1],
                          [4, 5, 3, 1, 6, 2],
                          [1, 2, 4, 6, 3, 5],
                          [3, 6, 2, 5, 1, 4]],
                         sol)

    def _test_flow_solvable_no_hints(self):
        p = HaidoPuzzle(((1, 2, 3, 4, 5, None),
                         (2, 3, 4, 5, None, None),
                         (3, 4, 5, None, None, None),
                         (4, 5, None, None, None, None),
                         (5, None, None, None, None, None),
                         (None, None, None, None, None, None)),
                        tuple([None] * 24))
        sol = p.solve()
        self.assertEqual([[1, 2, 3, 4, 5, 6],
                          [2, 3, 4, 5, 6, 1],
                          [3, 4, 5, 6, 1, 2],
                          [4, 5, 6, 1, 2, 3],
                          [5, 6, 1, 2, 3, 4],
                          [6, 1, 2, 3, 4, 5]],
                         sol)

    def _test_flow_unsolvable_no_hints(self):
        p = HaidoPuzzle(((1, None, None, None, None, None),
                         (None, 1, None, None, None, None),
                         (None, None, 1, None, None, None),
                         (None, None, None, 1, None, None),
                         (None, None, None, None, 2, 3),
                         (None, None, None, None, 3, 2)),
                        tuple([None] * 24))
        sol = p.solve()
        self.assertEqual(None, sol)

    def _test_flow_unsolvable_no_values(self):
        p = HaidoPuzzle(tuple([tuple([None] * 6)] * 6),
                        (2, 3, None, 5, 5, 3,
                         None, None, 2, 2, None, None,
                         4, None, 4, 5, 3, 4,
                         2, None, None, None, 2, 3))
        sol = p.solve()
        self.assertEqual(None, sol)

    def _test_flow_unsolvable_no_values_simple(self):
        p1 = HaidoPuzzle(tuple([tuple([None] * 6)] * 6),
                         (None, None, None, None, None, None,
                          None, None, None, None, None, None,
                          1, None, None, None, None, None,
                          None, 1, None, None, None, None))
        sol1 = p1.solve()
        self.assertEqual(None, sol1)

        p2 = HaidoPuzzle(tuple([tuple([None] * 6)] * 6),
                         (None, None, None, None, None, None,
                          None, None, None, None, None, None,
                          1, None, None, None, 1, None,
                          None, None, None, None, None, None))
        sol2 = p2.solve()
        self.assertEqual(None, sol2)

        p3 = HaidoPuzzle(tuple([tuple([None] * 6)] * 6),
                         (None, None, None, None, None, None,
                          None, None, None, None, None, None,
                          2, 2, None, None, None, None,
                          None, None, None, 2, None, None))
        sol3 = p3.solve()
        self.assertEqual(None, sol3)

    def _test_flow_unsolvable_values_and_hints(self):
        p = HaidoPuzzle((tuple([None] * 6),
                         tuple([None] * 6),
                         tuple([None] * 6),
                         (None, None, 5, None, None, None),
                         tuple([None] * 6),
                         tuple([None] * 6)),
                        (2, 3, None, None, 5, 3,
                         None, None, 2, 2, None, None,
                         4, None, 4, 5, 3, 4,
                         2, None, None, None, 2, 3))
        sol = p.solve()
        self.assertEqual(None, sol)

    def _test_flow_unsolvable_values_and_hints_simple(self):
        p = HaidoPuzzle((tuple([None] * 6),
                         tuple([None] * 6),
                         tuple([None] * 6),
                         (4, None, None, None, None, None),
                         tuple([None] * 6),
                         tuple([None] * 6)),
                        (None, None, None, None, None, None,
                         None, None, None, None, None, None,
                         None, None, None, None, None, None,
                         None, None, None, 3, None, None))
        sol = p.solve()
        self.assertEqual(None, sol)

    def _test_flow_several_solutions_no_hints_no_values(self):
        p = HaidoPuzzle(tuple([tuple([None] * 6)] * 6),
                        tuple([None] * 24))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))

    def _test_flow_several_solutions_no_hints(self):
        p = HaidoPuzzle(((1, 2, 3, 4, None, None),
                         (2, 3, 4, 1, None, None),
                         (3, 4, 5, 6, 1, 2),
                         (4, 1, 6, 5, 2, 3),
                         (5, 6, 1, 2, 3, 4),
                         (6, 5, 2, 3, 4, 1)),
                        tuple([None] * 24))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))
        self.assertEqual(2, len(sol))
        self.assertIn(
            [[1, 2, 3, 4, 5, 6],
             [2, 3, 4, 1, 6, 5],
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
        p = HaidoPuzzle(tuple([tuple([None] * 6)] * 6),
                        (None, 3, None, None, 5, 3,
                         None, None, 2, 2, None, None,
                         4, None, 4, 5, 3, 4,
                         2, None, None, None, 2, 3))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))

    def _test_flow_several_solutions_values_and_hints(self):
        p = HaidoPuzzle((tuple([None] * 6),
                         tuple([None] * 6),
                         tuple([None] * 6),
                         (None, None, None, None, None, 2),
                         tuple([None] * 6),
                         tuple([None] * 6)),
                        (None, 3, None, None, 5, 3,
                         None, None, 2, None, None, None,
                         4, None, 4, 5, 3, 4,
                         2, None, None, None, 2, 3))
        sol = p.solve()
        self.assertTrue(isinstance(sol, tuple))

    def _test_mark_basic_conclusions_from_top(self):
        p = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                        tuple([None if i != 1 else 2 for i in range(16)]))
        p._mark_basic_conclusions()
        for i in range(4):
            for j in range(4):
                if j == 1:
                    if i == 0:
                        self.assertEqual({3, 4}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    elif i > 1:
                        self.assertEqual({2}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    else:
                        self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_right(self):
        p = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                        tuple([None if i != 4 else 1 for i in range(16)]))
        p._mark_basic_conclusions()
        for i in range(4):
            for j in range(4):
                if i == 0:
                    if j == 3:
                        self.assertEqual(1, p.puzzle_to_draw_on[i][j]._value)
                    else:
                        self.assertEqual({1}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_bottom(self):
        p = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                        tuple([None if i != 10 else 3 for i in range(16)]))
        p._mark_basic_conclusions()
        for i in range(4):
            for j in range(4):
                if j == 2:
                    if i == 0:
                        self.assertEqual({3}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    elif i == 3:
                        self.assertEqual({4}, p.puzzle_to_draw_on[i][j]._illegal_values)
                    else:
                        self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_basic_conclusions_from_left(self):
        p = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                        tuple([None if i != 15 else 4 for i in range(16)]))
        p._mark_basic_conclusions()
        for i in range(4):
            for j in range(4):
                self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_seen(self):
        p = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                        tuple([None if i != 1 else 2 for i in range(16)]))
        p.puzzle_to_draw_on[1][1].set_value(2)
        p._mark_puzzle_specific_seen_and_unseen(1)
        for i in range(4):
            for j in range(4):
                if i == 1 and j == 1:
                    self.assertEqual((True, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                elif i == 0:
                    if j == 0:
                        self.assertEqual((True, None, None, True), p.puzzle_to_draw_on[i][j]._seen)
                    elif j == 3:
                        self.assertEqual((True, True, None, None), p.puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((True, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                elif i == 3:
                    if j == 0:
                        self.assertEqual((None, None, True, True), p.puzzle_to_draw_on[i][j]._seen)
                    elif j == 3:
                        self.assertEqual((None, True, True, None), p.puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((None, None, True, None), p.puzzle_to_draw_on[i][j]._seen)
                else:
                    if j == 0:
                        self.assertEqual((None, None, None, True), p.puzzle_to_draw_on[i][j]._seen)
                    elif j == 3:
                        self.assertEqual((None, True, None, None), p.puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((None, None, None, None), p.puzzle_to_draw_on[i][j]._seen)

    def _test_do_not_mark_seen(self):
        p = HaidoPuzzle(tuple([tuple([None] * 4)] * 4),
                        tuple([None if i != 1 else 2 for i in range(16)]))
        p.puzzle_to_draw_on[1][1].set_value(3)
        p._mark_puzzle_specific_seen_and_unseen(1)
        for i in range(4):
            for j in range(4):
                if i == 0:
                    if j == 0:
                        self.assertEqual((True, None, None, True), p.puzzle_to_draw_on[i][j]._seen)
                    elif j == 3:
                        self.assertEqual((True, True, None, None), p.puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((True, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                elif i == 3:
                    if j == 0:
                        self.assertEqual((None, None, True, True), p.puzzle_to_draw_on[i][j]._seen)
                    elif j == 3:
                        self.assertEqual((None, True, True, None), p.puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((None, None, True, None), p.puzzle_to_draw_on[i][j]._seen)
                else:
                    if j == 0:
                        self.assertEqual((None, None, None, True), p.puzzle_to_draw_on[i][j]._seen)
                    elif j == 3:
                        self.assertEqual((None, True, None, None), p.puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((None, None, None, None), p.puzzle_to_draw_on[i][j]._seen)


if __name__ == '__main__':
    unittest.main()
