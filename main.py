from src.puzzles_with_skyscrapers.haido_puzzle import HaidoPuzzle

if __name__ == '__main__':
    # p = SkyscrapersPuzzle([[None for i in range(6)] for j in range(6)], [4] + [None for i in range(17)] + [5] + [None for i in range(5)])
    # p = SkyscrapersPuzzle([[None for i in range(6)] for j in range(6)], [None for i in range(12)] + [5] + [None for i in range(11)])
    # p = SkyscrapersPuzzle([[None for i in range(6)] for j in range(6)], [None for i in range(6)] + [6] + [None for i in range(17)])
    # p = SkyscrapersPuzzle([[None for i in range(6)] for j in range(6)], [None for i in range(18)] + [6, 5, 4, 3, 2, None])
    # p = SkyscrapersPuzzle.create_from_raw_puzzle([[None for i in range(5)] for j in range(5)],
    #                       [3, 3, None, None, None, None, 3, None, None, 4, None, 2, None, None, 4, None, 3, 4, None, None])
    # p = SkyscrapersPuzzle.create_from_raw_puzzle([[None for i in range(5)] for j in range(5)],
    #                                              [None]*20)
    # p = SkyscrapersPuzzle([[None for i in range(6)] for j in range(6)],
    #                       [None, None, 4, 4, None, 4,
    #                        4, None, None, 4, None, None,
    #                        4, None, None, None, 4, None,
    #                        None, None, 4, None, 4, None])

    # p = HaidoPuzzle(tuple(tuple(None for i in range(6)) for j in range(6)),
    #                 (2, 3, None, None, 5, 3,
    #                  None, None, 2, 2, None, None,
    #                  4, None, 4, 5, 3, 4,
    #                  2, None, None, None, 2, 3))

    p = HaidoPuzzle(tuple([tuple([None] * 6)] * 6), tuple([None, 5, 4, 3, 2, 1] + [None] * 18))

    sol = p.solve()
    # for row in p.puzzle_to_draw_on:
    #     print("   ".join([x.show_str() for x in row]))
    # for row in p.puzzle_to_draw_on:
    #     print(" ".join([str(x.value) for x in row]))
    if sol is None:
        print("There is no solution.")
    elif isinstance(sol, tuple):
        for row in sol[0]:
            print(" ".join([str(x) for x in row]))
        print('-------------------------')
        for row in sol[1]:
            print(" ".join([str(x) for x in row]))
    else:
        for row in sol:
            print(" ".join([str(x) for x in row]))
