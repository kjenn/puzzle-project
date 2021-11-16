import unittest

from src.pachamama_puzzle.pachamama_cell import PachamamaCell
from src.pachamama_puzzle.pachamama_shape import PachamamaShape


class TestPachamamaCell(unittest.TestCase):

    def test_ctor(self):

        with self.assertRaises(ValueError):
            PachamamaCell(0, PachamamaShape.TRIANGLE)

        with self.assertRaises(ValueError):
            PachamamaCell(6, PachamamaShape.CIRCLE)

        p1 = PachamamaCell(1, PachamamaShape.TRIANGLE)
        self.assertEqual(1, p1.number)
        self.assertEqual(PachamamaShape.TRIANGLE, p1.shape)

        p2 = PachamamaCell(5, PachamamaShape.SQUARE)
        self.assertEqual(5, p2.number)
        self.assertEqual(PachamamaShape.SQUARE, p2.shape)


if __name__ == '__main__':
    unittest.main()
