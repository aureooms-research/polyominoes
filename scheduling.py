from collections import Counter

def expand ( targets ) :

    def _deps ( dependencies, key ) :
        if key not in dependencies:
            deps = Counter()
            for target in targets[key]:
                deps.update(_deps(dependencies, target))
            dependencies[key] = deps
        return Counter([key]) | dependencies[key]

    dependencies = {}

    for target in targets: _deps(dependencies, target)

    return dependencies

def needed ( targets, wanted ):

    dependencies = expand(targets)

    cnt = Counter(wanted)

    for target in wanted:

        cnt.update(dependencies[target])

    return cnt
