from filter import _filter_one_sided
from filter import _filter_free
from filter import _filter_chiral
from filter import _filter_without_holes
from filter import _filter_with_odd_side_lengths
from filter import _filter_free

filters = {
    'one-sided': _filter_one_sided,
    'free': _filter_free,
    'chiral': _filter_chiral,
    'free without holes': _filter_without_holes,
    'fixed without holes': _filter_without_holes,
    'A217595': _filter_with_odd_side_lengths,
    'A217595 fixed': _filter_with_odd_side_lengths,
    'A217595 mem': _filter_free,
}

targets = {
    'order': [],
    'fixed': [],
    'one-sided': ['fixed'],
    'free': ['fixed'],
    'chiral': ['free'],
    'free without holes': ['free'],
    'fixed without holes': ['fixed'],
    'A217595': ['free without holes'],
    'A217595 fixed': ['fixed without holes'],
    'A217595 mem': ['A217595 fixed'],
}

