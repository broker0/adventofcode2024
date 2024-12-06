
TURNS = {
    (0, -1): (1, 0),    # N -> E
    (1,  0): (0, 1),    # E -> S
    (0,  1): (-1, 0),   # S -> W
    (-1, 0): (0, -1)    # W -> N
}


def guard_walk(area, w, h, pos):
    cnt = 0
    x, y, (sx, sy) = pos
    unique_pos = {(x, y)}

    while True:
        nx, ny = x+sx, y+sy
        if nx < 0 or nx >= w or ny < 0 or ny >= h:
            return len(unique_pos)

        if (nx, ny) in area:
            sx, sy = TURNS[(sx, sy)]
        else:
            x, y = nx, ny
            unique_pos.add((x, y))


def check_cycle(area, w, h, pos):
    x, y, (sx, sy) = pos
    unique_pos = {(x, y, sx, sy)}

    while True:
        nx, ny = x+sx, y+sy
        if nx < 0 or nx >= w or ny < 0 or ny >= h:
            return False

        if (nx, ny) in area:
            sx, sy = TURNS[(sx, sy)]
        else:
            x, y = nx, ny
            new_pos = (x, y, (sx, sy))

            if new_pos in unique_pos:
                return True

            unique_pos.add(new_pos)


area = set()
initial_pos = []
DIRS = {'>': (1, 0), 'v': (0, 1), '<': (-1, 0), '^': (0, -1)}

with open('day06.txt') as fl:
    w, h = 0, 0
    for y, line in enumerate(fl):
        h = max(h, y)
        for x, c in enumerate(line.strip()):
            w = max(w, x)
            if c == '#':
                area.add((x, y))
            elif c in '>v<^':
                initial_pos.append((x, y, DIRS[c]))


print(guard_walk(area, w + 1, h + 1, initial_pos[0]))

cycle_count = 0

for y in range(h + 1):
    for x in range(w+1):
        if (x, y) not in area:
            new_area = area.copy()
            new_area.add((x, y))
            if check_cycle(new_area, w+1, h+1, initial_pos[0]):
                cycle_count += 1

print(cycle_count)
