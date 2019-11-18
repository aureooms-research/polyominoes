from polyomino import Polyomino
from filter import filter_free
from filter import filter_one_sided
from filter import filter_chiral
from filter import filter_with_holes
from filter import filter_without_holes
from filter import filter_with_odd_side_lengths

def childset(minos):

    """
        Return the set of children of the collection of polyominoes.
    """

    children = set()
    for mino in minos:
        children.update(mino.children())
    return children


def _fixed():

    """
        Enumerate the fixed k-ominoes for all k >= 1.
    """

    # The one monomino
    minos = {Polyomino([(0,0)])}

    # Iteratively add the children of the members of the set before it
    while True:
        yield minos
        minos = childset(minos)

def fixed(n):

    """

        >>> from oeis import A001168
        >>> all(map(lambda n: len(fixed(n)) == A001168[n], range(1,8)))
        True

    """

    it = _fixed()

    for i in range(n):
        minos = next(it)

    return minos

def free(n):

    """

        >>> from oeis import A000105
        >>> all(map(lambda n: len(free(n)) == A000105[n], range(1,8)))
        True

    """

    return filter_free(fixed(n))

def one_sided(n):

    """

        >>> from oeis import A000988
        >>> all(map(lambda n: len(one_sided(n)) == A000988[n], range(1,8)))
        True

    """

    return filter_one_sided(fixed(n))

def chiral(n):

    """

        >>> from oeis import A030228
        >>> all(map(lambda n: len(chiral(n)) == A030228[n], range(1,8)))
        True

        For a(4)=2, the two chiral tetrominoes are XXX and XX .
                                                   X        XX

    """

    return filter_chiral(free(n))

def with_holes(n):

    """

        >>> from oeis import A001419
        >>> all(map(lambda n: len(with_holes(n)) == A001419[n], range(1,8)))
        True

    """

    return filter_with_holes(free(n))

def without_holes(n):

    """

        >>> from oeis import A000104
        >>> all(map(lambda n: len(without_holes(n)) == A000104[n], range(1,8)))
        True

    """

    return filter_without_holes(free(n))


def free_without_holes_with_odd_side_length(n):

    """

        >>> from oeis import A217595
        >>> all(map(lambda n: len(free_without_holes_with_odd_side_length(n)) == A217595[n], range(1,8)))
        True

    """

    return filter_with_odd_side_lengths(without_holes(n))
