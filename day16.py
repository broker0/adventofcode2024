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
                dest_cost = curr_cost + 1000
                dest_pos = curr_step.pos

            if dest_pos not in maze:
                continue

            dest_step = Step(dest_pos, dest_dir)
            heapq.heappush(queue, (dest_cost, dest_step))

    return costs


def find_paths(maze, start, end):
    s_to_e = find_costs(maze, start, 1)
    best_cost, best_step = get_best_step(s_to_e, end)

    e_to_s = find_costs(maze, best_step.pos, REV_DIR[best_step.dir])
    cost = get_best_step(e_to_s, start)
    print(cost)

    cnt = 1
    for (x, y) in maze:
        for d_d in range(4):
            d_step = Step(Position(x, y), d_d)
            if d_step not in s_to_e:
                continue

            for d_r in range(4):
                r_step = Step(Position(x, y), d_r)
                if r_step not in e_to_s:
                    continue

                if s_to_e[d_step] + e_to_s[r_step] == best_cost:
                    # print(d_step, r_step)
                    cnt += 1

    return cnt


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

    # part 2  is not working yet
    print(find_paths(maze, start, end))

