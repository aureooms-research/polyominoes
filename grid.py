from collections import Counter

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
