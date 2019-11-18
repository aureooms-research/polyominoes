"""
Functions and classes that involve polyominoes.

Some code stolen (MIT LICENSE) from
https://raw.githubusercontent.com/tesseralis/polyomino/master/polyomino.py
"""
# from functools import total_ordering
from grid import _neighbors

## TODO: Figure out how to have the same effect WITHIN the class
## using __eq__, __gt__, __lt__, etc
def mino_key(m):
    """
        Generate a standard key for a polyomino.
    """
    #Sort the mino by order, then shape, then 'closeness to top'
    h, w = m.shape
    return (m.order, h, w, sum(2**(i+j*w) for i, j in m))

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
        if self:
            rows, cols = zip(*self)
            return -min(rows)+max(rows)+1, -min(rows)+max(cols)+1
        else:
            return (0,0)
    @property
    def width(self):
        return self.shape[1]
    @property
    def height(self):
        return self.shape[0]

    @property
    def order(self):
        return len(self)

    @property
    def origin(self):
        for i in range(n):
            if (0,i) in self:
                return (0,i)

    # [transformations]
    def corner(self):
        if not self:
            return (0,0)
        rows, cols = zip(*self)
        return (min(rows), min(cols))

    def normalize(self):
        """
        Return a polyomino in normal form (min x,y is zero)
        """
        imin, jmin = self.corner()
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
        if not self:
            return frozenset([Polyomino([(0,0)])])

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
