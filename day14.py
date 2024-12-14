import re
from collections import namedtuple, defaultdict

Robot = namedtuple("Robot", ["x", "y", "dx", "dy"])


def state_after_steps(state, w, h, steps):
    new_state = []
    for robot in state:
        new_pos = (robot.x + robot.dx * steps) % w, (robot.y + robot.dy * steps) % h
        new_state.append(Robot(*new_pos, robot.dx, robot.dy))

    return new_state


def robots_by_pos(robots):
    result = defaultdict(list)
    for robot in robots:
        result[(robot.x, robot.y)].append(robot)
    return dict(result)


def dump(robots_dict, w, h):
    for y in range(h):
        for x in range(w):
            robots_at_cell = robots_dict.get((x, y), [])
            count = len(robots_at_cell)
            if count == 0:
                print('.', end=' ')
            elif count > 9:
                print('+', end=' ')
            else:
                print(count, end=' ')
        print()


def count_robots(robots, w, h):
    center_x = w // 2
    center_y = h // 2
    quadrant = [0, 0, 0, 0]

    for robot in state_after_steps(robots, w, h, 100):
        x, y = robot.x, robot.y
        if x == center_x or y == center_y:
            continue

        if x < center_x:
            if y < center_y:
                quadrant[0] += 1  # top left
            else:
                quadrant[2] += 1  # right left
        else:
            if y < center_y:
                quadrant[1] += 1  # top right
            else:
                quadrant[3] += 1  # bottom right

    return quadrant


STEPS = [   # clockwise
    (0, -1),    # 0 top
    (1, 0),     # 1 right
    (0, 1),     # 2 bottom
    (-1, 0),    # 3 left
]


def chech_tree(robots):
    neighbors = 0

    pos = robots_by_pos(robots)

    for robot in robots:
        for (dx, dy) in STEPS:
            nx, ny = robot.x + dx, robot.y + dy
            if (nx, ny) in pos:
                neighbors += 1

    return neighbors


with open('day14.txt') as fl:
    robots = []
    w = h = 0
    while line := fl.readline().strip():
        robot = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
        pos = int(robot.group(1)), int(robot.group(2))
        vel = int(robot.group(3)), int(robot.group(4))
        robot = Robot(*pos, *vel)
        robots.append(robot)
        w, h = max(w, robot.x+1), max(h, robot.y+1)

    quadrants = count_robots(robots, w, h)
    print(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3])
    print(len(robots))

    max_neighbors = 0

    for _ in range(1, 1000000):
        robots = state_after_steps(robots, w, h, 1)
        neighbors = chech_tree(robots)
        if neighbors > max_neighbors:
            max_neighbors = neighbors
            print(_, max_neighbors)
            dump(robots_by_pos(robots), w, h)
