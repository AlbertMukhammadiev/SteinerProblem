from itertools import permutations


def generate_paths(n):
    def various_pairs(xs):
        variants = []
        for i in range(len(xs)):
            for j in range(i + 1, len(xs)):
                variants.append((xs[i], xs[j]))

        return variants

    def various_tuples(n):
        xss = [list(range(n))]
        while True:
            xs = xss.pop()
            if len(xs) == 2:
                return map(tuple, xss)
            for subset in various_pairs(xs):
                temp = xs.copy()
                temp.remove(subset[0])
                temp.remove(subset[1])
                temp.insert(0, subset)
                xss.insert(0, temp)

    def get_path(tup, acc):
        if type(tup[0]) is int:
            acc.append(tup)
        else:
            get_path(tup[0], acc)
            if type(tup[1]) is not int:
                get_path(tup[1], acc)

            acc.append(tup)

        return acc

    tuples = various_tuples(n)
    paths = {}
    for tup in tuples:
        paths[tup] = get_path(tup, [])

    return paths