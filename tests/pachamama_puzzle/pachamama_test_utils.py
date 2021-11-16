from collections import Set
from typing import Tuple

from src.pachamama_puzzle.pachamama_cell import PachamamaCell
from src.pachamama_puzzle.pachamama_filled_cell import PachamamaFilledCell
from src.pachamama_puzzle.pachamama_puzzle import PachamamaPuzzle
from src.pachamama_puzzle.pachamama_region import PachamamaRegion
from src.pachamama_puzzle.pachamama_shape import PachamamaShape
from src.pachamama_puzzle.pachamama_solved_puzzle import PachamamaSolvedPuzzle


def create_region(shape: PachamamaShape, cell_indices: Set[Tuple[int, int]]) -> PachamamaRegion:
    region = PachamamaRegion(shape)
    region.cell_indices = cell_indices
    return region


def get_complex_puzzle() -> PachamamaPuzzle:
    return PachamamaPuzzle(((PachamamaCell(None, None), PachamamaCell(5, None),
                             PachamamaCell(1, None), PachamamaCell(None, PachamamaShape.CIRCLE),
                             PachamamaCell(None, None), PachamamaCell(None, None)),
                            (PachamamaCell(4, PachamamaShape.TRIANGLE), PachamamaCell(None, None),
                             PachamamaCell(None, PachamamaShape.TRIANGLE), PachamamaCell(2, None),
                             PachamamaCell(None, PachamamaShape.CIRCLE), PachamamaCell(None, None)),
                            (PachamamaCell(None, PachamamaShape.SQUARE), PachamamaCell(None, None),
                             PachamamaCell(None, None), PachamamaCell(None, None),
                             PachamamaCell(None, None), PachamamaCell(None, None)),
                            (PachamamaCell(None, PachamamaShape.CIRCLE), PachamamaCell(None, None),
                             PachamamaCell(None, PachamamaShape.TRIANGLE), PachamamaCell(1, None),
                             PachamamaCell(None, None), PachamamaCell(None, PachamamaShape.CIRCLE)),
                            (PachamamaCell(3, PachamamaShape.TRIANGLE), PachamamaCell(None, PachamamaShape.CIRCLE),
                             PachamamaCell(None, None), PachamamaCell(None, None),
                             PachamamaCell(None, None), PachamamaCell(3, PachamamaShape.SQUARE)),
                            (PachamamaCell(None, None), PachamamaCell(None, None),
                             PachamamaCell(None, None), PachamamaCell(None, PachamamaShape.SQUARE),
                             PachamamaCell(None, None), PachamamaCell(4, None))
                            ))


def get_complex_legal_solution() -> PachamamaSolvedPuzzle:
    return PachamamaSolvedPuzzle((
        (PachamamaFilledCell(1, PachamamaShape.TRIANGLE), PachamamaFilledCell(5, PachamamaShape.TRIANGLE),
         PachamamaFilledCell(1, PachamamaShape.CIRCLE), PachamamaFilledCell(4, PachamamaShape.CIRCLE),
         PachamamaFilledCell(3, PachamamaShape.CIRCLE), PachamamaFilledCell(2, PachamamaShape.CIRCLE)),
        (PachamamaFilledCell(4, PachamamaShape.TRIANGLE), PachamamaFilledCell(2, PachamamaShape.TRIANGLE),
         PachamamaFilledCell(3, PachamamaShape.TRIANGLE), PachamamaFilledCell(2, PachamamaShape.SQUARE),
         PachamamaFilledCell(5, PachamamaShape.CIRCLE), PachamamaFilledCell(1, PachamamaShape.SQUARE)),
        (PachamamaFilledCell(3, PachamamaShape.SQUARE), PachamamaFilledCell(1, PachamamaShape.SQUARE),
         PachamamaFilledCell(5, PachamamaShape.SQUARE), PachamamaFilledCell(4, PachamamaShape.SQUARE),
         PachamamaFilledCell(3, PachamamaShape.TRIANGLE), PachamamaFilledCell(2, PachamamaShape.SQUARE)),
        (PachamamaFilledCell(2, PachamamaShape.CIRCLE), PachamamaFilledCell(4, PachamamaShape.CIRCLE),
         PachamamaFilledCell(2, PachamamaShape.TRIANGLE), PachamamaFilledCell(1, PachamamaShape.TRIANGLE),
         PachamamaFilledCell(5, PachamamaShape.TRIANGLE), PachamamaFilledCell(1, PachamamaShape.CIRCLE)),
        (PachamamaFilledCell(3, PachamamaShape.TRIANGLE), PachamamaFilledCell(5, PachamamaShape.CIRCLE),
         PachamamaFilledCell(3, PachamamaShape.CIRCLE), PachamamaFilledCell(4, PachamamaShape.TRIANGLE),
         PachamamaFilledCell(2, PachamamaShape.SQUARE), PachamamaFilledCell(3, PachamamaShape.SQUARE)),
        (PachamamaFilledCell(1, PachamamaShape.TRIANGLE), PachamamaFilledCell(2, PachamamaShape.TRIANGLE),
         PachamamaFilledCell(1, PachamamaShape.CIRCLE), PachamamaFilledCell(5, PachamamaShape.SQUARE),
         PachamamaFilledCell(1, PachamamaShape.SQUARE), PachamamaFilledCell(4, PachamamaShape.SQUARE))
    ))
