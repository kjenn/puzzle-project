import unittest

from src.pachamama_puzzle.pachamama_cell import PachamamaCell
from src.pachamama_puzzle.pachamama_filled_cell import PachamamaFilledCell
from src.pachamama_puzzle.pachamama_region import PachamamaRegion
from src.pachamama_puzzle.pachamama_shape import PachamamaShape


class TestPachamamaRegion(unittest.TestCase):

    def test_add_cell(self):
        r = PachamamaRegion(PachamamaShape.SQUARE)
        self.assertEqual(set(), r.cell_indices)
        self.assertEqual(PachamamaShape.SQUARE, r.shape)
        r.add_cell((1, 3))
        r.add_cell((2, 3))
        self.assertEqual({(1, 3), (2, 3)}, r.cell_indices)
        self.assertEqual(PachamamaShape.SQUARE, r.shape)


if __name__ == '__main__':
    unittest.main()
