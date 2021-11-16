import unittest

from src.pachamama_puzzle.pachamama_cell import PachamamaCell
from src.pachamama_puzzle.pachamama_filled_cell import PachamamaFilledCell
from src.pachamama_puzzle.pachamama_puzzle import PachamamaPuzzle
from src.pachamama_puzzle.pachamama_shape import PachamamaShape
from src.pachamama_puzzle.pachamama_solved_puzzle import PachamamaSolvedPuzzle
from tests.pachamama_puzzle.pachamama_test_utils import get_complex_legal_solution, get_complex_puzzle, create_region


class TestPachamamaPuzzle(unittest.TestCase):

    def test_is_sol_legal(self):
        p = PachamamaPuzzle(((PachamamaCell(None, PachamamaShape.CIRCLE), PachamamaCell(None, None)),
                             (PachamamaCell(2, None), PachamamaCell(None, None))))

        self.assertFalse(p.is_sol_legal(None))

        self.assertFalse(
            p.is_sol_legal(PachamamaSolvedPuzzle((tuple([PachamamaFilledCell(1, PachamamaShape.CIRCLE)]),
                                                  tuple([PachamamaFilledCell(2, PachamamaShape.CIRCLE)]))))
        )

        self.assertFalse(
            p.is_sol_legal((PachamamaSolvedPuzzle((
                (PachamamaFilledCell(1, PachamamaShape.CIRCLE), PachamamaFilledCell(3, PachamamaShape.CIRCLE)),
                (PachamamaFilledCell(2, PachamamaShape.CIRCLE), PachamamaFilledCell(4, PachamamaShape.CIRCLE)),
                (PachamamaFilledCell(1, PachamamaShape.SQUARE), PachamamaFilledCell(5, PachamamaShape.CIRCLE))
            ))))
        )

        self.assertFalse(
            p.is_sol_legal((PachamamaSolvedPuzzle((
                (PachamamaFilledCell(1, PachamamaShape.TRIANGLE), PachamamaFilledCell(3, PachamamaShape.TRIANGLE)),
                (PachamamaFilledCell(2, PachamamaShape.TRIANGLE), PachamamaFilledCell(4, PachamamaShape.TRIANGLE))
            ))))
        )

        self.assertFalse(
            p.is_sol_legal((PachamamaSolvedPuzzle((
                (PachamamaFilledCell(2, PachamamaShape.CIRCLE), PachamamaFilledCell(3, PachamamaShape.CIRCLE)),
                (PachamamaFilledCell(1, PachamamaShape.CIRCLE), PachamamaFilledCell(4, PachamamaShape.CIRCLE))
            ))))
        )

        self.assertTrue(
            PachamamaPuzzle(tuple([tuple([PachamamaCell(None, None)] * 6)] * 6)).is_sol_legal(
                get_complex_legal_solution()))

        self.assertTrue(
            get_complex_puzzle().is_sol_legal(get_complex_legal_solution()))

    def test_get_adjacent_indices(self):
        p = PachamamaPuzzle(tuple([tuple([PachamamaCell(None, None)] * 6)] * 3))
        self.assertEqual({(0, 2), (1, 1), (1, 3), (2, 2)},
                         p._get_adjacent_indices(1, 2))
        self.assertEqual({(0, 0), (0, 2), (1, 1)},
                         p._get_adjacent_indices(0, 1))
        self.assertEqual({(0, 5), (1, 4), (2, 5)},
                         p._get_adjacent_indices(1, 5))
        self.assertEqual({(1, 5), (2, 4)},
                         p._get_adjacent_indices(2, 5))

    def test_get_neighbor_indices(self):
        p = PachamamaPuzzle(tuple([tuple([PachamamaCell(None, None)] * 6)] * 3))
        self.assertEqual({(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (2, 2), (2, 3)},
                         p._get_neighbor_indices(1, 2))
        self.assertEqual({(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)},
                         p._get_neighbor_indices(0, 1))
        self.assertEqual({(0, 4), (0, 5), (1, 4), (2, 4), (2, 5)},
                         p._get_neighbor_indices(1, 5))
        self.assertEqual({(1, 4), (1, 5), (2, 4)},
                         p._get_neighbor_indices(2, 5))

    def test_get_region_neighbor_indices(self):
        p = PachamamaPuzzle(tuple([tuple([PachamamaCell(None, None)] * 6)] * 4))

        self.assertEqual(
            {(0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (1, 4), (2, 1), (2, 2), (2, 4), (3, 2), (3, 3), (3, 4)},
            p._get_region_neighbor_indices(create_region(PachamamaShape.CIRCLE, {(1, 2), (1, 3), (2, 3)})))

        self.assertEqual(
            {(0, 3), (1, 3), (1, 4), (2, 4), (2, 5)},
            p._get_region_neighbor_indices(create_region(PachamamaShape.CIRCLE, {(0, 4), (0, 5), (1, 5)})))

        self.assertEqual(
            {(0, 1), (1, 1), (1, 2), (2, 2), (3, 0), (3, 2)},
            p._get_region_neighbor_indices(
                create_region(PachamamaShape.CIRCLE, {(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)})))


if __name__ == '__main__':
    unittest.main()
