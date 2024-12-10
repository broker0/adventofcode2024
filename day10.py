from collections import deque

STEPS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def check_trails1(terrain, initials):
    top_reached = 0

    for (x, y) in initials:
        visited = set()
        queue = deque([(x, y)])

        while queue:
            curr_pos = queue.popleft()
            if curr_pos in visited:
                continue
            visited.add(curr_pos)

            height = terrain[curr_pos]
            if height == 9:
                top_reached += 1

            for (dx, dy) in STEPS:
                npos = (curr_pos[0] + dx, curr_pos[1] + dy)
                if npos in terrain and terrain[npos] == height + 1:
                    queue.append(npos)

    print(top_reached)


def check_trails2(terrain, initials):
    top_reached = 0

    def search_trails(x, y, height):
        tops = 0
        for (dx, dy) in STEPS:
            nx, ny = x+dx, y+dy
            if (nx, ny) in terrain and terrain[(nx, ny)] == height+1:
                if height+1 == 9:
                    tops += 1
                else:
                    tops += search_trails(nx, ny, height+1)

        return tops

    for (x, y) in initials:
        top_reached += search_trails(x, y, terrain[(x, y)])

    print(top_reached)


with open('day10.txt', 'rt') as fl:
    terrain = {}
    initials = set()

    for (y, line) in enumerate(fl):
        for (x, height) in enumerate(line.strip()):
            terrain[(x, y)] = int(height)
            if height == '0':
                initials.add((x, y))

    check_trails1(terrain, initials)
    check_trails2(terrain, initials)
