
def check_report(levels):
    steps = [a - b for a, b in zip(levels, levels[1:])]
    return all(1 <= s <= 3 for s in steps) or all(-3 <= s <= -1 for s in steps)


with open("day02.txt", "rt") as fl:
    safe1 = 0
    safe2 = 0

    for line in fl.readlines():
        report = list(map(int, line.strip().split()))

        if check_report(report):
            safe1 += 1
            safe2 += 1
        else:
            for i in range(len(report)):
                new_report = report[:i] + report[i+1:]
                if check_report(new_report):
                    safe2 += 1
                    break

    print(safe1, safe2)
