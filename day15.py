import copy

STEPS = {
    '^': (0, -1),
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
}


class Warehouse:
    def __init__(self, fl):
        self.terrain = {}
        self.width, self.height = 0, 0
        self.x, self.y = None, None

        for (y, line) in enumerate(fl):
            line = line.strip()
            if not line:
                break

            self.height = max(y+1, self.height)
            self.width = max(len(line), self.width)

            for (x, tile) in enumerate(line.strip()):
                if tile == '#':
                    self.terrain[(x, y)] = '#'
                elif tile == 'O':
                    self.terrain[(x, y)] = 'O'
                elif tile == '@':
                    self.terrain[(x, y)] = '.'
                    self.x, self.y = x, y
                elif tile == '.':
                    self.terrain[(x, y)] = '.'
                else:
                    raise ValueError

    def dump(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.terrain.get((x, y), None)
                if (x, y) == (self.x, self.y):
                    print('@', end='')
                elif tile is not None:
                    print(tile, end='')
                else:
                    print('.', end='')
            print()

    def find_free_place(self, x, y, dx, dy):
        while True:
            nx, ny = x + dx, y + dy
            tile = self.terrain.get((nx, ny), None)

            if tile is None:
                return None

            if tile == '#':
                return None

            if tile == '.':
                return nx, ny

            x, y = nx, ny

    def move_robot(self, direction):
        is_moved_box = False
        dx, dy = STEPS[direction]
        nx, ny = self.x + dx, self.y + dy
        ntile = self.terrain.get((nx, ny), None)

        if ntile is None or ntile == '#':
            return False

        if ntile == 'O':
            new_box_pos = self.find_free_place(nx, ny, dx, dy)
            if new_box_pos is None:
                return False

            self.terrain[new_box_pos] = 'O'
            self.terrain[(nx, ny)] = '.'
            is_moved_box = True

        self.x, self.y = nx, ny

        return is_moved_box

    def gps_sum(self):
        return sum(y*100+x for ((x, y), tile) in self.terrain.items() if tile == 'O')


with open('day15.txt') as fl:
    warehouse = Warehouse(fl)

    moves = ''
    for line in fl:
        moves += line.strip()

    for (i, move) in enumerate(moves):
        if warehouse.move_robot(move):
            pass

    print(warehouse.gps_sum())
