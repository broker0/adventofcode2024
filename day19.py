
def try_arrange(design, towels):
    cache = {'': 1}

    def search(design):
        if design in cache:
            return cache[design]

        # print(design)

        cnt = 0
        for towel in towels:
            if design.startswith(towel):
                design_remain = design[len(towel):]
                cnt += search(design_remain)

        cache[design] = cnt
        return cnt

    return search(design)


with open('day19.txt') as fl:
    towels = set(fl.readline().strip().split(', '))
    fl.readline()

    designs = []
    while line := fl.readline().strip():
        designs.append(line)

    # print(designs)
    # print(towels)

    count1 = 0
    count2 = 0
    for design in designs:
        cnt = try_arrange(design, towels)
        if cnt:
            count1 += 1
        count2 += cnt

    print(f"{count1}")
    print(f"{count2}")
