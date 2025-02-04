import enumerate

def cardinality ( iterable ) :

    try:
        return len(iterable)
    except TypeError:
        return sum(map(lambda x: 1, iterable))


def fixed(n):

    """

        >>> fixed(9)
        9910
        >>> from oeis import A001168
        >>> all(map(lambda n: fixed(n) == A001168[n], range(10)))
        True

    """

    return cardinality(enumerate._redelmeier(n))

def free(n):

    """

        >>> from oeis import A000105
        >>> all(map(lambda n: free(n) == A000105[n], range(10)))
        True

    """

    return cardinality(enumerate._free_mem(n))

def one_sided(n):

    """

        >>> from oeis import A000988
        >>> all(map(lambda n: one_sided(n) == A000988[n], range(10)))
        True

    """

    return cardinality(enumerate._one_sided_mem(n))

def chiral(n):

    """

        >>> from oeis import A030228
        >>> all(map(lambda n: chiral(n) == A030228[n], range(10)))
        True

    """

    return cardinality(enumerate._chiral_mem(n))

def with_holes(n):

    """

        >>> from oeis import A001419
        >>> all(map(lambda n: with_holes(n) == A001419[n], range(10)))
        True

    """

    return cardinality(enumerate._with_holes_mem(n))

def without_holes(n):

    """

        >>> from oeis import A000104
        >>> all(map(lambda n: without_holes(n) == A000104[n], range(10)))
        True

    """

    return cardinality(enumerate._without_holes_mem(n))


def free_without_holes_with_odd_side_length(n):

    """

        >>> from oeis import A217595
        >>> all(map(lambda n: free_without_holes_with_odd_side_length(n) == A217595[n], range(10)))
        True

    """

    return cardinality(enumerate._free_without_holes_with_odd_side_length_mem(n))
