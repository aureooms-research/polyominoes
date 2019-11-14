Enumeration of Polyominoes
==

> ENUMARETE DAZ LATTICE ANIMALZ

[![License](https://img.shields.io/github/license/aureooms-research/polyominoes.svg)](https://raw.githubusercontent.com/aureooms-research/polyominoes/master/LICENSE)
[![Build](https://img.shields.io/travis/aureooms-research/polyominoes/master.svg)](https://travis-ci.org/aureooms-research/polyominoes/branches)
[![GitHub issues](https://img.shields.io/github/issues/aureooms-research/polyominoes.svg)](https://github.com/aureooms-research/polyominoes/issues)

```py
pypy3 count.py 13 -f csv
```

  |                                          order |               [fixed](https://oeis.org/A00168) |          [one-sided](https://oeis.org/A000988) |               [free](https://oeis.org/A000105) | [free without holes](https://oeis.org/A000104) |            [A217595](https://oeis.org/A217595) |
  | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- |
  |                                              1 |                                              1 |                                              1 |                                              1 |                                              1 |                                              1 |
  |                                              2 |                                              2 |                                              1 |                                              1 |                                              1 |                                              0 |
  |                                              3 |                                              6 |                                              2 |                                              2 |                                              2 |                                              1 |
  |                                              4 |                                             19 |                                              7 |                                              5 |                                              5 |                                              1 |
  |                                              5 |                                             63 |                                             18 |                                             12 |                                             12 |                                              2 |
  |                                              6 |                                            216 |                                             60 |                                             35 |                                             35 |                                              4 |
  |                                              7 |                                            760 |                                            196 |                                            108 |                                            107 |                                              7 |
  |                                              8 |                                           2725 |                                            704 |                                            369 |                                            363 |                                             12 |
  |                                              9 |                                           9910 |                                           2500 |                                           1285 |                                           1248 |                                             35 |
  |                                             10 |                                          36446 |                                           9189 |                                           4655 |                                           4460 |                                             55 |
  |                                             11 |                                         135268 |                                          33896 |                                          17073 |                                          16094 |                                            144 |
  |                                             12 |                                         505861 |                                         126759 |                                          63600 |                                          58937 |                                            335 |
  |                                             13 |                                        1903890 |                                         476270 |                                         238591 |                                         217117 |                                            710 |


## Credits

The code was originally derived from
[tesseralis/polyomino](https://github.com/tesseralis/polyomino).
