import unittest

from src.components.unsolvable_error import UnsolvableError
from src.puzzles_with_skyscrapers.components.cell_with_skyscraper import CellWithSkyscraper


class TestCellWithSkyscraper(unittest.TestCase):

    def test_ctor(self):
        self._test_ctor_val_out_of_range()
        self._test_ctor_seen_wrong_length()
        self._test_ctor_seen_contradicts_val()
        self._test_ctor_highest_val()
        self._test_ctor_without_extra_params()
        self._test_ctor_with_value_param()
        self._test_ctor_with_seen_param()
        self._test_ctor_with_can_be_empty_param()
        self._test_ctor_with_all_params()

    def test_get_possible_values(self):
        self._test_get_possible_values_after_set_value()
        self._test_get_possible_values_after_value_in_ctor()
        self._test_get_possible_values_after_illegals()
        self._test_get_possible_values_after_illegals_and_set_value()

    def test_set_value(self):
        self._test_set_value_out_of_range()
        self._test_set_value_empty_when_not_allowed()
        self._test_set_value_out_of_range_and_contradicting_ctor()
        self._test_set_value_contradicting_ctor()
        self._test_set_value_contradicting_prev_set()
        self._test_set_value_contradicting_illegal()
        self._test_set_value_highest()
        self._test_set_value_empty()
        self._test_set_value_legit()

    def test_add_illegal(self):
        self._test_add_illegal_which_is_value_from_ctor()
        self._test_add_illegal_which_is_set_value()
        self._test_add_illegal_which_is_only_legal()
        self._test_add_illegal_out_of_range()
        self._test_add_illegal_legit()
        self._test_add_all_illegal_but_one()
        self._test_add_all_illegal()

    def test_set_seen(self):
        self._test_set_seen_wrong_length()
        self._test_set_seen_run_over_existing_from_ctor()
        self._test_set_seen_run_over_existing()
        self._test_set_seen_false_for_highest()
        self._test_set_seen_legit()
        self._test_set_seen_with_true_and_possible_empty()

    def test_set_seen_from_side(self):
        self._test_set_seen_from_side_bad_index()
        self._test_set_seen_from_side_run_over_existing_value_from_ctor()
        self._test_set_seen_from_side_run_over_existing_value_from_set()
        self._test_set_seen_from_side_false_for_highest()
        self._test_set_seen_from_side_legit()

    def test_get_seen_from_side(self):
        self._test_get_seen_from_side_bad_index()
        self._test_get_seen_from_side_highest()
        self._test_get_seen_from_side_legit()

    def _test_ctor_val_out_of_range(self):
        with self.assertRaises(ValueError):
            CellWithSkyscraper(6, 7)
        with self.assertRaises(ValueError):
            CellWithSkyscraper(6, 0)

    def _test_ctor_seen_wrong_length(self):
        with self.assertRaises(ValueError):
            CellWithSkyscraper(6, None, (True, False, True))
        with self.assertRaises(ValueError):
            CellWithSkyscraper(6, None, (True, False, True, None, None))
        with self.assertRaises(ValueError):
            CellWithSkyscraper(6, None, True)
        with self.assertRaises(ValueError):
            CellWithSkyscraper(6, None, None)

    def _test_ctor_seen_contradicts_val(self):
        with self.assertRaises(UnsolvableError):
            CellWithSkyscraper(6, 6, (False, None, None, None))
        with self.assertRaises(UnsolvableError):
            CellWithSkyscraper(6, 0, (True, None, None, None), can_be_empty=True)

    def _test_ctor_highest_val(self):
        c = CellWithSkyscraper(6, 6, (None, True, None, None))
        self.assertEqual(6, c._value)
        self.assertEqual({1, 2, 3, 4, 5}, c._illegal_values)
        self.assertEqual((True, True, True, True), c._seen)
        self.assertEqual(6, c.highest_possible_value)
        self.assertEqual(1, c.lowest_possible_value)
        self.assertFalse(c.can_be_empty)

    def _test_ctor_empty_val(self):
        c = CellWithSkyscraper(6, 0, (None, False, None, None), can_be_empty=True)
        self.assertEqual(0, c._value)
        self.assertEqual({1, 2, 3, 4, 5, 6}, c._illegal_values)
        self.assertEqual((False, False, False, False), c._seen)
        self.assertEqual(6, c.highest_possible_value)
        self.assertEqual(0, c.lowest_possible_value)
        self.assertTrue(c.can_be_empty)

    def _test_ctor_without_extra_params(self):
        c = CellWithSkyscraper(6)
        self.assertEqual(None, c._value)
        self.assertEqual(set(), c._illegal_values)
        self.assertEqual((None, None, None, None), c._seen)
        self.assertEqual(6, c.highest_possible_value)
        self.assertEqual(1, c.lowest_possible_value)
        self.assertFalse(c.can_be_empty)

    def _test_ctor_with_value_param(self):
        c = CellWithSkyscraper(6, 1)
        self.assertEqual(1, c._value)
        self.assertEqual({2, 3, 4, 5, 6}, c._illegal_values)
        self.assertEqual((None, None, None, None), c._seen)
        self.assertEqual(6, c.highest_possible_value)
        self.assertEqual(1, c.lowest_possible_value)
        self.assertFalse(c.can_be_empty)

    def _test_ctor_with_seen_param(self):
        c = CellWithSkyscraper(6, None, (True, None, False, None))
        self.assertEqual(None, c._value)
        self.assertEqual({6}, c._illegal_values)
        self.assertEqual((True, None, False, None), c._seen)
        self.assertEqual(6, c.highest_possible_value)
        self.assertEqual(1, c.lowest_possible_value)
        self.assertFalse(c.can_be_empty)

    def _test_ctor_with_can_be_empty_param(self):
        c = CellWithSkyscraper(6, can_be_empty=True)
        self.assertEqual(None, c._value)
        self.assertEqual(set(), c._illegal_values)
        self.assertEqual((None, None, None, None), c._seen)
        self.assertEqual(6, c.highest_possible_value)
        self.assertEqual(0, c.lowest_possible_value)
        self.assertTrue(c.can_be_empty)

    def _test_ctor_with_all_params(self):
        c = CellWithSkyscraper(6, 4, (None, True, False, None), can_be_empty=True)
        self.assertEqual(4, c._value)
        self.assertEqual({0, 1, 2, 3, 5, 6}, c._illegal_values)
        self.assertEqual((None, True, False, None), c._seen)
        self.assertEqual(6, c.highest_possible_value)
        self.assertEqual(0, c.lowest_possible_value)
        self.assertTrue(c.can_be_empty)

    def _test_get_possible_values_after_set_value(self):
        c1 = CellWithSkyscraper(6)
        c1.set_value(4)
        self.assertEqual({4}, c1.get_possible_values())

        c2 = CellWithSkyscraper(6, can_be_empty=True)
        c2.set_value(0)
        self.assertEqual({0}, c2.get_possible_values())

    def _test_get_possible_values_after_value_in_ctor(self):
        c1 = CellWithSkyscraper(6, 3)
        self.assertEqual({3}, c1.get_possible_values())

        c2 = CellWithSkyscraper(6, 0, can_be_empty=True)
        self.assertEqual({0}, c2.get_possible_values())

    def _test_get_possible_values_after_illegals(self):
        c1 = CellWithSkyscraper(6)
        c1.add_illegal_value(1)
        c1.add_illegal_value(6)
        self.assertEqual({2, 3, 4, 5}, c1.get_possible_values())

        c2 = CellWithSkyscraper(6, can_be_empty=True)
        c2.add_illegal_value(1)
        c2.add_illegal_value(6)
        self.assertEqual({0, 2, 3, 4, 5}, c2.get_possible_values())

    def _test_get_possible_values_after_illegals_and_set_value(self):
        c1 = CellWithSkyscraper(6)
        c1.add_illegal_value(1)
        c1.add_illegal_value(6)
        c1.set_value(2)
        self.assertEqual({2}, c1.get_possible_values())

        c2 = CellWithSkyscraper(6, can_be_empty=True)
        c2.add_illegal_value(1)
        c2.add_illegal_value(6)
        c2.set_value(2)
        self.assertEqual({2}, c2.get_possible_values())

    def _test_set_value_out_of_range(self):
        c = CellWithSkyscraper(6)
        with self.assertRaises(ValueError):
            c.set_value(7)

    def _test_set_value_empty_when_not_allowed(self):
        c = CellWithSkyscraper(6)
        with self.assertRaises(ValueError):
            c.set_value(0)

    def _test_set_value_out_of_range_and_contradicting_ctor(self):
        c = CellWithSkyscraper(6, 4)
        with self.assertRaises(ValueError):
            c.set_value(7)

    def _test_set_value_contradicting_ctor(self):
        c = CellWithSkyscraper(6, 4)
        with self.assertRaises(UnsolvableError):
            c.set_value(3)

    def _test_set_value_contradicting_prev_set(self):
        c = CellWithSkyscraper(6)
        c.set_value(5)
        with self.assertRaises(UnsolvableError):
            c.set_value(3)

    def _test_set_value_contradicting_illegal(self):
        c = CellWithSkyscraper(6)
        c.add_illegal_value(5)
        with self.assertRaises(UnsolvableError):
            c.set_value(5)

    def _test_set_value_highest(self):
        c = CellWithSkyscraper(6, can_be_empty=True)
        c.set_value(6)
        self.assertEqual((True, True, True, True), c._seen)

    def _test_set_value_empty(self):
        c = CellWithSkyscraper(6, can_be_empty=True)
        c.set_value(0)
        self.assertEqual((False, False, False, False), c._seen)

    def _test_set_value_legit(self):
        c = CellWithSkyscraper(6, can_be_empty=True)
        c.set_value(5)
        self.assertEqual(5, c._value)
        self.assertEqual({5}, c.get_possible_values())
        self.assertEqual({0, 1, 2, 3, 4, 6}, c._illegal_values)

    def _test_add_illegal_which_is_value_from_ctor(self):
        c = CellWithSkyscraper(6, 3)
        with self.assertRaises(UnsolvableError):
            c.add_illegal_value(3)

    def _test_add_illegal_which_is_set_value(self):
        c = CellWithSkyscraper(6)
        c.set_value(1)
        with self.assertRaises(UnsolvableError):
            c.add_illegal_value(1)

    def _test_add_illegal_which_is_only_legal(self):
        c = CellWithSkyscraper(6)
        for i in range(1, 6):
            c.add_illegal_value(i)
        with self.assertRaises(UnsolvableError):
            c.add_illegal_value(6)

    def _test_add_illegal_out_of_range(self):
        c1 = CellWithSkyscraper(6)
        with self.assertRaises(ValueError):
            c1.add_illegal_value(7)

        c1 = CellWithSkyscraper(6)
        with self.assertRaises(ValueError):
            c1.add_illegal_value(0)

    def _test_add_illegal_legit(self):
        c = CellWithSkyscraper(6)
        c.add_illegal_value(1)
        self.assertEqual({2, 3, 4, 5, 6}, c.get_possible_values())
        self.assertEqual({1}, c._illegal_values)
        self.assertEqual(None, c._value)

    def _test_add_all_illegal_but_one(self):
        c1 = CellWithSkyscraper(6)
        for i in range(1, 6):
            c1.add_illegal_value(i)
        self.assertEqual({6}, c1.get_possible_values())
        self.assertEqual({1, 2, 3, 4, 5}, c1._illegal_values)
        self.assertEqual(6, c1._value)
        self.assertEqual((True, True, True, True), c1._seen)

        c2 = CellWithSkyscraper(6, can_be_empty=True)
        for i in range(1, 7):
            c2.add_illegal_value(i)
        self.assertEqual({0}, c2.get_possible_values())
        self.assertEqual({1, 2, 3, 4, 5, 6}, c2._illegal_values)
        self.assertEqual(0, c2._value)
        self.assertEqual((False, False, False, False), c2._seen)

        c3 = CellWithSkyscraper(6, can_be_empty=True)
        for i in range(6):
            c3.add_illegal_value(i)
        self.assertEqual({6}, c3.get_possible_values())
        self.assertEqual({0, 1, 2, 3, 4, 5}, c3._illegal_values)
        self.assertEqual(6, c3._value)
        self.assertEqual((True, True, True, True), c3._seen)

    def _test_add_all_illegal(self):
        c1 = CellWithSkyscraper(6, can_be_empty=True)
        with self.assertRaises(UnsolvableError):
            for i in range(7):
                c1.add_illegal_value(i)

    def _test_set_seen_wrong_length(self):
        c = CellWithSkyscraper(6)
        with self.assertRaises(ValueError):
            c._set_seen(True)
        with self.assertRaises(ValueError):
            c._set_seen(None)
        with self.assertRaises(ValueError):
            c._set_seen((True, None, False))
        with self.assertRaises(ValueError):
            c._set_seen((True, None, False, False, False))

    def _test_set_seen_run_over_existing_from_ctor(self):
        c = CellWithSkyscraper(6, None, (True, None, None, None))
        with self.assertRaises(UnsolvableError):
            c._set_seen((False, None, None, None))

    def _test_set_seen_run_over_existing(self):
        c = CellWithSkyscraper(6)
        c._set_seen((True, None, True, None))
        with self.assertRaises(UnsolvableError):
            c._set_seen((None, False, False, None))

    def _test_set_seen_false_for_highest(self):
        c = CellWithSkyscraper(6, 6)
        with self.assertRaises(UnsolvableError):
            c._set_seen((None, False, None, None))

    def _test_set_seen_legit(self):
        c = CellWithSkyscraper(6)
        c._set_seen((True, None, False, None))
        self.assertEqual((True, None, False, None), c._seen)
        c._set_seen((True, None, None, False))
        self.assertEqual((True, None, False, False), c._seen)

    def _test_set_seen_with_true_and_possible_empty(self):
        c = CellWithSkyscraper(6, can_be_empty=True)
        c._set_seen((True, None, False, None))
        self.assertEqual((True, None, False, None), c._seen)
        self.assertEqual({0, 6}, c._illegal_values)

    def _test_set_seen_from_side_bad_index(self):
        c = CellWithSkyscraper(6)
        with self.assertRaises(ValueError):
            c.set_seen_from_side(4, True)

    def _test_set_seen_from_side_run_over_existing_value_from_ctor(self):
        c = CellWithSkyscraper(6, None, (False, False, False, False))
        with self.assertRaises(UnsolvableError):
            c.set_seen_from_side(0, True)

    def _test_set_seen_from_side_run_over_existing_value_from_set(self):
        c = CellWithSkyscraper(6)
        c._set_seen((None, True, None, None))
        with self.assertRaises(UnsolvableError):
            c.set_seen_from_side(1, False)

    def _test_set_seen_from_side_false_for_highest(self):
        c = CellWithSkyscraper(6, 6)
        with self.assertRaises(UnsolvableError):
            c.set_seen_from_side(1, False)

    def _test_set_seen_from_side_legit(self):
        c = CellWithSkyscraper(6)
        c.set_seen_from_side(0, True)
        self.assertEqual((True, None, None, None), c._seen)
        c.set_seen_from_side(3, False)
        self.assertEqual((True, None, None, False), c._seen)

    def _test_get_seen_from_side_bad_index(self):
        c = CellWithSkyscraper(6)
        with self.assertRaises(ValueError):
            c.get_seen_from_side(4)

    def _test_get_seen_from_side_highest(self):
        c = CellWithSkyscraper(6, 6)
        self.assertEqual(True, c.get_seen_from_side(1))

    def _test_get_seen_from_side_legit(self):
        c = CellWithSkyscraper(6, None, (True, None, None, False))
        self.assertEqual(True, c.get_seen_from_side(0))
        self.assertEqual(None, c.get_seen_from_side(1))
        self.assertEqual(False, c.get_seen_from_side(3))


if __name__ == '__main__':
    unittest.main()
