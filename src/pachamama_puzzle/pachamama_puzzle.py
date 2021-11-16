from typing import Tuple, Set

from src.pachamama_puzzle.pachamama_region import PachamamaRegion
from src.components.abstract_grid_puzzle import AbstractGridPuzzle


class PachamamaPuzzle(AbstractGridPuzzle):

    def is_sol_legal(self, sol: "PachamamaSolvedPuzzle") -> bool:
        if sol is None:
            return False

        if sol.num_of_rows != self.num_of_rows or sol.num_of_cols != self.num_of_cols:
            return False

        for i in range(self.num_of_rows):
            for j in range(self.num_of_cols):
                if self.puzzle[i][j].number is not None:
                    if self.puzzle[i][j].number != sol.puzzle[i][j].number:
                        return False
                if self.puzzle[i][j].shape is not None:
                    if self.puzzle[i][j].shape != sol.puzzle[i][j].shape:
                        return False

        return sol.is_legal()

    def _get_adjacent_indices(self, row: int, col: int) -> Set[Tuple[int, int]]:
        return self._get_only_real_cells(self._get_possible_adjacent_indices(row, col))

    def _get_neighbor_indices(self, row: int, col: int) -> Set[Tuple[int, int]]:
        return self._get_only_real_cells(self._get_possible_neighbor_indices(row, col))

    def _get_region_neighbor_indices(self, region: PachamamaRegion) -> Set[Tuple[int, int]]:
        return set(neighbor for cell in region.cell_indices for neighbor in self._get_neighbor_indices(cell[0], cell[1])
                   if neighbor not in region.cell_indices)

    def _get_only_real_cells(self, possible_cells: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        return set(x for x in possible_cells if self._does_cell_exist(x[0], x[1]))

    @staticmethod
    def _get_possible_adjacent_indices(row: int, col: int) -> Set[Tuple[int, int]]:
        return {(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)}

    @staticmethod
    def _get_possible_neighbor_indices(row: int, col: int) -> Set[Tuple[int, int]]:
        return PachamamaPuzzle._get_possible_adjacent_indices(row, col) \
               | {(row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)}

    def _does_cell_exist(self, row: int, col: int) -> bool:
        return 0 <= row < self.num_of_rows and 0 <= col < self.num_of_cols

    def __eq__(self, other):
        if not isinstance(other, PachamamaPuzzle):
            return False
        return self.puzzle == other.puzzle

# TODO add parser to allow simpler form of input (1C would be a cell with #1 and a circle)
