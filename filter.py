from itertools import chain
from grid import is_connected
from grid import boundary
from grid import corners
from grid import _boundary_lengths
from polyomino import mino_key
from debug import debug

def _filter_chiral(minos):

    for mino in minos:

        if mino == mino.reflect_vert(): continue
        if mino == mino.reflect_horiz(): continue
        if mino == mino.reflect_diag(): continue
        if mino == mino.reflect_skew(): continue

        yield mino

def filter_chiral(minos):
    return list(_filter_chiral(minos))

def _filter_one_sided(minos, sort=True):

    """
        Remove rotations in set of minos.
    """

    vis = set() # visited mino rotation families
    for mino in minos:
        # If we haven't seen a rotation of this mino before,
        # add its rotations to the visisted list
        if mino not in vis:
            mino_rots = mino.rotations()
            vis.update(mino_rots)
            # Add the (maximal rotation of the) mino
            yield max(mino_rots, key=mino_key) if sort else mino

def filter_one_sided(minos, sort=True):
    return list(_filter_one_sided(minos,sort=sort))

def _filter_free(minos, sort=True):
    """Remove rotations and reflections in the set of minos."""
    vis = set() # visited transformation families
    for mino in minos:
        # If we haven't seen a rotation or reflection of this mino before,
        # add its transforms to the visisted list
        if mino not in vis:
            mino_trans = mino.transforms()
            vis.update(mino_trans)
            # Add the (maximal transform of the) mino
            yield max(mino_trans, key=mino_key) if sort else mino

def filter_free(minos, sort=True):
    return frozenset(_filter_free(minos,sort=sort))


def _filter_without_holes ( minos ) :

    """
    Check if outside of polyomino is connected. If not there is a hole.
    """

    for mino in minos:

        h, w = mino.shape

        whole_grid = set((x,y) for x in range(-1,h+1) for y in range(-1,w+1))

        antimino = whole_grid - mino

        if is_connected(antimino): yield mino

def filter_without_holes ( minos ) :
    return frozenset(_filter_without_holes(minos))

def _filter_with_holes ( minos ) :
    yield from filter_with_holes( minos )

def filter_with_holes ( minos ) :
    return minos.difference(filter_without_holes(minos))

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
    return list(_filter_with_odd_side_lengths(minos))

filters = {
    'one-sided': _filter_one_sided,
    'free': _filter_free,
    'chiral': _filter_chiral,
    'free without holes': _filter_without_holes,
    'A217595': _filter_with_odd_side_lengths,
}
