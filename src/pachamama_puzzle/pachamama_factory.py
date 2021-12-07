from typing import Tuple, Optional

from src.pachamama_puzzle.pachamama_cell import PachamamaCell
from src.pachamama_puzzle.pachamama_filled_cell import PachamamaFilledCell
from src.pachamama_puzzle.pachamama_puzzle import PachamamaPuzzle
from src.pachamama_puzzle.pachamama_shape import PachamamaShape
from src.pachamama_puzzle.pachamama_solved_puzzle import PachamamaSolvedPuzzle


LETTER_TO_SHAPE = {'X': None, 'C': PachamamaShape.CIRCLE, 'T': PachamamaShape.TRIANGLE, 'S': PachamamaShape.SQUARE}


def create_pachamama_puzzle(simple_representation: Tuple[Tuple[str, ...], ...]) -> PachamamaPuzzle:
    grid = tuple(tuple(_create_pachamama_cell(cell) for cell in row) for row in simple_representation)
    if all((isinstance(cell, PachamamaFilledCell) for row in grid for cell in row)):
        return PachamamaSolvedPuzzle(grid)
    return PachamamaPuzzle(grid)


def _create_pachamama_cell(string_representation: str) -> PachamamaCell:
    if len(string_representation) != 2:
        raise ValueError(_get_representation_explanation() + f"The problematic cell: {string_representation}")
    cell_num = _get_cell_num(string_representation[0])
    shape_string = string_representation[1]
    cell_shape = _get_cell_shape(shape_string)
    if cell_num and cell_shape:
        return PachamamaFilledCell(cell_num, cell_shape)
    return PachamamaCell(cell_num, cell_shape)


def _get_cell_num(num_string: str) -> Optional[int]:
    try:
        cell_num = int(num_string)
    except ValueError:
        raise ValueError(_get_representation_explanation() + f"The problematic number: {num_string}")
    if cell_num not in range(PachamamaCell.MAX_REGION_SIZE + 1):
        raise ValueError(_get_representation_explanation() + f"The problematic number: {num_string}")
    if cell_num == 0:
        return None
    return cell_num


def _get_cell_shape(shape_string: str) -> Optional[PachamamaShape]:
    try:
        cell_shape = LETTER_TO_SHAPE[shape_string.upper()]
    except KeyError:
        raise ValueError(_get_representation_explanation() + f"The problematic shape: {shape_string}")
    return cell_shape


def _get_representation_explanation():
    return f"A wrong string representation of a Pachamama cell was given. A representation must be of " \
           f"length 2, where the first value is a number between 0 and {PachamamaCell.MAX_REGION_SIZE}, " \
           f"and the second value is one of: {LETTER_TO_SHAPE.keys()}. "
