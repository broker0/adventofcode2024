import heapq
from collections import namedtuple, Counter, defaultdict

STEPS = [
    (0, -1),    # 0 top
    (1, 0),     # 1 right
    (0, 1),     # 2 bottom
    (-1, 0),    # 3 left
]


class StepState(namedtuple("_StepState", ["x", "y", "step", "g", "h", "prev"])):
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)


class Racetrack:
    def __init__(self, fl):
        self.maze = set()
        self.walls = set()

        self.start = None
        self.end = None
        self.width = self.height = 0

        for (y, line) in enumerate(fl):
            line = line.strip()
            if not line:
                break

            for (x, tile) in enumerate(line.strip()):
                self.width = max(self.width, x + 1)
                self.height = max(self.height, y + 1)

                if tile == 'S':
                    self.start = (x, y)
                    self.maze.add((x, y))
                elif tile == 'E':
                    self.end = (x, y)
                    self.maze.add((x, y))
                elif tile == '.':
                    self.maze.add((x, y))
                elif tile == '#':
                    self.walls.add((x, y))
                else:
                    raise ValueError

    @staticmethod
    def heuristic(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def search_path(self, x, y):
        heap = []
        heapq.heappush(heap, StepState(x, y, 0, 0, Racetrack.heuristic(x, y, *self.end), None))
        visited = set()

        while heap:
            curr = heapq.heappop(heap)
            if (curr.x, curr.y) in visited:
                continue
            else:
                visited.add((curr.x, curr.y))

            if (curr.x, curr.y) == self.end:
                path = []
                while curr:
                    path.append(StepState(curr.x, curr.y, curr.step, curr.g, curr.h, None))
                    curr = curr.prev
                return path[::-1]

            for (dx, dy) in STEPS:
                nx, ny = curr.x + dx, curr.y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.walls:
                    g = curr.g + 1
                    h = Racetrack.heuristic(nx, ny, *self.end)
                    heapq.heappush(heap, StepState(nx, ny, curr.step + 1, g, h, curr))

        return []

    def cheats1(self, path):
        saves = Counter()
        passed = set()
        original_cost = len(path)-1
        steps = {(step.x, step.y): step for step in path}

        for (i, step) in enumerate(path):
            print(i, len(path))
            passed.add((step.x, step.y))

            for (dx1, dy1) in STEPS:
                nx1, ny1 = step.x+dx1, step.y+dy1
                # if (nx1, ny1) not in self.walls:
                #     continue

                for (dx2, dy2) in STEPS:
                    nx2, ny2 = nx1 + dx2, ny1 + dy2

                    if (nx2, ny2) in self.maze and (nx2, ny2) not in passed:
                        if (nx2, ny2) not in steps:
                            raise ValueError

                        new_step = steps[(nx2, ny2)]

                        new_path = path[new_step.step:]
                        new_cost = i + 2 + len(new_path)-1
                        if new_cost < original_cost:
                            saves[original_cost-new_cost] += 1

        return saves

    def dijkstra(self, start_x, start_y):
        steps_to = {wall: 999999 for wall in self.walls}
        steps_to[(start_x, start_y)] = 1

        queue = [(1, (start_x, start_y))]

        while queue:
            curr_steps, (curr_x, curr_y) = heapq.heappop(queue)

            if curr_steps > steps_to[(curr_x, curr_y)]:
                continue

            if curr_steps > 30:
                continue

            for (dx, dy) in STEPS:
                nx, ny = curr_x + dx, curr_y + dy
                if (nx, ny) not in self.walls:
                    continue

                new_steps = curr_steps + 1

                if new_steps < steps_to[(nx, ny)]:
                    steps_to[(nx, ny)] = new_steps
                    heapq.heappush(queue, (new_steps, (nx, ny)))

        return {(x, y): steps for ((x, y), steps) in steps_to.items() if steps != 999999}


    def cheats2(self, path):
        saves = Counter()
        passed = set()
        original_cost = len(path)-1
        steps = {(step.x, step.y): step for step in path}

        for (i, step) in enumerate(path):
            passed.add((step.x, step.y))

            for dx in range(-20, 21):
                for dy in range(-20, 21):
                    cheat_steps = abs(dx) + abs(dy)
                    if cheat_steps <= 20:
                        nx, ny = step.x + dx, step.y + dy
                        if (nx, ny) in self.maze and (nx, ny) not in passed:
                            if (nx, ny) not in steps:
                                raise ValueError

                            new_step = steps[(nx, ny)]

                            new_path = path[new_step.step:]
                            new_cost = i + cheat_steps + len(new_path) - 1
                            if new_cost < original_cost:
                                saves[original_cost - new_cost] += 1

        return saves

    def dump(self, path, c1=None, c2=None):
        path = {(step.x, step.y) for step in path}

        for y in range(self.height):
            for x in range(self.width):
                if c1 == (x, y):
                    print("1", end="")
                elif c2 == (x, y):
                    print("2", end="")
                elif (x, y) in path:
                    print("O", end="")
                elif (x, y) in self.walls:
                    print("#", end="")
                else:
                    print(".", end="")

            print()


with open('day20.txt') as fl:
    track = Racetrack(fl)

path = track.search_path(*track.start)
print(len(path))
saves = track.cheats1(path)

print("====")
save_cnt = 0
for save_time in sorted(saves.keys()):
    if save_time >= 100:
        # print(saves[save_time], "cheat that save", save_time, "picoseconds")
        save_cnt += saves[save_time]

print(save_cnt)

saves = track.cheats2(path)
save_cnt = 0

for save_time in sorted(saves.keys()):
    if save_time >= 100:
        # print(saves[save_time], "cheat that save", save_time, "picoseconds")
        save_cnt += saves[save_time]

print(save_cnt)
