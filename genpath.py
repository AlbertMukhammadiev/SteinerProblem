from itertools import permutations, filterfalse


def generate_paths(n):
    def update_entry(entry, pair):
        entry[0].remove(pair[0])
        entry[0].remove(pair[1])
        entry[0].insert(0, pair)
        entry[1].append(pair)

    def logging(log):
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
    

log = generate_paths(4)
for i, step in enumerate(log):
    print(i, step)