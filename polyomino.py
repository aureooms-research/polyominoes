"""
Functions and classes that involve polyominoes.

Some code stolen (MIT LICENSE) from
https://raw.githubusercontent.com/tesseralis/polyomino/master/polyomino.py
"""
# from functools import total_ordering
from grid import _neighbors
from grid import translate
from grid import _translate
from grid import normalize
from functools import lru_cache
from functools import total_ordering

@lru_cache(maxsize=10000)
def _mino_key(n, h, w, cells):
    #Sort the mino by order, then shape, then 'closeness to top'
    return (n, h, w, sum(2**(i+j*h) for i, j in cells))

def mino_key(m):
    """
        Generate a standard key for a polyomino.
    """
    return _mino_key(m.order, m.height, m.width, m.cells)

@total_ordering
class Polyomino:

    """
        Represent a fixed polyomino in space as a set of point tuples.

        hyp: cells is a frozenset
    """

    def __init__(self, cells, height=None, width=None):

        self.cells = cells

        if height is None or width is None:
            if cells:
                rows, cols = zip(*cells)
                if height is None: height = max(rows)+1
                if width is None: width = max(cols)+1
            else:
                if height is None: height = 0
                if width is None: width = 0

        self.height = height
        self.width = width

    def grid(self):

        """
            Return boolean-grid representation of this polyomino.
        """

        # Create a blank grid in the shape of the mino
        h = self.height
        w = self.width
        grid = [[False]*w for row in range(h)]
        # Fill the grid with the values in the mino
        for i, j in self.cells:
            grid[i][j] = True
        return grid

    def __hash__(self):
        return self.cells.__hash__()

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
        return self.cells.__eq__(other.cells)

    def __lt__(self, other):
        return mino_key(self) < mino_key(other)

    # [properties]

    @property
    def order(self):
        return len(self.cells)

    @property
    def origin(self):
        for i in range(len(self.cells)):
            if (0,i) in self.cells:
                return (0,i)

    @property
    def corner(self):
        if not self.cells:
            return (0,0)
        rows, cols = zip(*self.cells)
        return (min(rows), min(cols))

    def translate(self, numrows, numcols):
        """Translate by numrows and numcols"""
        return Polyomino(translate(self.cells, numrows, numcols), self.height, self.width)

    def rotate_left(self):
        """Rotate counterclockwise"""
        return Polyomino(normalize([(-j, i) for i, j in self.cells]), self.width, self.height)

    def rotate_half(self):
        """Rotate 180 degrees"""
        return Polyomino(normalize([(-i, -j) for i, j in self.cells]), self.height, self.width)

    def rotate_right(self):
        """Rotate clockwise"""
        return Polyomino(normalize([(j, -i) for i, j in self.cells]), self.width, self.height)

    def reflect_vert(self):
        """Reflect vertically"""
        return Polyomino(normalize([(-i, j) for i, j in self.cells]), self.height, self.width)

    def reflect_horiz(self):
        """Reflect horizontally"""
        return Polyomino(normalize([(i, -j) for i, j in self.cells]), self.height, self.width)

    def reflect_diag(self):
        """Reflection across line i==j"""
        return Polyomino(frozenset((j, i) for i, j in self.cells), self.width, self.height)

    def reflect_skew(self):
        """Reflection across line i==-j"""
        return Polyomino(normalize([(-j, -i) for i, j in self.cells]), self.width, self.height)

    # [Congruent polyominoes]
    def rotations(self):
        """Return rotations of this mino."""
        return [self,
                self.rotate_left(),
                self.rotate_half(),
                self.rotate_right()]

    def reflections(self):
        """Return reflections of this mino."""
        return [self,
                self.reflect_vert(),
                self.reflect_horiz(),
                self.reflect_diag(),
                self.reflect_skew()]

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

    def augment(self, cell):

        """
            hyp: cell is a neighbour of self
        """

        cells = self.cells
        height = self.height
        width = self.width

        if cell[0] == height:
            height += 1
        elif cell[1] == width:
            width += 1
        elif cell[0] == -1:
            height += 1
            cells = _translate(cells, 1, 0)
            cell = (0, cell[1])
        elif cell[1] == -1:
            width += 1
            cells = _translate(cells, 0, 1)
            cell = (cell[0], 0)

        newcells = frozenset(cells) | {cell}

        return Polyomino(newcells, height, width)

    def neighbours(self):

        nbrs = set()

        for cell in self.cells: nbrs.update(_neighbors(cell))

        return nbrs - self.cells


    def children(self):
        """
        Returns all polyominoes obtained by adding a square to this one.
        """
        if not self.cells: return {singleton}

        childset = set()
        # Add each neighbor
        for nbr in self.neighbours():
            new = self.augment(nbr)
            childset.add(new)
        return childset

empty = Polyomino(frozenset(), 0, 0)
singleton = Polyomino(frozenset([(0,0)]), 1, 1)
