from polyomino import Polyomino
from filter import filter_free
from filter import filter_one_sided
from filter import filter_chiral
from filter import filter_with_holes
from filter import filter_without_holes
from filter import filter_with_odd_side_lengths
from grid import neighbors

def _redelmeier_routine(p, parent, untried, forbidden):

    # todo use lifo linked list / stack implementation for untried

    if p == 0:
        yield parent.normalize()

    else:

        while untried:

            nbr = untried.pop()

            child = Polyomino(parent | {nbr})

            new_neighbours = list(filter(
                    lambda x : x not in parent and x not in forbidden and ((x[1] >= 0 and x[0] >= 0) or x[1] >= 1),
                    neighbors(nbr).difference(untried)
            ))

            forbidden = forbidden.union([nbr])

            yield from _redelmeier_routine(p-1, child, untried + new_neighbours, forbidden)

def _redelmeier(p):

    yield from _redelmeier_routine(p, Polyomino([]), [(0,0)], frozenset())


def childset(minos):

    """
        Return the set of children of the collection of polyominoes.
    """

    children = set()
    for mino in minos:
        children.update(mino.children())
    return children

def _fixed_with_offset(offset):

    init = fixed(offset)
    yield from _fixed_with_init(init)

def _fixed_with_init(minos):

    # Iteratively add the children of the members of the set before it
    while True:
        yield minos
        minos = childset(minos)

def _fixed():

    """
        Enumerate the fixed k-ominoes for all k >= 0.

        >>> from oeis import A001168
        >>> it = _fixed()
        >>> all(map(lambda n: len(next(it)) == A001168[n], range(8)))
        True

    """

    # The one zeromino
    init = {Polyomino([])}

    yield from _fixed_with_init(init)

def fixed(n):

    """

        >>> from oeis import A001168
        >>> all(map(lambda n: len(fixed(n)) == A001168[n], range(8)))
        True

    """

    return frozenset(_redelmeier(n))

def free(n):

    """

        >>> from oeis import A000105
        >>> all(map(lambda n: len(free(n)) == A000105[n], range(8)))
        True

    """

    return filter_free(fixed(n))

def one_sided(n):

    """

        >>> from oeis import A000988
        >>> all(map(lambda n: len(one_sided(n)) == A000988[n], range(8)))
        True

    """

    return filter_one_sided(fixed(n))

def chiral(n):

    """

        >>> from oeis import A030228
        >>> all(map(lambda n: len(chiral(n)) == A030228[n], range(8)))
        True

        For a(4)=2, the two chiral tetrominoes are XXX and XX .
                                                   X        XX

    """

    return filter_chiral(free(n))

def with_holes(n):

    """

        >>> from oeis import A001419
        >>> all(map(lambda n: len(with_holes(n)) == A001419[n], range(8)))
        True

    """

    return filter_with_holes(free(n))

def without_holes(n):

    """

        >>> from oeis import A000104
        >>> all(map(lambda n: len(without_holes(n)) == A000104[n], range(8)))
        True

    """

    return filter_without_holes(free(n))


def free_without_holes_with_odd_side_length(n):

    """

        >>> from oeis import A217595
        >>> all(map(lambda n: len(free_without_holes_with_odd_side_length(n)) == A217595[n], range(8)))
        True

    """

    return filter_with_odd_side_lengths(without_holes(n))
