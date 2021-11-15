from src.puzzles_with_skyscrapers.skyscrapers_puzzle import SkyscrapersPuzzle

if __name__ == '__main__':

    p = SkyscrapersPuzzle(tuple([tuple([None] * 6)] * 6),
                          (None, None, 4, 4, None, 4,
                           4, None, None, 4, None, None,
                           4, None, None, None, 4, None,
                           None, None, 4, None, 4, None))

    sol = p.solve()
    # if sol is None:
    #     print("")
    # elif isinstance(sol, tuple):
    #     for row in sol[0]:
    #         print(" ".join([str(x) for x in row]))
    #     print('-------------------------')
    #     for row in sol[1]:
    #         print(" ".join([str(x) for x in row]))
    # else:
    #     for row in sol:
    #         print(" ".join([str(x) for x in row]))
