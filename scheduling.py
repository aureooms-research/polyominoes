
def expand ( targets ) :

    def _deps ( dependencies, key ) :
        if key not in dependencies:
            deps = frozenset()
            for target in targets[key]:
                deps = deps.union(_deps(dependencies, target))
            dependencies[key] = deps
        return dependencies[key].union([key])

    dependencies = {}

    for target in targets: _deps(dependencies, target)

    return dependencies

def needed ( targets, wanted ):

    dependencies = expand(targets)

    return wanted.union(*(dependencies[target] for target in wanted))
