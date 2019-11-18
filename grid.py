from collections import Counter
from debug import debug

def neighbors(cell):

    """

        Get neighbors of this cell in no specific order.

        >>> sorted(neighbors((7,5)))
        [(6, 5), (7, 4), (7, 6), (8, 5)]

    """

    return frozenset(_neighbors(cell))

def _neighbors(cell):

    """

        Get upper, right, lower, left neighbors of this cell, in that order.

        >>> list(_neighbors((7,5)))
        [(7, 6), (8, 5), (7, 4), (6, 5)]

    """

    i, j = cell
    yield (i, j+1)
    yield (i+1, j)
    yield (i, j-1)
    yield (i-1, j)


def _neighbors_from_direction(neighbor, cell):

    """

        Get the neighbors you see if you look left, forward, right, then backward
        after entering the cell from a neighboring one.
        (clockwise).

    """

    x, y = neighbor
    i, j = cell
    dx, dy = x-i, y-j

    if dx == 0:
        if dy == 1:
            yield (i+1, j)
            yield (i, j-1)
            yield (i-1, j)
            yield (i, j+1)
        else:
            yield (i-1, j)
            yield (i, j+1)
            yield (i+1, j)
            yield (i, j-1)
    elif dx == 1:
        yield (i, j-1)
        yield (i-1, j)
        yield (i, j+1)
        yield (i+1, j)
    else:
        yield (i, j+1)
        yield (i+1, j)
        yield (i, j-1)
        yield (i-1, j)


def is_connected ( cells ) :

    it = iter(cells)

    try:
        first = next(it)
    except StopIteration:
        return True

    todo = set(it)
    queue = [first]

    while queue:

        current = queue.pop()

        for neighbor in _neighbors(current):

            if neighbor in todo:
                todo.remove(neighbor)
                queue.append(neighbor)

    return not todo


def boundary_cells ( mino ):

    """
        Returns cells of the boundary of the input polyomino.
    """

    kill_count = Counter(chain(*[_neighbors(cell) for cell in mino]))

    debug("kill_count", kill_count)

    killed = map(lambda t: t[0], filter(lambda t: t[1] == 4, kill_count.items()))

    return mino.difference(killed)


def boundary ( mino ):

    """
        Returns boundary of the input polyomino (clockwise).
    """

    if len(mino) == 0: return []

    if len(mino) == 1: return [(0,0), (0,1), (1,1), (1,0)]

    # xxxxxx
    # ^ x
    # ! xxxx
    #   xxx
    #  xx

    n = len(mino)

    first = mino.origin

    debug("first", first)

    # those are coordinates of the lattice

    previous = first
    if (first[0],first[1]+1) in mino:
        boundary = [(first[0],first[1]+1)]
        second = (first[0],first[1]+1)
    else:
        boundary = [(first[0]+1,first[1]+1)]
        second = (first[0]+1,first[1])

    current = second

    while True:

        assert len(boundary) <= 2 * (n+1)

        debug('boundary', boundary)
        debug('previous', previous)
        debug('current', current)

        for case, neighbor in enumerate(_neighbors_from_direction(previous, current)):

            debug('neighbor', case, 'is', neighbor)

            if case >= 1:
                x = boundary[-1][0] + neighbor[0] - current[0]
                y = boundary[-1][1] + neighbor[1] - current[1]
                boundary.append((x,y))

            if neighbor in mino:
                previous = current
                current = neighbor
                break

        if current == second and previous == first:
            boundary.pop()
            return boundary


def _corners ( b ) :

    for p, q, r in zip(b[-1:] + b[:-1], b, b[1:] + b[:1]):
        if (not p[0] == q[0] == r[0]) and (not p[1] == q[1] == r[1]):
            yield q


def corners ( b ) :
    return list(_corners(b))

def _boundary_lengths ( c ) :

    for p, q in zip(c, c[1:] + c[:1]):
        yield max(abs(p[0]-q[0]), abs(p[1]-q[1]))
