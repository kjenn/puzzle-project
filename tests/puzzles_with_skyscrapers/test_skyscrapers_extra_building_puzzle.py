import unittest

from src.components.unsolvable_error import UnsolvableError
from src.puzzles_with_skyscrapers.skyscrapers_extra_building_puzzle import SkyscrapersExtraBuildingPuzzle


class TestSkyscrapersExtraBuildingPuzzle(unittest.TestCase):

    def test_mark_initial_conclusions(self):
        self._test_mark_initial_conclusions_from_top()
        self._test_mark_initial_conclusions_from_right()
        self._test_mark_initial_conclusions_from_bottom()
        self._test_mark_initial_conclusions_from_left()
        
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

    def _test_mark_initial_conclusions_from_top(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 6)] * 6), tuple([None if i != 0 else 4 for i in range(24)]))
        p._mark_initial_conclusions()
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

    def _test_mark_initial_conclusions_from_right(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 6)] * 6), tuple([None if i != 7 else 3 for i in range(24)]))
        p._mark_initial_conclusions()
        for i in range(6):
            for j in range(6):
                if j == 5 and i == 1:
                    self.assertEqual({6, 7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                elif j == 4 and i == 1:
                    self.assertEqual({7}, p.puzzle_to_draw_on[i][j]._illegal_values)
                else:
                    self.assertEqual(set(), p.puzzle_to_draw_on[i][j]._illegal_values)

    def _test_mark_initial_conclusions_from_bottom(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 6)] * 6), tuple([None if i != 14 else 5 for i in range(24)]))
        p._mark_initial_conclusions()
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

    def _test_mark_initial_conclusions_from_left(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 6)] * 6), tuple([None if i != 21 else 2 for i in range(24)]))
        p._mark_initial_conclusions()
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
        self._check_seen_unseen_col_1_row_1_unseen_col_1_rest_seen(p)

    def _test_mark_seen(self):
        p = SkyscrapersExtraBuildingPuzzle(
            tuple([tuple([None] * 4)] * 4), tuple([None if i != 1 else 3 for i in range(16)]))
        p.puzzle_to_draw_on[1][1]._set_seen((False, None, None, None))
        p._mark_puzzle_specific_seen_and_unseen(1)
        self._check_seen_unseen_col_1_row_1_unseen_col_1_rest_seen(p)

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

    def _check_seen_unseen_col_1_row_1_unseen_col_1_rest_seen(self, p):
        for i in range(4):
            for j in range(4):
                if j == 1:
                    if i == 1:
                        self.assertEqual((False, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                    elif i == 3:
                        self.assertEqual((True, None, True, None), p.puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((True, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                elif j == 0:
                    if i == 0:
                        self.assertEqual((True, None, None, True), p.puzzle_to_draw_on[i][j]._seen)
                    elif i == 3:
                        self.assertEqual((None, None, True, True), p.puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((None, None, None, True), p.puzzle_to_draw_on[i][j]._seen)
                elif j == 3:
                    if i == 0:
                        self.assertEqual((True, True, None, None), p.puzzle_to_draw_on[i][j]._seen)
                    elif i == 3:
                        self.assertEqual((None, True, True, None), p.puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((None, True, None, None), p.puzzle_to_draw_on[i][j]._seen)
                else:
                    if i == 0:
                        self.assertEqual((True, None, None, None), p.puzzle_to_draw_on[i][j]._seen)
                    elif i == 3:
                        self.assertEqual((None, None, True, None), p.puzzle_to_draw_on[i][j]._seen)
                    else:
                        self.assertEqual((None, None, None, None), p.puzzle_to_draw_on[i][j]._seen)

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


if __name__ == '__main__':
    unittest.main()
