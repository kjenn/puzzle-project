import unittest

from src.puzzles_with_skyscrapers.components import hint_for_puzzle_with_skyscrapers


class TestHintForPuzzleWithSkyscrapers(unittest.TestCase):

    def test_get_hint_side(self):
        for i in range(8):
            self.assertEqual(0, hint_for_puzzle_with_skyscrapers.get_hint_side(i, 8))
        for i in range(8, 16):
            self.assertEqual(1, hint_for_puzzle_with_skyscrapers.get_hint_side(i, 8))
        for i in range(16, 24):
            self.assertEqual(2, hint_for_puzzle_with_skyscrapers.get_hint_side(i, 8))
        for i in range(24, 32):
            self.assertEqual(3, hint_for_puzzle_with_skyscrapers.get_hint_side(i, 8))

    def test_validate_hint_index(self):
        for i in range(32):
            hint_for_puzzle_with_skyscrapers.validate_hint_index(i, 8)
        with self.assertRaises(ValueError):
            hint_for_puzzle_with_skyscrapers.validate_hint_index(-1, 8)
        with self.assertRaises(ValueError):
            hint_for_puzzle_with_skyscrapers.validate_hint_index(32, 8)
        with self.assertRaises(ValueError):
            hint_for_puzzle_with_skyscrapers.validate_hint_index(40, 8)


if __name__ == '__main__':
    unittest.main()