from typing import Set

from src.pachamama_puzzle.pachamama_cell import PachamamaCell
from src.pachamama_puzzle.pachamama_filled_cell import PachamamaFilledCell
from src.pachamama_puzzle.pachamama_puzzle import PachamamaPuzzle
from src.pachamama_puzzle.pachamama_region import PachamamaRegion


class PachamamaSolvedPuzzle(PachamamaPuzzle):

    def is_legal(self) -> bool:
        for row in self.puzzle:
            for cell in row:
                if not isinstance(cell, PachamamaFilledCell):
                    return False

        for region in self._get_regions():
            if len(region.cell_indices) > PachamamaCell.MAX_REGION_SIZE:
                return False
            for neighbor_x, neighbor_y in self._get_region_neighbor_indices(region):
                if self.puzzle[neighbor_x][neighbor_y].shape == region.shape:
                    return False
            numbers_in_region = set(self.puzzle[x][y].number for x, y in region.cell_indices)
            for i in range(1, len(region.cell_indices) + 1):
                if i not in numbers_in_region:
                    return False

        for i in range(self.num_of_rows):
            for j in range(self.num_of_cols):
                neighbor_numbers = set(self.puzzle[x][y].number for x, y in self._get_neighbor_indices(i, j))
                if self.puzzle[i][j].number in neighbor_numbers:
                    return False

        return True

    def _get_regions(self) -> Set[PachamamaRegion]:
        cell_to_region = {(x, y): None for x in range(self.num_of_rows) for y in range(self.num_of_cols)}
        for i in range(self.num_of_rows):
            for j in range(self.num_of_cols):
                if cell_to_region.get((i, j)) is None:
                    region_shape = self.puzzle[i][j].shape
                    region = PachamamaRegion(region_shape)
                    new_cells_in_region = {(i, j)}
                    while len(new_cells_in_region) > 0:
                        current_cell = new_cells_in_region.pop()
                        cell_to_region[current_cell] = region
                        region.add_cell(current_cell)
                        for adjacent in self._get_adjacent_indices(current_cell[0], current_cell[1]):
                            if cell_to_region[adjacent] is None \
                                    and self.puzzle[adjacent[0]][adjacent[1]].shape == region_shape:
                                new_cells_in_region.add(adjacent)
        return set(cell_to_region.values())
