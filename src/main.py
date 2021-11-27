from src.puzzles_with_skyscrapers.skyscrapers_extra_building_puzzle import SkyscrapersExtraBuildingPuzzle
from src.puzzles_with_skyscrapers.skyscrapers_gaps_puzzle import SkyscrapersGapsPuzzle
from src.puzzles_with_skyscrapers.skyscrapers_puzzle import SkyscrapersPuzzle

if __name__ == '__main__':
    # p = SkyscrapersPuzzle(tuple([tuple([None] * 6)] * 6),
    #                       (None, None, 4, 4, None, 4,
    #                        4, None, None, 4, None, None,
    #                        4, None, None, None, 4, None,
    #                        None, None, 4, None, 4, None))
    # p = SkyscrapersExtraBuildingPuzzle(tuple([tuple([None] * 5)] * 5),
    #                                    (None, None, None, None, None,
    #                                     5, 5, 3, 3, None,
    #                                     4, None, 3, 1, None,
    #                                     None, None, None, 3, None))
    p = SkyscrapersGapsPuzzle(tuple([tuple([None] * 6)] * 6),
                              (3, None, 1, 4, 1, 5,
                               None, 3, None, None, None, None,
                               None, None, None, None, None, None,
                               None, 3, None, 1, 4, None))

    sol = p.solve()
