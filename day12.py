from collections import defaultdict

STEPS = [   # clockwise
    (0, -1),    # 0 top
    (1, 0),     # 1 right
    (0, 1),     # 2 bottom
    (-1, 0),    # 3 left
]


ORT_STEPS = {
    0: ((1, 0), (-1, 0)),
    1: ((0, 1), (0, -1)),
    2: ((1, 0), (-1, 0)),
    3: ((0, 1), (0, -1)),
}


def get_plant_region(terrain, x, y):
    curr_plant = terrain[(x, y)]
    region = set()

    def scan_adjacent(x, y):
        if terrain.get((x, y), None) == curr_plant:
            region.add((x, y))
            for (dx, dy) in STEPS:
                nx, ny = x+dx, y+dy
                if (nx, ny) not in region:
                    scan_adjacent(nx, ny)

    scan_adjacent(x, y)

    return region


def get_area_and_perimeter(plant_regions):
    areas = defaultdict(list)

    for plant in plant_regions.keys():
        for area in plant_regions[plant]:
            curr_area, curr_perimeter = 0, 0

            for (x, y) in area:
                perimeter = 4

                for (dx, dy) in STEPS:
                    nx, ny = x+dx, y+dy
                    if (nx, ny) in area:
                        perimeter -= 1

                curr_area, curr_perimeter = (curr_area+1, curr_perimeter+perimeter)

            areas[plant].append((curr_area, curr_perimeter))

    return areas


def get_free_sides(region, x, y):
    plant = terrain[(x, y)]
    sides = set()

    for (i, (dx, dy)) in enumerate(STEPS):
        nx, ny = x+dx, y+dy
        if (nx, ny) not in region:
            sides.add((x, y, i))

    return sides


def get_area_and_sides(terrain, plant_regions, w, h):
    sides = defaultdict(list)

    for plant in plant_regions.keys():
        for region in plant_regions[plant]:
            free_sided = set()
            for (x, y) in region:
                free_sided |= get_free_sides(region, x, y)

            # print(free_sided)
            sections = 0
            if plant == 'S':
                pass

            # print(plant, free_sided, region, sections)

            while free_sided:
                x, y, side = free_sided.pop()

                queue = [(x, y)]
                while queue:
                    x, y = queue.pop()
                    for (dx, dy) in ORT_STEPS[side]:
                        nx, ny = x+dx, y+dy
                        if (nx, ny, side) in free_sided:
                            queue.append((nx, ny))
                            free_sided.remove((nx, ny, side))

                sections += 1

            # print(plant, free_sided, region, sections)

            sides[plant].append((len(region), sections))

    return sides


with open('day12.txt') as fl:
    terrain = {}
    w, h = 0, 0

    for (y, line) in enumerate(fl):
        h = max(y+1, h)
        for (x, plant) in enumerate(line.strip()):
            w = max(x+1, w)
            terrain[(x, y)] = plant

    plant_regions = defaultdict(list)
    scanned = set()

    for y in range(h):
        for x in range(w):
            if (x, y) in scanned:
                continue

            curr_plant = terrain[(x, y)]
            plants = get_plant_region(terrain, x, y)
            scanned |= plants
            plant_regions[curr_plant].append(plants)

    areas_and_perimeters = get_area_and_perimeter(plant_regions)
    print(sum(sum(area * perimeter for (area, perimeter) in areas_and_perimeters[plant]) for plant in areas_and_perimeters.keys()))

    sections = get_area_and_sides(terrain, plant_regions, w, h)
    print(sum(sum(area * perimeter for (area, perimeter) in sections[plant]) for plant in sections.keys()))