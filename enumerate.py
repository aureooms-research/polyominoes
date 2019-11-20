from polyomino import Polyomino
from polyomino import empty
from filter import _filter_free
from filter import _filter_free_mem
from filter import _filter_one_sided
from filter import _filter_one_sided_mem
from filter import _filter_chiral
from filter import _filter_with_holes
from filter import _filter_without_holes
from filter import _filter_with_odd_side_lengths
from grid import neighbors
from grid import normalize

def _redelmeier_routine(p, parent, untried, forbidden):

    # todo use lifo linked list / stack implementation for untried

    if p == 0:
        yield Polyomino(normalize(parent))

    else:

        while untried:

            nbr = untried.pop()

            child = parent | {nbr}

            new_neighbours = list(filter(
                    lambda x : x not in parent and x not in forbidden and ((x[1] >= 0 and x[0] >= 0) or x[1] >= 1),
                    neighbors(nbr).difference(untried)
            ))

            forbidden = forbidden.union([nbr])

            yield from _redelmeier_routine(p-1, child, untried + new_neighbours, forbidden)

def _redelmeier(n):

    return _redelmeier_routine(n, frozenset(), [(0,0)], frozenset())

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

def _fixed_gen():

    """
        Enumerate the fixed k-ominoes for all k >= 0.

        >>> from oeis import A001168
        >>> it = _fixed_gen()
        >>> all(map(lambda n: len(next(it)) == A001168[n], range(8)))
        True

    """

    return _fixed_with_init({empty})

_fixed = _redelmeier

def fixed(n):

    """

        >>> from oeis import A001168
        >>> all(map(lambda n: len(fixed(n)) == A001168[n], range(8)))
        True

    """

    return frozenset(_fixed(n))

def _free_mem(n):
    return _filter_free_mem(_fixed(n))

def _free(n):
    return _filter_free(_fixed(n))

def free(n):

    """

        >>> from oeis import A000105
        >>> all(map(lambda n: len(free(n)) == A000105[n], range(8)))
        True

    """

    return frozenset(_free(n))

def _one_sided_mem(n):
    return _filter_one_sided_mem(_fixed(n))

def _one_sided(n):
    return _filter_one_sided(_fixed(n))

def one_sided(n):

    """

        >>> from oeis import A000988
        >>> all(map(lambda n: len(one_sided(n)) == A000988[n], range(8)))
        True

    """

    return frozenset(_one_sided(n))

def _chiral_mem(n):
    return _filter_chiral(_free_mem(n))

def _chiral(n):
    return _filter_chiral(_free(n))

def chiral(n):

    """

        >>> from oeis import A030228
        >>> all(map(lambda n: len(chiral(n)) == A030228[n], range(8)))
        True

        For a(4)=2, the two chiral tetrominoes are XXX and XX .
                                                   X        XX

    """

    return frozenset(_chiral(n))

def _with_holes(n):
    return _filter_with_holes(_free(n))

def _with_holes_mem(n):
    return _filter_with_holes(_free_mem(n))

def with_holes(n):

    """

        >>> from oeis import A001419
        >>> all(map(lambda n: len(with_holes(n)) == A001419[n], range(8)))
        True

    """

    return frozenset(_with_holes(n))

def _without_holes(n):
    return _filter_without_holes(_free(n))

def _without_holes_mem(n):
    return _filter_without_holes(_free_mem(n))

def without_holes(n):

    """

        >>> from oeis import A000104
        >>> all(map(lambda n: len(without_holes(n)) == A000104[n], range(8)))
        True

    """

    return frozenset(_without_holes(n))


def _free_without_holes_with_odd_side_length(n):
    return _filter_with_odd_side_lengths(_without_holes(n))

def _free_without_holes_with_odd_side_length_mem(n):
    return _filter_with_odd_side_lengths(_without_holes_mem(n))

def free_without_holes_with_odd_side_length(n):

    """

        >>> from oeis import A217595
        >>> all(map(lambda n: len(free_without_holes_with_odd_side_length(n)) == A217595[n], range(8)))
        True

    """

    return frozenset(_free_without_holes_with_odd_side_length(n))
