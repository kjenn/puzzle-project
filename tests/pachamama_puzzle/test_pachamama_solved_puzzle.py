import unittest

from src.pachamama_puzzle.pachamama_cell import PachamamaCell
from src.pachamama_puzzle.pachamama_filled_cell import PachamamaFilledCell
from src.pachamama_puzzle.pachamama_shape import PachamamaShape
from src.pachamama_puzzle.pachamama_solved_puzzle import PachamamaSolvedPuzzle
from tests.pachamama_puzzle.pachamama_test_utils import get_complex_legal_solution, create_region


class TestPachamamaSolvedPuzzle(unittest.TestCase):

    def test_is_legal(self):
        self._test_is_legal_wrong_cell_type()
        self._test_is_legal_large_region()
        self._test_is_legal_region_with_repeats()
        self._test_is_legal_region_missing_number()
        self._test_is_legal_regions_touching()
        self._test_is_legal_numbers_touching()
        self._test_is_legal_legit()

    def test_get_regions(self):
        s = get_complex_legal_solution()

        expected_regions = {
            create_region(PachamamaShape.TRIANGLE, {(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)}),
            create_region(PachamamaShape.CIRCLE, {(0, 2), (0, 3), (0, 4), (0, 5), (1, 4)}),
            create_region(PachamamaShape.SQUARE, {(1, 3), (2, 0), (2, 1), (2, 2), (2, 3)}),
            create_region(PachamamaShape.SQUARE, {(1, 5), (2, 5)}),
            create_region(PachamamaShape.TRIANGLE, {(2, 4), (3, 2), (3, 3), (3, 4), (4, 3)}),
            create_region(PachamamaShape.CIRCLE, {(3, 0), (3, 1), (4, 1), (4, 2), (5, 2)}),
            create_region(PachamamaShape.CIRCLE, {(3, 5)}),
            create_region(PachamamaShape.TRIANGLE, {(4, 0), (5, 0), (5, 1)}),
            create_region(PachamamaShape.SQUARE, {(4, 4), (4, 5), (5, 3), (5, 4), (5, 5)})
        }

        self.assertEqual(expected_regions, s._get_regions())

    def _test_is_legal_wrong_cell_type(self):
        s = PachamamaSolvedPuzzle(tuple([tuple([PachamamaCell(None, None)])]))
        self.assertFalse(s.is_legal())

    def _test_is_legal_large_region(self):
        s = PachamamaSolvedPuzzle((
            (PachamamaFilledCell(1, PachamamaShape.TRIANGLE), PachamamaFilledCell(2, PachamamaShape.TRIANGLE),
             PachamamaFilledCell(3, PachamamaShape.TRIANGLE)),
            (PachamamaFilledCell(4, PachamamaShape.TRIANGLE), PachamamaFilledCell(5, PachamamaShape.TRIANGLE),
             PachamamaFilledCell(1, PachamamaShape.TRIANGLE))
        ))
        self.assertFalse(s.is_legal())

    def _test_is_legal_region_with_repeats(self):
        s = PachamamaSolvedPuzzle(tuple([
            tuple([PachamamaFilledCell(1, PachamamaShape.TRIANGLE), PachamamaFilledCell(2, PachamamaShape.TRIANGLE),
                   PachamamaFilledCell(3, PachamamaShape.TRIANGLE), PachamamaFilledCell(1, PachamamaShape.TRIANGLE)])
        ]))
        self.assertFalse(s.is_legal())

    def _test_is_legal_region_missing_number(self):
        s = PachamamaSolvedPuzzle(tuple([
            tuple([PachamamaFilledCell(1, PachamamaShape.TRIANGLE), PachamamaFilledCell(2, PachamamaShape.TRIANGLE),
                   PachamamaFilledCell(3, PachamamaShape.TRIANGLE), PachamamaFilledCell(5, PachamamaShape.TRIANGLE)])
        ]))
        self.assertFalse(s.is_legal())

    def _test_is_legal_regions_touching(self):
        s = PachamamaSolvedPuzzle((
            (PachamamaFilledCell(1, PachamamaShape.TRIANGLE), PachamamaFilledCell(2, PachamamaShape.TRIANGLE),
             PachamamaFilledCell(1, PachamamaShape.CIRCLE), PachamamaFilledCell(2, PachamamaShape.CIRCLE)),
            (PachamamaFilledCell(3, PachamamaShape.TRIANGLE), PachamamaFilledCell(4, PachamamaShape.TRIANGLE),
             PachamamaFilledCell(3, PachamamaShape.CIRCLE), PachamamaFilledCell(4, PachamamaShape.CIRCLE)),
            (PachamamaFilledCell(1, PachamamaShape.SQUARE), PachamamaFilledCell(2, PachamamaShape.SQUARE),
             PachamamaFilledCell(1, PachamamaShape.TRIANGLE), PachamamaFilledCell(2, PachamamaShape.TRIANGLE)),
            (PachamamaFilledCell(3, PachamamaShape.SQUARE), PachamamaFilledCell(4, PachamamaShape.SQUARE),
             PachamamaFilledCell(3, PachamamaShape.TRIANGLE), PachamamaFilledCell(4, PachamamaShape.TRIANGLE))
        ))
        self.assertFalse(s.is_legal())

    def _test_is_legal_numbers_touching(self):
        s1 = PachamamaSolvedPuzzle((
            (PachamamaFilledCell(1, PachamamaShape.TRIANGLE), PachamamaFilledCell(2, PachamamaShape.TRIANGLE)),
            (PachamamaFilledCell(3, PachamamaShape.TRIANGLE), PachamamaFilledCell(1, PachamamaShape.CIRCLE))
        ))
        self.assertFalse(s1.is_legal())

        s2 = PachamamaSolvedPuzzle((
            (PachamamaFilledCell(1, PachamamaShape.TRIANGLE), PachamamaFilledCell(2, PachamamaShape.TRIANGLE)),
            (PachamamaFilledCell(1, PachamamaShape.CIRCLE), PachamamaFilledCell(3, PachamamaShape.TRIANGLE))
        ))
        self.assertFalse(s2.is_legal())

    def _test_is_legal_legit(self):
        s = get_complex_legal_solution()

        self.assertTrue(s.is_legal())


if __name__ == '__main__':
    unittest.main()
