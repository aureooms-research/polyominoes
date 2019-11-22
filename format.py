import json

def grid(h, w, cells):

    """
        Return boolean-grid representation of this polyomino.
    """

    # Create a blank grid in the shape of the mino
    grid = [[False]*w for row in range(h)]
    # Fill the grid with the values in the mino
    for i, j in cells:
        grid[i][j] = True
    return grid

def to_repr(mino):
    return 'Polyomino({}, height={}, width={})'.format(mino.cells, mino.height, mino.width)

def to_bitstring(mino):
    """
        O(n^2) bits

        >>> from polyomino import empty
        >>> to_bitstring(empty)
        '0 0 '

        >>> from polyomino import singleton
        >>> to_bitstring(singleton)
        '1 1 1'

    """
    bitstring = draw_grid(mino, cell='1', empty='0', sep='', endrow='')
    return '{} {} {}'.format(mino.height, mino.width, bitstring)

def to_coordinates(mino):
    """
        O(n log n) bits

        >>> from polyomino import empty
        >>> to_coordinates(empty)
        '0 0 0 '

        >>> from polyomino import singleton
        >>> to_coordinates(singleton)
        '1 1 1 0 0'

    """
    coordinates = ' '.join(sorted(map(lambda cell: '{} {}'.format(*cell), mino.cells)))
    return '{} {} {} {}'.format(mino.order, mino.height, mino.width, coordinates)

def draw_grid(mino, cell="[]", empty="  ", sep='', endrow="\n"):

    """
        Pretty string of the polyomino.
    """
    result = []
    for row in grid(mino.height, mino.width, mino.cells):
        result.append(sep.join(cell if c else empty for c in row))
    return endrow.join(result)

def to_json_object(mino):

    """

        >>> from polyomino import empty
        >>> to_json_object(empty)
        {'height': 0, 'width': 0, 'cells': []}

        >>> from polyomino import singleton
        >>> to_json_object(singleton)
        {'height': 1, 'width': 1, 'cells': [[0, 0]]}

    """


    cells = sorted(map(list,mino.cells))

    return {
        'height': mino.height,
        'width': mino.width,
        'cells': cells,
    }

def to_json(mino, **kwargs):

    """

        >>> from polyomino import empty
        >>> to_json(empty)
        '{"height": 0, "width": 0, "cells": []}'

        >>> from polyomino import singleton
        >>> to_json(singleton)
        '{"height": 1, "width": 1, "cells": [[0, 0]]}'

    """

    return json.dumps(to_json_object(mino), **kwargs)
