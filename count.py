import enumerate

def cardinality ( iterable ) :
    return sum(map(lambda x: 1, iterable))


def fixed(n):

    """

        >>> from oeis import A001168
        >>> all(map(lambda n: fixed(n) == A001168[n], range(1,10)))
        True

    """

    return len(enumerate.fixed(n))

def free(n):

    """

        >>> from oeis import A000105
        >>> all(map(lambda n: free(n) == A000105[n], range(1,10)))
        True

    """

    return len(enumerate.free(n))

def one_sided(n):

    """

        >>> from oeis import A000988
        >>> all(map(lambda n: one_sided(n) == A000988[n], range(1,10)))
        True

    """

    return len(enumerate.one_sided(n))

def chiral(n):

    """

        >>> from oeis import A030228
        >>> all(map(lambda n: chiral(n) == A030228[n], range(1,10)))
        True

    """

    return len(enumerate.chiral(n))

def with_holes(n):

    """

        >>> from oeis import A001419
        >>> all(map(lambda n: with_holes(n) == A001419[n], range(1,10)))
        True

    """

    return len(enumerate.with_holes(n))

def without_holes(n):

    """

        >>> from oeis import A000104
        >>> all(map(lambda n: without_holes(n) == A000104[n], range(1,10)))
        True

    """

    return len(enumerate.without_holes(n))


def free_without_holes_with_odd_side_length(n):

    """

        >>> from oeis import A217595
        >>> all(map(lambda n: free_without_holes_with_odd_side_length(n) == A217595[n], range(1,10)))
        True

    """

    return len(enumerate.free_without_holes_with_odd_side_length(n))
