from filter import _filter_one_sided
from filter import _filter_one_sided_mem
from filter import _filter_free
from filter import _filter_free_mem
from filter import _filter_chiral
from filter import _filter_without_holes
from filter import _filter_with_odd_side_lengths

filters = {
    'one-sided': _filter_one_sided,
    'one-sided mem': _filter_one_sided_mem,
    'free': _filter_free,
    'free mem': _filter_free_mem,
    'chiral': _filter_chiral,
    'free without holes': _filter_without_holes,
    'free without holes mem': _filter_without_holes,
    'fixed without holes': _filter_without_holes,
    'A217595': _filter_with_odd_side_lengths,
    'A217595 fixed': _filter_with_odd_side_lengths,
    'A217595 mem': _filter_free_mem,
    'A217595 mem 2': _filter_with_odd_side_lengths,
}

targets = {
    'order': [],
    'fixed': [],
    'one-sided': ['fixed'],
    'one-sided mem': ['fixed'],
    'free': ['fixed'],
    'free mem': ['fixed'],
    'chiral': ['free'],
    'free without holes': ['free'],
    'free without holes mem': ['free mem'],
    'fixed without holes': ['fixed'],
    'A217595': ['free without holes'],
    'A217595 fixed': ['fixed without holes'],
    'A217595 mem': ['A217595 fixed'],
    'A217595 mem 2': ['free without holes mem'],
}
