from src.puzzles_with_skyscrapers.skyscrapers_puzzle import SkyscrapersPuzzle

if __name__ == '__main__':

    p = SkyscrapersPuzzle(tuple([tuple([None] * 6)] * 6),
                          (None, None, 4, 4, None, 4,
                           4, None, None, 4, None, None,
                           4, None, None, None, 4, None,
                           None, None, 4, None, 4, None))

    sol = p.solve()