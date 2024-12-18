from collections import deque, namedtuple

STEPS = [
    (0, -1),    # 0 top
    (1, 0),     # 1 right
    (0, 1),     # 2 bottom
    (-1, 0),    # 3 left
]

StepState = namedtuple("StepState", ["step", "x", "y"])


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

    def search_path(self, initial):
        queue = deque([initial])
        visited = set()

        while queue:
            curr = queue.popleft()
            if (curr.x, curr.y) in visited:
                continue

            visited.add((curr.x, curr.y))

            if (curr.x, curr.y) == (self.end_x, self.end_y):
                return curr

            for (dx, dy) in STEPS:
                nx, ny = curr.x + dx, curr.y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.blocked:
                    queue.append(StepState(curr.step+1, nx, ny))

        return None


with open('day18.txt') as fl:
    memory = Memory(fl)


memory.search_path(StepState(0, memory.start_x, memory.start_y))

for i in range(1024):
    memory.drop_byte(i)


res = memory.search_path(StepState(0, memory.start_x, memory.start_y))
print(res.step)

for i in range(1024, len(memory.falling_bytes)):
    memory.drop_byte(i)
    res = memory.search_path(StepState(0, memory.start_x, memory.start_y))
    if res is None:
        x, y = memory.falling_bytes[i]
        print(f"{x},{y}")
        break
