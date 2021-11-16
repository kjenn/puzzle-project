from typing import Optional

from src.pachamama_puzzle.pachamama_cell import PachamamaCell
from src.pachamama_puzzle.pachamama_shape import PachamamaShape


class PachamamaFilledCell(PachamamaCell):

    def __init__(self, number: Optional[int], shape: Optional[PachamamaShape]):
        super().__init__(number, shape)
        if shape is None:
            raise ValueError("A filled cell must have a shape")
        if number is None:
            raise ValueError("A filled cell must have a number")
