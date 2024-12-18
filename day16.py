import heapq
from collections import namedtuple, deque

Position = namedtuple("Position", ["x", "y"])
Step = namedtuple("Step", ["pos", "dir"])

STEPS = {
    0: (0, -1),  # ^
    1: (1, 0),   # >
    2: (0, 1),   # v
    3: (-1, 0),  # <
}

TURNS = {
    0: [0, 1, 3],
    1: [1, 0, 2],
    2: [2, 1, 3],
    3: [3, 0, 2],
}

REV_DIR = {
    0: 2,
    1: 3,
    2: 0,
    3: 1,
}


def find_costs(maze, start, initial_dir):
    costs = {Step(Position(x, y), d): 9999999 for (x, y) in maze for d in range(4)}

    initial_step = Step(start, initial_dir)

    queue = []
    heapq.heappush(queue, (0, initial_step))

    while queue:
        curr_cost, curr_step = heapq.heappop(queue)
        if curr_cost > costs[curr_step]:
            continue

        costs[curr_step] = curr_cost

        for dest_dir in TURNS[curr_step.dir]:
            if curr_step.dir == dest_dir:
                dest_cost = curr_cost + 1
                dest_pos = Position(curr_step.pos.x+STEPS[dest_dir][0], curr_step.pos.y+STEPS[dest_dir][1])
            else:
                dest_cost = curr_cost + 1001
                dest_pos = Position(curr_step.pos.x+STEPS[dest_dir][0], curr_step.pos.y+STEPS[dest_dir][1])

            if dest_pos not in maze:
                continue

            dest_step = Step(dest_pos, dest_dir)
            heapq.heappush(queue, (dest_cost, dest_step))

    return costs


def find_paths(maze, start, end):
    s_to_e = find_costs(maze, start, 1)
    best_cost, best_step = get_best_step(s_to_e, end)

    queue = [(best_cost, best_step)]
    visited = set()
    best_path_pos = {best_step.pos}

    while queue:
        curr_score, curr_step = queue.pop(0)
        if curr_step in visited:
            continue

        visited.add(curr_step)

        for (dx, dy) in STEPS.values():
            npos = Position(curr_step.pos.x+dx, curr_step.pos.y+dy)
            for d in STEPS.keys():
                nstep = Step(npos, d)
                if nstep in visited:
                    continue

                if nstep in s_to_e:
                    nscore = s_to_e[nstep]
                    if nstep.dir == curr_step.dir and curr_score == nscore + 1:
                        queue.append((nscore, nstep))
                        best_path_pos.add(nstep.pos)
                    elif nstep.dir != curr_step.dir and curr_score == nscore + 1001:
                        queue.append((nscore, nstep))
                        best_path_pos.add(nstep.pos)

    return best_path_pos


def get_best_step(costs, pos):
    best_cost = 999999
    best_step = None
    for d in range(4):
        step = Step(pos, d)
        if best_step is None or costs[step] < best_cost:
            best_step = step
            best_cost = costs[step]

    return best_cost, best_step


with open('day16.txt') as fl:
    maze = set()

    start = None
    end = None

    for (y, line) in enumerate(fl):
        line = line.strip()
        if not line:
            break

        for (x, tile) in enumerate(line.strip()):
            if tile == 'S':
                start = Position(x, y)
                maze.add((x, y))
            elif tile == 'E':
                end = Position(x, y)
                maze.add((x, y))
            elif tile == '.':
                maze.add((x, y))
            elif tile == '#':
                pass
            else:
                raise ValueError

    costs = find_costs(maze, start, 1)   # > direction
    print(get_best_step(costs, end))

    tiles = find_paths(maze, start, end)
    print(len(tiles))
