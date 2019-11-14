"""

    Module with peer-reviewed counts for polyomino classes.
    All sequences start at order 0.
    The empty polyomino exists, is unique, has no hole, is not chiral.
    Scrapped from the [OEIS](https://oeis.org).

    TRIVIA
    ==

    A000105(n) + A030228(n) = A000988(n) because the number of free polyominoes plus the
    number of polyominoes lacking bilateral symmetry equals the number of one-sided
    polyominoes. - Graeme McRae, Jan 05 2006

    >>> all(map(lambda n: A000105[n] + A030228[n] == A000988[n], range(20)))
    True

"""


"""
    Number of n-celled polyominoes without holes.

    https://oeis.org/A000104
"""
A000104 = M1424 = N0560 = free_without_holes = (1, 1, 1, 2, 5, 12, 35, 107,
                363, 1248, 4460, 16094, 58937, 217117, 805475, 3001127,
                11230003, 42161529, 158781106, 599563893, 2269506062,
                8609442688, 32725637373, 124621833354, 475368834568,
                1816103345752, 6948228104703)

"""
    Number of free polyominoes (or square animals) with n cells.

    https://oeis.org/A000105

    a(n) + A030228(n) = A000988(n) because the number of free polyominoes plus the
    number of polyominoes lacking bilateral symmetry equals the number of one-sided
    polyominoes. - Graeme McRae, Jan 05 2006
"""

A000105 = M1425 = N0561 = free = (1, 1, 1, 2, 5, 12, 35, 108, 369, 1285, 4655,
                17073, 63600, 238591, 901971, 3426576, 13079255, 50107909,
                192622052, 742624232, 2870671950, 11123060678, 43191857688,
                168047007728, 654999700403, 2557227044764, 9999088822075,
                39153010938487, 153511100594603)


"""
    Number of n-celled polyominoes with holes.

    https://oeis.org/A001419
"""
A001419 = M4226 = N1767 = free_with_holes = (0, 0, 0, 0, 0, 0, 1, 6, 37, 195,
                979, 4663, 21474, 96496, 425449, 1849252, 7946380, 33840946,
                143060339, 601165888, 2513617990, 10466220315, 43425174374,
                179630865835, 741123699012, 3050860717372)

"""
    Number of one-sided polyominoes with n cells.

    https://oeis.org/A000988

    A000105(n) + A030228(n) = a(n) because the number of free polyominoes plus the
    number of polyominoes lacking bilateral symmetry equals the number of one-sided
    polyominoes. - Graeme McRae, Jan 05 2006
"""
A000988 = M1749 = N0693 = one_sided = (1, 1, 1, 2, 7, 18, 60, 196, 704, 2500,
                9189, 33896, 126759, 476270, 1802312, 6849777, 26152418,
                100203194, 385221143, 1485200848, 5741256764, 22245940545,
                86383382827, 336093325058, 1309998125640, 5114451441106,
                19998172734786, 78306011677182, 307022182222506,
                1205243866707468, 4736694001644862)

"""
    Number of fixed polyominoes with n cells.

    https://oeis.org/A001168
"""
A001168 = M1639 = N0641 = fixed = (1, 1, 2, 6, 19, 63, 216, 760, 2725, 9910,
                36446, 135268, 505861, 1903890, 7204874, 27394666, 104592937,
                400795844, 1540820542, 5940738676, 22964779660, 88983512783,
                345532572678, 1344372335524, 5239988770268, 20457802016011,
                79992676367108, 313224032098244, 1228088671826973)

"""
    Number of chiral polyominoes with n cells.

    https://oeis.org/A030228

    A000105(n) + a(n) = A000988(n) because the number of free polyominoes plus the
    number of polyominoes lacking bilateral symmetry equals the number of one-sided
    polyominoes. - Graeme McRae, Jan 05 2006
"""

A030228 = chiral = (0, 0, 0, 0, 2, 6, 25, 88, 335, 1215, 4534, 16823, 63159,
                237679, 900341, 3423201, 13073163, 50095285, 192599091,
                742576616, 2870584814, 11122879867, 43191525139, 168046317330,
                654998425237, 2557224396342, 9999083912711, 39153000738695,
                153511081627903)
