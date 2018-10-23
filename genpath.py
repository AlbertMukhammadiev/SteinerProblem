"""This is an auxiliary module for the module steiner.py
which allows to generate paths of building of Steiner tree.

Functions:
    generate_paths(n) -> filterfalse obj
"""

from itertools import permutations, filterfalse


def generate_paths(n):
    """Build all sorts of ways to select two points.

    Arguments:
    n -- initial number of points
    """
    def update_entry(entry, pair):
        """Update new entry in log by new pair of points

        Arguments:
        entry -- new entry in log
        pair -- chosen pair of points
        """
        entry[0].remove(pair[0])
        entry[0].remove(pair[1])
        entry[0].insert(0, pair)
        entry[1].append(pair)

    def logging(log):
        """Generate all sorts of paths.

        Arguments:
        log -- list of tuples that consist remainder points and done steps
        """
        while True:
            remainders, done_steps = log.pop()
            if len(remainders) == 2:
                log.append((remainders, done_steps))
                return
            
            for pair in permutations(remainders, 2):
                entry = (remainders.copy(), done_steps.copy())
                update_entry(entry, pair)
                log.insert(0, entry)

    log = [(list(range(n)), [])]
    logging(log)
    paths = [entry[1] for entry in log]
    return filterfalse(lambda x: [x[1], x[0]] in paths,paths)


if __name__ == '__main__':
    log = generate_paths(4)
    for i, step in enumerate(log):
        print(i, step)