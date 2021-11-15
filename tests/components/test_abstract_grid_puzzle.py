import unittest
from unittest.mock import patch

from src.components.abstract_grid_puzzle import AbstractGridPuzzle


@patch.object(AbstractGridPuzzle, '__abstractmethods__', set())
class TesAbstractGridPuzzle(unittest.TestCase):

    def test_ctor(self):

        with self.assertRaises(ValueError):
            AbstractGridPuzzle(None)
        with self.assertRaises(ValueError):
            AbstractGridPuzzle(tuple([]))
        with self.assertRaises(ValueError):
            AbstractGridPuzzle(tuple([tuple([])]))
        with self.assertRaises(ValueError):
            AbstractGridPuzzle(tuple([tuple([1, 2, 3]), tuple([3, 1, 2]), tuple([2])]))

        puzzle1 = tuple([tuple([None])])
        p1 = AbstractGridPuzzle(puzzle1)
        self.assertEqual(1, p1.num_of_rows)
        self.assertEqual(1, p1.num_of_cols)
        self.assertEqual(puzzle1, p1.puzzle)

        puzzle2 = tuple([tuple([1])])
        p2 = AbstractGridPuzzle(puzzle2)
        self.assertEqual(1, p2.num_of_rows)
        self.assertEqual(1, p2.num_of_cols)
        self.assertEqual(puzzle2, p2.puzzle)

        puzzle3 = tuple([tuple([1, 2, None]), tuple([3, None, 2])])
        p3 = AbstractGridPuzzle(puzzle3)
        self.assertEqual(2, p3.num_of_rows)
        self.assertEqual(3, p3.num_of_cols)
        self.assertEqual(puzzle3, p3.puzzle)


if __name__ == '__main__':
    unittest.main()
