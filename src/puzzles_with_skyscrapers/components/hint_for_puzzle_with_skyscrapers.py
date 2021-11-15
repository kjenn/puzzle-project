from src.components.abstract_grid_puzzle import NUMBER_OF_GRID_SIDES


def get_hint_side(hint_index: int, num_of_rows_in_puzzle: int):
    return int(hint_index / num_of_rows_in_puzzle)


def validate_hint_index(hint_index: int, num_of_rows_in_puzzle: int):
    number_of_hints = NUMBER_OF_GRID_SIDES * num_of_rows_in_puzzle
    if not 0 <= hint_index < number_of_hints:
        raise ValueError(f"There are only {number_of_hints} possible hints.")

