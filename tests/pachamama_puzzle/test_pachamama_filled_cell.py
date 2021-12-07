import unittest

from src.pachamama_puzzle.pachamama_filled_cell import PachamamaFilledCell
from src.pachamama_puzzle.pachamama_shape import PachamamaShape


class TestPachamamaFilledCell(unittest.TestCase):

    def test_ctor(self):

        with self.assertRaises(ValueError):
            PachamamaFilledCell(0, PachamamaShape.TRIANGLE)

        with self.assertRaises(ValueError):
            PachamamaFilledCell(None, PachamamaShape.TRIANGLE)

        with self.assertRaises(ValueError):
            PachamamaFilledCell(4, None)

        with self.assertRaises(ValueError):
            PachamamaFilledCell(None, None)


if __name__ == '__main__':
    unittest.main()
