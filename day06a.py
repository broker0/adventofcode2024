DIRS = {'>': (1, 0), 'v': (0, 1), '<': (-1, 0), '^': (0, -1)}

TURNS = {
    (0, -1): (1, 0),  # N -> E
    (1, 0): (0, 1),  # E -> S
    (0, 1): (-1, 0),  # S -> W
    (-1, 0): (0, -1)  # W -> N
}


def move_guard(area, pos):
    x, y, (sx, sy) = pos
    nx, ny = x + sx, y + sy

    if not (0 <= nx < len(area[0]) and 0 <= ny < len(area)):
        return None
    if area[ny][nx] == '#':
        return x, y, TURNS[(sx, sy)]

    return nx, ny, (sx, sy)


def guard_walk(area, pos):
    unique_pos = set()

    while pos:
        x, y, _ = pos
        unique_pos.add((x, y))
        pos = move_guard(area, pos)

    return len(unique_pos), unique_pos


def check_cycle(area, pos):
    unique_states = set()

    while pos:
        unique_states.add(pos)
        pos = move_guard(area, pos)

        if pos in unique_states:
            return True

    return False


area = []
initial_pos = []

with open('day06.txt') as fl:
    for y, line in enumerate(fl):
        line = line.strip()
        for x, c in enumerate(line):
            if c in DIRS:
                initial_pos.append((x, y, DIRS[c]))
        area.append(line)

total, positions = guard_walk(area, initial_pos[0])
print(total)


cycle_count = sum(
    check_cycle(area[:y] + [area[y][:x] + '#' + area[y][x + 1:]] + area[y + 1:], initial_pos[0]) for (x, y) in positions
)

print(cycle_count)
