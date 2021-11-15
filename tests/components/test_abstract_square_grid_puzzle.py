import unittest
from unittest.mock import patch

from src.components.abstract_square_grid_puzzle import AbstractSquareGridPuzzle


@patch.object(AbstractSquareGridPuzzle, '__abstractmethods__', set())
class TesAbstractSquareGridPuzzle(unittest.TestCase):

    def test_ctor(self):
        with self.assertRaises(ValueError):
            AbstractSquareGridPuzzle(tuple([tuple([1, 2, None]), tuple([3, None, 2])]))

        puzzle1 = tuple([tuple([None])])
        p1 = AbstractSquareGridPuzzle(puzzle1)
        self.assertEqual(1, p1.num_of_rows)
        self.assertEqual(1, p1.num_of_cols)
        self.assertEqual(puzzle1, p1.puzzle)

        puzzle2 = tuple([tuple([1])])
        p2 = AbstractSquareGridPuzzle(puzzle2)
        self.assertEqual(1, p2.num_of_rows)
        self.assertEqual(1, p2.num_of_cols)
        self.assertEqual(puzzle2, p2.puzzle)

        puzzle3 = tuple([tuple([1, 2, None]), tuple([3, None, 2]), tuple([None, None, None])])
        p3 = AbstractSquareGridPuzzle(puzzle3)
        self.assertEqual(3, p3.num_of_rows)
        self.assertEqual(3, p3.num_of_cols)
        self.assertEqual(puzzle3, p3.puzzle)


if __name__ == '__main__':
    unittest.main()
