from itertools import count
from collections import defaultdict

from debug import debug

from enumerate import _fixed_with_offset
from enumerate import _redelmeier
from dependencies import filters
from dependencies import targets
from count import cardinality
from online import links
from scheduling import needed

COLUMNS = (
    "order",
    "fixed",
    "one-sided",
    "free",
    "chiral",
    "free without holes",
    "fixed without holes",
    "A217595",
    "A217595 fixed",
    "A217595 mem",
)

LONGEST_COLUMN_TITLE = max(map(len, COLUMNS))

FMT = {
    'csv': {
        'sep': ', ',
        'title': ':>{}'.format(LONGEST_COLUMN_TITLE),
        'entry': ':>{}'.format(LONGEST_COLUMN_TITLE),
        'newline': '',
        'endline': '',
        'hline': '',
        'linkify': False,
    },
    'md': {
        'sep': ' | ',
        'title': ':>{}'.format(LONGEST_COLUMN_TITLE+28),
        'entry': ':>{}'.format(LONGEST_COLUMN_TITLE+28),
        'newline': '| ',
        'endline': ' |',
        'hline': ':-^{}'.format(LONGEST_COLUMN_TITLE+28),
        'linkify': True,
    },
}

CSV = FMT['csv']

DEFAULT_COLUMNS = (
    "order",
    "fixed",
    "one-sided",
    "free",
    "chiral",
    "free without holes",
    "A217595",
)

def put ( x ) :
    print(x, end='', flush=True)

def main (
        min_order=0 ,
        max_order=None ,
        columns=DEFAULT_COLUMNS,
        format_sep=CSV['sep'],
        format_title=CSV['title'],
        format_entry=CSV['entry'],
        format_newline=CSV['newline'],
        format_endline=CSV['endline'],
        format_hline=CSV['hline'],
        format_linkify=CSV['linkify'],
        show_intermediate=False,
        **options
    ) :

    wanted = frozenset(columns)
    tocompute = needed(targets, columns)
    debug('tocompute', tocompute)

    if show_intermediate:
        wanted = frozenset(tocompute.keys())
        tocompute = needed(targets, wanted)
        columns = list(filter(wanted.__contains__, COLUMNS))

    ncols = len(columns)

    if format_linkify:
        titles = list(map(lambda column: column if column not in links else '[{}]({})'.format(column, links[column]), columns))
    else:
        titles = columns

    # header

    if format_title:
        HEADER_FMT = format_newline + format_sep.join(['{'+format_title+'}']*ncols) + format_endline
        header = HEADER_FMT.format(*titles)
        print(header)

    if format_hline:
        HLINE_FMT  = format_newline + format_sep.join(['{'+format_hline+'}']*ncols) + format_endline
        hline = HLINE_FMT.format(*(['']*ncols))
        print(hline)

    # entries

    events = entries(min_order, max_order, wanted, tocompute)

    _cache = {}

    def retrieve(order, kind):

        while (order, kind) not in _cache:
            k, t, count = next(events)
            _cache[(k, t)] = count

        return _cache[(order, kind)]

    if max_order is None:
        orders = count(min_order)
    else:
        orders = range(min_order, max_order+1)

    for order in orders:

        put(format_newline)

        for j, kind in enumerate(columns):
            if j > 0: put(format_sep)
            value = retrieve(order, kind)
            put(('{'+format_entry+'}').format(value))

        put(format_endline)
        put('\n')

def entries(min_order, max_order, wanted, tocompute):

    it = _fixed_with_offset(min_order)

    _cache = {}

    def default_iter ( ) :
        return lambda key: filters[key](*(_cache[dep] for dep in targets[key]))

    compute_iter = defaultdict(default_iter, {
        'order': lambda key: i,
        'fixed': lambda key: next(it) if max_order is not None and max_order > min_order else _redelmeier(i),
    })


    def default_list ( ) :
        return lambda key: list(compute_iter[key](key))

    compute_list = defaultdict(default_list, {
        'order': lambda key: i,
    })

    def default_counter ( ) :
        return lambda key: cardinality(_cache[key])

    compute_count = defaultdict(default_counter, {
        'order': lambda key: _cache[key],
    })

    for i in count(min_order):

        for target in COLUMNS:

            if target in tocompute:

                if tocompute[target] == 1:
                    _cache[target] = compute_iter[target](target)

                else:
                    _cache[target] = compute_list[target](target)

                if target in wanted:
                    yield (i, target, compute_count[target](target))

if __name__ == '__main__':

    import argparse

    class FormatAction(argparse.Action):
        # adapted from documentation
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, values)
            fmt = FMT[values]
            for key, val in fmt.items():
                nskey = 'format_' + key
                if getattr(namespace, nskey) is None:
                    setattr(namespace, nskey, val)

    parser = argparse.ArgumentParser(description='Generate count table for polyominoes.')
    parser.add_argument('-f', '--format', required=True, choices=('csv', 'md'),
            help='table format', action=FormatAction)

    parser.add_argument('--min-order', type=int, default=0, help='minimum order in the table')
    parser.add_argument('--max-order', type=int, help='maximum order in the table')

    parser.add_argument('--format-sep', help='separator for table format')
    parser.add_argument('--format-title', help='title format for table')
    parser.add_argument('--format-entry', help='entry format for table')
    parser.add_argument('--format-newline', help='newline for table format')
    parser.add_argument('--format-endline', help='endline for table format')
    parser.add_argument('--format-hline', help='hline filler for table format')
    parser.add_argument('--format-linkify', type=bool, help='enable links in table header')

    parser.add_argument('--show-intermediate', action='store_true', help='also print columns for intermediate computations')

    parser.add_argument('--columns', nargs='+', default=DEFAULT_COLUMNS, choices=COLUMNS, help='columns of the table')

    args = parser.parse_args()
    arguments = vars(args)
    main(**arguments)
