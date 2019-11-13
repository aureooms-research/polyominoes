"""
Functions and classes that involve polyominoes.

Some code stolen (MIT LICENSE) from
https://raw.githubusercontent.com/tesseralis/polyomino/master/polyomino.py
"""
from itertools import chain
from functools import total_ordering
from grid import is_connected
from grid import _neighbors
from grid import _neighbors_from_direction
from collections import Counter
from debug import debug

def _generate(n):
    """
    Generate the fixed n-ominoes.
    """

    if n <= 0:
        return

    # The one monomino
    minos = {Polyomino([(0,0)])}
    yield minos

    # Iteratively add the children of the members of the set before it
    for i in range(n-1):
        minos = childset(minos)
        yield minos

def generate(n):

    for minos in _generate(n):
        pass

    return minos

def childset(minos):
    """Return the set of children of the collection of polyominoes."""
    children = set()
    for mino in minos:
        children.update(mino.children())
    return children

def one_sided(minos, sort=True):
    """Remove rotations in set of minos."""
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

def free(minos, sort=True):
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

## TODO: Figure out how to have the same effect WITHIN the class
## using __eq__, __gt__, __lt__, etc
def mino_key(m):
    """Generate a standard key for a polyomino"""
    #Sort the mino by order, then shape, then 'closeness to top'
    h, w = m.shape
    return (len(m), h/w, sum(2**(i+j*w) for i, j in m))

##@total_ordering
class Polyomino(frozenset):
    """
    Represent a fixed polyomino in space as a set of point tuples.
    """
    def grid(self):
        """Return boolean-grid representation of this polyomino."""
        # Create a blank grid in the shape of the mino
        h, w = self.shape
        grid = [[False]*w for row in range(h)]
        # Fill the grid with the values in the mino
        for i, j in self:
            grid[i][j] = True
        return grid

    def __hash__(self):
        # Just inherit superclass's hashing
        return super().__hash__()

    def __str__(self, cell="[]", empty="  "):
        """
        Pretty string of the polyomino.
        """
        grid = self.grid()
        result = []
        for row in grid:
            result.append("".join(cell if c else empty for c in row))
        return '\n'.join(result)

    def __eq__(self, other):
        """
        Equality to another mino.
        """
        return super().__eq__(other)

    # [properties]
    # TODO: Make O(1), pre-storage?
    @property
    def shape(self):
        """Width and height of a mino"""
        rows, cols = zip(*self)
        return -min(rows)+max(rows)+1, -min(rows)+max(cols)+1
    @property
    def width(self):
        return self.shape[1]
    @property
    def height(self):
        return self.shape[0]

    # [transformations]
    def normalize(self):
        """
        Return a polyomino in normal form (min x,y is zero)
        """
        rows, cols = zip(*self)
        imin, jmin = min(rows), min(cols)
        return self.translate(-imin, -jmin)

    def translate(self, numrows, numcols):
        """Translate by numrows and numcols"""
        return Polyomino((i+numrows, j+numcols) for i, j in self)

    def rotate_left(self):
        """Rotate counterclockwise"""
        return Polyomino((-j, i) for i, j in self).normalize()

    def rotate_half(self):
        """Rotate 180 degrees"""
        return Polyomino((-i, -j) for i, j in self).normalize()

    def rotate_right(self):
        """Rotate clockwise"""
        return Polyomino((j, -i) for i, j in self).normalize()

    def reflect_vert(self):
        """Reflect vertically"""
        return Polyomino((-i, j) for i, j in self).normalize()

    def reflect_horiz(self):
        """Reflect horizontally"""
        return Polyomino((i, -j) for i, j in self).normalize()

    def reflect_diag(self):
        """Reflection across line i==j"""
        return Polyomino((j, i) for i, j in self)

    def reflect_skew(self):
        """Reflection across line i==-j"""
        return Polyomino((-j, -i) for i, j in self).normalize()

    # [Congruent polyominoes]
    def rotations(self):
        """Return rotations of this mino."""
        return [self,
                self.rotate_left(),
                self.rotate_half(),
                self.rotate_right()]

    def transforms(self):
        """Return transformations of this mino."""
        return [self,
                self.rotate_left(),
                self.rotate_half(),
                self.rotate_right(),
                self.reflect_vert(),
                self.reflect_horiz(),
                self.reflect_diag(),
                self.reflect_skew()]

    # TODO: more "pythonic" way of keeping track of symmetry?
    def symmetry(self):
        """
        Return the symmetry sigil of the polyomino.
        '?': No symmetries
        '|-\/': Reflective symmetry across axis
        '%': Twofold rotational symmetry
        '@': Fourfold rotational symmetry
        '+X': Twofold reflective symmetry
        'O': All symmetries
        """
        sym = ''
        if self == self.reflect_horiz():
            sym += '|'
        if self == self.reflect_vert():
            sym += '-'
        if self == self.reflect_diag():
            sym += '\\'
        if self == self.reflect_skew():
            sym += '/'
        if self == self.rotate_half():
            sym += '%'
        if self == self.rotate_left():
            sym += '@'
        if '|-' in sym:
            sym += '+'
        if '\\/' in sym:
            sym += 'X'
        if '@+X' in sym:
            sym += 'O'
        if not sym:
            sym = '?'
        return sym

    def children(self):
        """
        Returns all polyominoes obtained by adding a square to this one.
        """
        childset = set()
        # Get all the neighbors of all the cells
        nbrs = set()
        for square in self:
            nbrs.update(_neighbors(square))
        nbrs -= self
        # Add each neighbor
        for nbr in nbrs:
            new = Polyomino(self | {nbr})
            # Only normalize if we need to
            if nbr[0] == -1:
                new = new.translate(1, 0)
            elif nbr[1] == -1:
                new = new.translate(0, 1)
            childset.add(new)
        return childset

def _without_holes ( minos ) :

    """
    Check if outside of polyomino is connected. If not there is a hole.
    """

    for mino in minos:

        n = len(mino)

        whole_grid = set((x,y) for x in range(-1,n+2) for y in range(-1,n+2))

        antimino = whole_grid - mino

        if is_connected(antimino): yield mino

def without_holes ( minos ) :
    return frozenset(_without_holes(minos))

def _with_odd_side_lengths ( minos ):

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

def with_odd_side_lengths ( minos ):
    return frozenset(_with_odd_side_lengths(minos))

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
