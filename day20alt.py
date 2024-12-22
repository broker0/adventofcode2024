from collections import namedtuple, Counter

STEPS = [
    (0, -1),    # 0 top
    (1, 0),     # 1 right
    (0, 1),     # 2 bottom
    (-1, 0),    # 3 left
]

Racetrack = namedtuple("Racetrack", ["x", "y", "distance"])


def read_racetrack(filename):
    with open(filename) as fl:
        start = None
        track = set()

        for (y, line) in enumerate(fl):
            for (x, tile) in enumerate(line.strip()):
                if tile != '#':
                    track.add((x, y))

                if tile == 'S':
                    start = (x, y)

        racetrack = [Racetrack(*start, len(track)-1)]
        track.discard(start)

        while track:
            for (dx, dy) in STEPS:
                nx, ny = racetrack[-1].x + dx, racetrack[-1].y + dy
                if (nx, ny) in track:
                    racetrack.append(Racetrack(nx, ny, racetrack[-1].distance - 1))
                    track.discard((nx, ny))
                    break

        return racetrack


def count_cheats(track, max_cheat):
    track_idx = {(pos.x, pos.y): pos for pos in track}
    saves = Counter()

    for pos in track:

        for dx in range(-max_cheat, max_cheat + 1):
            for dy in range(-max_cheat, max_cheat + 1):
                cheat_distance = abs(dx) + abs(dy)
                if cheat_distance <= max_cheat:
                    nx, ny = pos.x + dx, pos.y + dy
                    if (nx, ny) not in track_idx:
                        continue

                    cheat_pos = track_idx[(nx, ny)]
                    if cheat_pos.distance >= pos.distance:
                        continue

                    save = pos.distance - cheat_pos.distance - cheat_distance

                    if save <= 0:
                        continue

                    saves[save] += 1

    return saves


def dump_save(saves, limit):
    for (save, count) in sorted(saves.most_common()):
        if save >= limit:
            print(count, "cheats save", save, "saved pico")


track = read_racetrack('day20.txt')

saves = count_cheats(track, 2)
# dump_save(saves, 0)
print(sum(count for (save, count) in saves.most_common() if save >= 100))

saves = count_cheats(track, 20)
# dump_save(saves, 50)
print(sum(count for (save, count) in saves.most_common() if save >= 100))
