from polyomino import _generate
from polyomino import one_sided
from polyomino import free
from polyomino import without_holes
from polyomino import with_odd_side_lengths

def main ( n ) :

    HEADER_FMT = '{:>20}, {:>20}, {:>20}, {:>20}, {:>20}, {:>20}'
    ROW_FMT = '{:>20}, {:>20}, {:>20}, {:>20}, {:>20}, {:>20}'

    header = HEADER_FMT.format("order", "fixed", "one-sided", "free", "free without holes", "A217595")

    print(header)

    for i, fixed_set in enumerate(_generate(n), 1):

        fixed_len = len(fixed_set)

        one_sided_set = one_sided(fixed_set)
        one_sided_len = len(one_sided_set)

        free_set = free(fixed_set)
        free_len = len(free_set)

        free_without_holes_set = without_holes(free_set)
        free_without_holes_len = len(free_without_holes_set)

        A217595_set = with_odd_side_lengths(free_without_holes_set)
        A217595_len = len(A217595_set)

        row = ROW_FMT.format(i, fixed_len, one_sided_len, free_len, free_without_holes_len, A217595_len)
        print(row)

if __name__ == '__main__':
    import sys
    n = int(sys.argv[1])
    main(n)
