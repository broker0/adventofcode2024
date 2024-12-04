
def check_xmas1(x, y, dx, dy, data):
    mask = "XMAS"
    steps = [
        (1, 0), (0, 1), (-1, 0), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1),
    ]

    match = 0
    for (sx, sy) in steps:
        for d in range(len(mask)):
            cx, cy = x + sx*d, y + sy*d
            if cx < 0 or cx >= dx or cy < 0 or cy >= dy or data[cy][cx] != mask[d]:
                break
        else:
            match += 1

    return match


def check_xmas2(x, y, dx, dy, data):
    if x < 1 or y < 1 or x >= dx-1 or y >= dy-1:
        return 0

    if data[y][x] != 'A':
        return 0

    if not ((data[y-1][x-1], data[y+1][x+1]) in (('M', 'S'), ('S', 'M'))):
        return 0

    if not ((data[y-1][x+1], data[y+1][x-1]) in (('M', 'S'), ('S', 'M'))):
        return 0

    return 1


with open("day04.txt", "rt") as fl:
    lines = []
    for line in fl:
        lines.append(line.strip())

    dx = len(lines[0])
    dy = len(lines)

    total_xmas1 = 0
    total_xmas2 = 0
    for x in range(dx):
        for y in range(dy):
            total_xmas1 += check_xmas1(x, y, dx, dy, lines)
            total_xmas2 += check_xmas2(x, y, dx, dy, lines)

    print(total_xmas1, total_xmas2)
