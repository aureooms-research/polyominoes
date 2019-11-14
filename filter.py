from itertools import chain
from grid import is_connected
from grid import _neighbors_from_direction
from polyomino import mino_key
from debug import debug

def filter_chiral(minos):
    # TODO
    return minos

def filter_one_sided(minos, sort=True):

    """
        Remove rotations in set of minos.
    """

    vis = set() # visited mino rotation families
    result = set()
    for mino in minos:
        # If we haven't seen a rotation of this mino before,
        # add its rotations to the visisted list
        if mino not in vis:
            mino_rots = mino.rotations()
            vis.update(mino_rots)
            # Add the (maximal rotation of the) mino
            result.add(max(mino_rots, key=mino_key) if sort else mino)
    return result

def filter_free(minos, sort=True):
    """Remove rotations and reflections in the set of minos."""
    vis = set() # visited transformation families
    result = set()
    for mino in minos:
        # If we haven't seen a rotation or reflection of this mino before,
        # add its transforms to the visisted list
        if mino not in vis:
            mino_trans = mino.transforms()
            vis.update(mino_trans)
            # Add the (maximal transform of the) mino
            result.add(max(mino_trans, key=mino_key) if sort else mino)
    return result


def _filter_without_holes ( minos ) :

    """
    Check if outside of polyomino is connected. If not there is a hole.
    """

    for mino in minos:

        n = len(mino)

        whole_grid = set((x,y) for x in range(-1,n+2) for y in range(-1,n+2))

        antimino = whole_grid - mino

        if is_connected(antimino): yield mino

def filter_without_holes ( minos ) :
    return frozenset(_filter_without_holes(minos))

def filter_with_holes ( minos ) :
    return minos - filter_without_holes(minos)

def _filter_with_odd_side_lengths ( minos ):

    for mino in minos:

        debug('polyomino')
        debug('=========')
        debug(mino)
        debug('=========')
        debug(frozenset(mino))

        b = boundary(mino)

        debug(b)

        c = corners(b)

        debug(c)

        if all(map(lambda x: x % 2, _boundary_lengths(c))):
            debug('OK')
            debug('polyomino')
            debug('=========')
            debug(mino)
            debug('=========')
            yield mino

        debug('#####################################')

def filter_with_odd_side_lengths ( minos ):
    return frozenset(_filter_with_odd_side_lengths(minos))

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

    for i in range(n):
        if (0,i) in mino:
            first = (0,i)
            break

    debug("first", first)

    boundary = []

    # those are coordinates of the lattice

    previous = first
    if (first[0],first[1]+1) in mino:
        boundary.append((first[0],first[1]+1))
        second = (first[0],first[1]+1)
    else:
        boundary.append((first[0]+1,first[1]+1))
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

        if current == second and previous == first: break

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
