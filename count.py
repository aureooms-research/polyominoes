from itertools import count
from enumerate import _fixed
from filter import filter_one_sided
from filter import filter_free
from filter import filter_without_holes
from filter import _filter_with_odd_side_lengths
from online import links
from scheduling import needed

FMT = {
    'csv': {
        'sep': ', ',
        'title': ':>18',
        'entry': ':>18',
        'newline': '',
        'endline': '',
        'hline': '',
        'linkify': False,
    },
    'md': {
        'sep': ' | ',
        'title': ':>46',
        'entry': ':>46',
        'newline': '| ',
        'endline': ' |',
        'hline': ':-^46',
        'linkify': True,
    },
}

CSV = FMT['csv']

COLUMNS = (
    "order",
    "fixed",
    "one-sided",
    "free",
    "free without holes",
    "A217595"
)

TARGETS = {
    'order': [],
    'fixed': [],
    'one-sided': ['fixed'],
    'free': ['fixed'],
    'free without holes': ['free'],
    'A217595': ['free without holes'],
}

def cardinality ( iterable ) :
    return sum(map(lambda x: 1, iterable))

def put ( x ) :
    print(x, end='', flush=True)

def main (
        n ,
        columns=COLUMNS,
        format_sep=CSV['sep'],
        format_title=CSV['title'],
        format_entry=CSV['entry'],
        format_newline=CSV['newline'],
        format_endline=CSV['endline'],
        format_hline=CSV['hline'],
        format_linkify=CSV['linkify'],
        **options
    ) :

    ncols = len(columns)

    wanted = frozenset(columns)

    if format_linkify:
        titles = list(map(lambda column: column if column not in links else '[{}]({})'.format(column, links[column]), columns))
    else:
        titles = columns

    # header

    HEADER_FMT = format_newline + format_sep.join(['{'+format_title+'}']*ncols) + format_endline
    header = HEADER_FMT.format(*titles)
    print(header)

    if format_hline:
        HLINE_FMT  = format_newline + format_sep.join(['{'+format_hline+'}']*ncols) + format_endline
        hline = HLINE_FMT.format(*(['']*ncols))
        print(hline)

    # entries

    events = entries(n, wanted)

    _cache = {}

    def retrieve(order, kind):

        while (order, kind) not in _cache:
            k, t, count = next(events)
            _cache[(k, t)] = count

        return _cache[(order, kind)]

    for i in range(n):

        order = i+1

        put(format_newline)

        for j, kind in enumerate(columns):
            if j > 0: put(format_sep)
            count = retrieve(order, kind)
            put(('{'+format_entry+'}').format(count))

        put(format_endline)
        put('\n')

def entries(n, wanted):

    tocompute = needed(TARGETS, wanted)

    it = _fixed()

    for i in count(1):

        if 'order' in wanted:
            yield (i, 'order', i)

        fixed_set = next(it)

        if 'fixed' in wanted:
            fixed_len = len(fixed_set)
            yield (i, 'fixed', fixed_len)

        if 'one-sided' in tocompute:
            one_sided_set = filter_one_sided(fixed_set)

            if 'one-sided' in wanted:
                one_sided_len = len(one_sided_set)
                yield (i, 'one-sided', one_sided_len)

        if 'free' in tocompute:
            free_set = filter_free(fixed_set)

            if 'free' in wanted:
                free_len = len(free_set)
                yield (i, 'free', free_len)

        if 'free without holes' in tocompute:
            free_without_holes_set = filter_without_holes(free_set)

            if 'free without holes' in wanted:
                free_without_holes_len = len(free_without_holes_set)
                yield (i, 'free without holes', free_without_holes_len)

        if 'A217595' in tocompute:
            A217595_set = _filter_with_odd_side_lengths(free_without_holes_set)
            if 'A217595' in wanted:
                A217595_len = cardinality(A217595_set)
                yield(i, 'A217595', A217595_len)

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
    parser.add_argument('order', metavar='n', type=int,
                        help='maximum order in the table')
    parser.add_argument('-f', '--format', required=True, choices=('csv', 'md'),
            help='table format', action=FormatAction)

    parser.add_argument('--format-sep', help='separator for table format')
    parser.add_argument('--format-title', help='title format for table')
    parser.add_argument('--format-entry', help='entry format for table')
    parser.add_argument('--format-newline', help='newline for table format')
    parser.add_argument('--format-endline', help='endline for table format')
    parser.add_argument('--format-hline', help='hline filler for table format')
    parser.add_argument('--format-linkify', type=bool, help='enable links in table header')

    parser.add_argument('--columns', nargs='+', default=COLUMNS, choices=COLUMNS, help='columns of the table')

    args = parser.parse_args()
    arguments = vars(args)
    main(args.order, **arguments)
