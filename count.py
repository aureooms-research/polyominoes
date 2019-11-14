from enumerate import _fixed
from filter import filter_one_sided
from filter import filter_free
from filter import filter_without_holes
from filter import filter_with_odd_side_lengths

FMT = {
    'csv': {
        'sep': ', ',
        'title': ':>20',
        'entry': ':>20',
        'newline': '',
        'endline': '',
        'hline': '',
    },
    'md': {
        'sep': ' | ',
        'title': ':>20',
        'entry': ':>20',
        'newline': '| ',
        'endline': ' |',
        'hline': ':-^20',
    },
}

CSV = FMT['csv']

def main (
        n ,
        format_sep=CSV['sep'],
        format_title=CSV['title'],
        format_entry=CSV['entry'],
        format_newline=CSV['newline'],
        format_endline=CSV['endline'],
        format_hline=CSV['hline'],
        **options
    ) :

    columns = ["order", "fixed", "one-sided", "free", "free without holes",
            "A217595"]

    ncols = len(columns)

    HEADER_FMT = format_newline + format_sep.join(['{'+format_title+'}']*ncols) + format_endline
    header = HEADER_FMT.format(*columns)
    print(header)

    if format_hline:
        HLINE_FMT  = format_newline + format_sep.join(['{'+format_hline+'}']*ncols) + format_endline
        hline = HLINE_FMT.format(*(['']*ncols))
        print(hline)

    ROW_FMT  = format_newline + format_sep.join(['{'+format_entry+'}']*ncols) + format_endline

    for i, fixed_set in enumerate(_fixed(n), 1):

        fixed_len = len(fixed_set)

        one_sided_set = filter_one_sided(fixed_set)
        one_sided_len = len(one_sided_set)

        free_set = filter_free(fixed_set)
        free_len = len(free_set)

        free_without_holes_set = filter_without_holes(free_set)
        free_without_holes_len = len(free_without_holes_set)

        A217595_set = filter_with_odd_side_lengths(free_without_holes_set)
        A217595_len = len(A217595_set)

        row = ROW_FMT.format(i, fixed_len, one_sided_len, free_len, free_without_holes_len, A217595_len)
        print(row)

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

    args = parser.parse_args()
    arguments = vars(args)
    main(args.order, **arguments)
