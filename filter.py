from itertools import chain
from functools import lru_cache
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

def _filter_one_sided(minos, sort=True):

    """
        Remove rotations in set of minos (with history).
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

def _filter_one_sided_mem(minos):

    """
        Remove rotations in set of minos (without history).

        hyp: minos has no duplicates
    """

    for mino in minos:
        mino_rots = mino.rotations()
        # If this mino is maximum amoung its rotations, output it
        if mino == max(mino_rots, key=mino_key):
            yield mino

def _filter_free(minos, sort=True):
    """
        Remove rotations and reflections in the set of minos (with history).
    """
    vis = set() # visited transformation families
    for mino in minos:
        # If we haven't seen a rotation or reflection of this mino before,
        # add its transforms to the visisted list
        if mino not in vis:
            mino_trans = mino.transforms()
            vis.update(mino_trans)
            # Add the (maximal transform of the) mino
            yield max(mino_trans, key=mino_key) if sort else mino

def _filter_free_mem(minos):

    """
        Remove rotations and reflections in the set of minos (without history).

        hyp: minos has no duplicates
    """

    for mino in minos:
        mino_trans = mino.transforms()
        # If this mino is maximum amoung its transformations, output it
        if mino == max(mino_trans, key=mino_key):
            yield mino

@lru_cache(maxsize=None)
def whole_grid ( h, w ) :
    return set((x,y) for x in range(-1,h+1) for y in range(-1,w+1))

@lru_cache(maxsize=None)
def has_topological_property ( condition ) :

    def _cnd ( mino ) :

        antimino = whole_grid(mino.height, mino.width) - mino.cells

        return condition(antimino)

    return _cnd

def _filter_holes ( condition , minos ) :

    return filter(has_topological_property(condition), minos)

def _filter_without_holes ( minos ) :

    """
        Check if outside of polyomino is connected. If not, there is a hole.
    """

    return _filter_holes(is_connected, minos)

def _filter_with_holes ( minos ) :

    """
        Check if outside of polyomino is disconnected. If it is, there is no hole.
    """

    return _filter_holes(lambda x : not is_connected(x), minos)

def _filter_with_odd_side_lengths ( minos ):

    for mino in minos:

        debug('polyomino')
        debug('=========')
        debug(mino)
        debug('=========')
        debug(mino.cells)

        b = boundary(mino.cells, mino.origin)

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
