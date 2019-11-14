
links = { }

def _add (a):
    link = 'https://oeis.org/{}'.format(a)
    links[a] = link
    return link

links['M1424'] = links['N0560'] = links['free without holes'] = _add('A000104')
links['M1425'] = links['N0561'] = links['free'] = _add('A000105')
links['M4226'] = links['N1767'] = links['free with holes'] = _add('A001419')
links['M1749'] = links['N0693'] = links['one-sided'] = _add('A000988')
links['M1639'] = links['N0641'] = links['fixed'] = _add('A001168')
links['chiral'] = _add('A030228')
links['free without holes with odd side length'] = _add('A217595')
