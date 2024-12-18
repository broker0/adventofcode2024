from collections import deque, namedtuple
import heapq

STEPS = [
    (0, -1),    # 0 top
    (1, 0),     # 1 right
    (0, 1),     # 2 bottom
    (-1, 0),    # 3 left
]


class StepState(namedtuple("_StepState", ["x", "y", "step", "g", "h", "prev"])):
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)


class Memory:
    def __init__(self, fl):
        self.falling_bytes = []
        self.blocked = set()
        self.width, self.height = 0, 0
        self.start_x, self.start_y = 0, 0
        self.tick = 0

        while line := fl.readline().strip():
            x, y = map(int, line.split(','))
            self.falling_bytes.append((x, y))
            self.width = max(self.width, x+1)
            self.height = max(self.height, y+1)

        self.end_x, self.end_y = self.width-1, self.height-1

    def drop_byte(self, n):
        self.blocked.add(self.falling_bytes[n])

    def dump(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == (self.start_x, self.start_y):
                    print("@", end="")
                elif (x, y) in self.blocked:
                    print("#", end="")
                else:
                    print(".", end="")

            print()

    @staticmethod
    def heuristic(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def search_path(self, x, y):
        # Инициализация
        heap = []
        heapq.heappush(heap, StepState(x, y, 0, 0, Memory.heuristic(x, y, self.end_x, self.end_y), None))
        visited = set()

        while heap:
            curr = heapq.heappop(heap)
            if (curr.x, curr.y) in visited:
                continue
            else:
                visited.add((curr.x, curr.y))

            if (curr.x, curr.y) == (self.end_x, self.end_y):
                path = []
                while curr:
                    path.append((curr.x, curr.y))
                    curr = curr.prev
                return path[::-1]

            for (dx, dy) in STEPS:
                nx, ny = curr.x + dx, curr.y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.blocked:
                    g = curr.g + 1
                    h = Memory.heuristic(nx, ny, self.end_x, self.end_y)
                    heapq.heappush(heap, StepState(nx, ny, curr.step + 1, g, h, curr))

        return []


with open('day18.txt') as fl:
    memory = Memory(fl)


for i in range(1024):
    memory.drop_byte(i)

path = memory.search_path(0, 0)
print(len(path)-1)

path = set(path)

for i in range(1024, len(memory.falling_bytes)):
    memory.drop_byte(i)
    if memory.falling_bytes[i] in path:
        path = set(memory.search_path(0, 0))
        if not len(path):
            x, y = memory.falling_bytes[i]
            print(f"{x},{y}")
            break

