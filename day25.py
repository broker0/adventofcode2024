

with open('day25.txt') as fl:
    keys = []
    locks = []

    while True:
        pattern = [
            fl.readline().strip(),
            fl.readline().strip(),
            fl.readline().strip(),
            fl.readline().strip(),
            fl.readline().strip(),
            fl.readline().strip(),
            fl.readline().strip(),
        ]
        rotated = [''.join(row) for row in zip(*pattern)]

        if pattern[0] == '#####' and pattern[6] == '.....':   # lock
            lock = []
            for r in rotated:
                lock.append(len(r.strip('.'))-1)

            locks.append(tuple(lock))
        elif pattern[0] == '.....' and pattern[6] == '#####':    # key
            key = []
            for r in rotated:
                key.append(7-len(r.strip('#'))-1)

            keys.append(tuple(key))
        else:
            raise ValueError

        line = fl.readline()
        if not line:
            break

fit = 0
for key in keys:
    for lock in locks:
        for (k, l) in zip(key, lock):
            if k+l > 5:
                break
        else:
            fit += 1

print(fit)
