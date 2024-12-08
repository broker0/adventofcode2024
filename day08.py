import itertools

with open('day08.txt') as fl:
    antennas = {}

    w, h = 0, 0
    for (y, line) in enumerate(fl):
        h = max(h, y)
        line = line.strip()
        for (x, c) in enumerate(line):
            w = max(w, x)
            if c != '.':
                if c not in antennas:
                    antennas[c] = []
                antennas[c].append((x, y))

    antinodes1 = set()
    antinodes2 = set()

    for freq in antennas:
        for (pos1, pos2) in itertools.permutations(antennas[freq], 2):
            dx, dy = pos2[0] - pos1[0], pos2[1] - pos1[1]
            nx, ny = pos2[0] + dx, pos2[1] + dy

            if 0 <= nx <= w and 0 <= ny <= h:
                antinodes1.add((nx, ny))

            nx, ny = pos1[0], pos1[1]
            while 0 <= nx <= w and 0 <= ny <= h:
                antinodes2.add((nx, ny))
                nx += dx
                ny += dy

    print(len(antinodes1), len(antinodes2))
