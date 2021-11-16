from typing import Tuple

from src.pachamama_puzzle.pachamama_cell import PachamamaShape


class PachamamaRegion:

    def __init__(self, shape: PachamamaShape):
        self.shape = shape
        self.cell_indices = set()

    def add_cell(self, cell_index: Tuple[int, int]):
        self.cell_indices.add(cell_index)

    def __eq__(self, other):
        if not isinstance(other, PachamamaRegion):
            return False
        return self.shape == other.shape and self.cell_indices == other.cell_indices

    def __hash__(self):
        return hash((self.shape, tuple(sorted(self.cell_indices))))
