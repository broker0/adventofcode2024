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
            self.width = max(len(line)*2, self.width)

            for (x, tile) in enumerate(line.strip()):
                if tile == '#':
                    self.terrain[(x*2, y)] = '#'
                    self.terrain[(x*2+1, y)] = '#'
                elif tile == 'O':
                    self.terrain[(x*2, y)] = '['
                    self.terrain[(x*2+1, y)] = ']'
                elif tile == '@':
                    self.terrain[(x*2, y)] = '.'
                    self.terrain[(x*2+1, y)] = '.'
                    self.x, self.y = x*2, y
                elif tile == '.':
                    self.terrain[(x*2, y)] = '.'
                    self.terrain[(x*2+1, y)] = '.'
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
                    raise ValueError
            print()

    def find_free_place_h(self, x, y, dx, dy):
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

    def move_robot_h(self, direction):
        is_moved_box = False
        dx, dy = STEPS[direction]
        nx, ny = self.x + dx, self.y + dy

        ntile = self.terrain.get((nx, ny), None)

        if ntile is None or ntile == '#':
            return False

        if ntile in '[]':
            new_box_pos = self.find_free_place_h(nx, ny, dx, dy)
            if new_box_pos is None:
                return False

            for cx in range(new_box_pos[0], nx, -dx):
                self.terrain[(cx, self.y)] = self.terrain[(cx-dx, self.y)]

            self.terrain[(nx, ny)] = '.'
            is_moved_box = True

        self.x, self.y = nx, ny

        return is_moved_box

    def move_box(self, x, y, dy):
        self.terrain[(x, y+dy)] = self.terrain[(x, y)]
        self.terrain[(x+1, y+dy)] = self.terrain[(x+1, y)]
        # self.terrain[(x, y+dy)] = '['
        # self.terrain[(x+1, y+dy)] = ']'
        self.terrain[(x, y)] = '.'
        self.terrain[(x+1, y)] = '.'

    def check_box_move(self, x, y, dy):

        boxes = []
        checked = set()

        def check(bx, by):
            if (bx, by) in checked:
                return True
            checked.add((bx, by))

            tl = self.terrain[(bx, by+dy)]
            tr = self.terrain[(bx+1, by+dy)]

            if tl == '#' or tr == '#':
                return False

            if tl == '[' and not check(bx, by+dy):
                return False

            if tl == ']' and not check(bx-1, by+dy):
                return False

            if tr == '[' and not check(bx+1, by+dy):
                return False

            boxes.append((bx, by))
            return True

        if check(x, y):
            return boxes

        return None

    def affected_boxes(self, x, y, dy):
        boxes = self.check_box_move(x, y, dy)
        return boxes

    def move_robot_v(self, direction):
        dx, dy = STEPS[direction]
        nx, ny = self.x + dx, self.y + dy

        ntile = self.terrain.get((nx, ny), None)

        if ntile is None or ntile == '#':
            return False

        if ntile == '.':
            self.x, self.y = nx, ny
            return False

        if ntile == '[':
            boxes = self.affected_boxes(nx, ny, dy)
        elif ntile == ']':
            boxes = self.affected_boxes(nx-1, ny, dy)
        else:
            raise ValueError

        if boxes is None:
            return False

        for box in boxes:
            self.move_box(*box, dy)

        self.x, self.y = nx, ny

        return True

    def move_robot(self, direction):
        if direction == '<' or direction == '>':
            return self.move_robot_h(direction)
        else:
            return self.move_robot_v(direction)

    def gps_sum(self):
        return sum(y*100+x for ((x, y), tile) in self.terrain.items() if tile == '[')


with open('day15.txt') as fl:
    warehouse = Warehouse(fl)

    moves = ''
    for line in fl:
        moves += line.strip()

    for (i, move) in enumerate(moves):
        if warehouse.move_robot(move):
            pass

    print(warehouse.gps_sum())
