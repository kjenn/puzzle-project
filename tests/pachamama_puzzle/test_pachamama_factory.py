import unittest
from typing import Tuple

from src.pachamama_puzzle import pachamama_factory
from src.pachamama_puzzle.pachamama_solved_puzzle import PachamamaSolvedPuzzle
from tests.pachamama_puzzle import pachamama_test_utils


class TestPachamamaFilledCell(unittest.TestCase):

    def test_create_pachamama_puzzle(self):
        created_puzzle = pachamama_factory.create_pachamama_puzzle(self._get_complex_puzzle_simple_representation())
        self.assertEqual(pachamama_test_utils.get_complex_puzzle(), created_puzzle)
        self.assertFalse(isinstance(created_puzzle, PachamamaSolvedPuzzle))

    def test_create_pachamama_solved_puzzle(self):
        created_puzzle = pachamama_factory.create_pachamama_puzzle(
            self._get_complex_puzzle_solution_simple_representation())
        self.assertEqual(pachamama_test_utils.get_complex_legal_solution(), created_puzzle)
        self.assertTrue(isinstance(created_puzzle, PachamamaSolvedPuzzle))

    def test_solution_checker_with_created_puzzle_and_solution(self):
        puzzle = pachamama_factory.create_pachamama_puzzle(self._get_complex_puzzle_simple_representation())
        sol = pachamama_factory.create_pachamama_puzzle(self._get_complex_puzzle_solution_simple_representation())
        self.assertTrue(puzzle.is_sol_legal(sol))

    def test_create_pachamama_puzzle_not_grid(self):
        with self.assertRaises(ValueError):
            pachamama_factory.create_pachamama_puzzle(
                (('0x', '5x', '1x', '0c', '0x', '0x'),
                 ('4T', '0X', '0T', '2X', '0C', '0X'),
                 ('0S', '0X', '0X', '0X', '0X', '0X'),
                 ('0C', '0X', '0T', '1X', '0X', '0C'),
                 ('3T', '0C', '0X', '0X', '0X', '3S'),
                 ('0X', '0X', '0X', '0S', '0X')))

    def test_create_pachamama_puzzle_illegal_value(self):
        with self.assertRaises(ValueError):
            pachamama_factory.create_pachamama_puzzle(
                (('0x', '5x', '1x', '0c', '0x', '0x'),
                 ('4T', '0X', '0T', '2X', '0C', '0X'),
                 ('0S', '0X', '0X', '0X', '0X', '0X'),
                 ('0C', '0X', '0T', '1X', '0X', '0C'),
                 ('3T', '0C', '0X', '0X', '0X', '3S'),
                 ('0X', '0X', '0X', '0S', '0X', '4XC')))

        with self.assertRaises(ValueError):
            pachamama_factory.create_pachamama_puzzle(
                (('0x', '5x', '1x', '0c', '0x', '0x'),
                 ('4T', '0X', '0T', '2X', '0C', '0X'),
                 ('0S', '0X', '0X', '0X', '0X', '0X'),
                 ('0C', '0X', '0T', '1X', '0X', '0C'),
                 ('3T', '0C', '0X', '0X', '0X', '3S'),
                 ('0X', '0X', '0X', '0S', '0X', '4')))

        with self.assertRaises(ValueError):
            pachamama_factory.create_pachamama_puzzle(
                (('0x', '5x', '1x', '0c', '0x', '0x'),
                 ('4T', '0X', '0T', '2X', '0C', '0X'),
                 ('0S', '0X', '0X', '0X', '0X', '0X'),
                 ('0C', '0X', '0T', '1X', '0X', '0C'),
                 ('3T', '0C', '0X', '0X', '0X', '3S'),
                 ('0X', '0X', '0X', '0S', '0X', 'X')))

        with self.assertRaises(ValueError):
            pachamama_factory.create_pachamama_puzzle(
                (('0x', '5x', '1x', '0c', '0x', '0x'),
                 ('4T', '0X', '0T', '2X', '0C', '0X'),
                 ('0S', '0X', '0X', '0X', '0X', '0X'),
                 ('0C', '0X', '0T', '1X', '0X', '0C'),
                 ('3T', '0C', '0X', '0X', '0X', '3S'),
                 ('0X', '0X', '0X', '0S', '0X', 'X4')))

        with self.assertRaises(ValueError):
            pachamama_factory.create_pachamama_puzzle(
                (('0x', '5x', '1x', '0c', '0x', '0x'),
                 ('4T', '0X', '0T', '2X', '0C', '0X'),
                 ('0S', '0X', '0X', '0X', '0X', '0X'),
                 ('0C', '0X', '0T', '1X', '0X', '0C'),
                 ('3T', '0C', '0X', '0X', '0X', '3S'),
                 ('0X', '0X', '0X', '0S', '0X', '6X')))

        with self.assertRaises(ValueError):
            pachamama_factory.create_pachamama_puzzle(
                (('0x', '5x', '1x', '0c', '0x', '0x'),
                 ('4T', '0X', '0T', '2X', '0C', '0X'),
                 ('0S', '0X', '0X', '0X', '0X', '0X'),
                 ('0C', '0X', '0T', '1X', '0X', '0C'),
                 ('3T', '0C', '0X', '0X', '0X', '3S'),
                 ('0X', '0X', '0X', '0S', '0X', '5z')))

    @staticmethod
    def _get_complex_puzzle_simple_representation() -> Tuple[Tuple[str, ...], ...]:
        return (('0x', '5x', '1x', '0c', '0x', '0x'),
                ('4T', '0X', '0T', '2X', '0C', '0X'),
                ('0S', '0X', '0X', '0X', '0X', '0X'),
                ('0C', '0X', '0T', '1X', '0X', '0C'),
                ('3T', '0C', '0X', '0X', '0X', '3S'),
                ('0X', '0X', '0X', '0S', '0X', '4X'))

    @staticmethod
    def _get_complex_puzzle_solution_simple_representation() -> Tuple[Tuple[str, ...], ...]:
        return (('1T', '5T', '1C', '4C', '3C', '2C'),
                ('4t', '2t', '3t', '2s', '5c', '1s'),
                ('3s', '1s', '5s', '4s', '3t', '2s'),
                ('2c', '4c', '2t', '1t', '5t', '1c'),
                ('3t', '5c', '3c', '4t', '2s', '3s'),
                ('1t', '2t', '1c', '5s', '1s', '4s'))


if __name__ == '__main__':
    unittest.main()
