
def check_report(levels):
    steps = [a - b for a, b in zip(levels, levels[1:])]
    return all(1 <= s <= 3 for s in steps) or all(-3 <= s <= -1 for s in steps)


with open("day02.txt", "rt") as fl:

    reports = []
    for line in fl.readlines():
        levels = list(map(int, line.strip().split()))
        reports.append(levels)

    safe1 = 0
    safe2 = 0

    for report in reports:
        is_safe = check_report(report)

        if is_safe:
            safe1 += 1
            safe2 += 1
        else:
            for i in range(len(report)):
                new_report = report[:i] + report[i+1:]
                is_safe = check_report(new_report)
                if is_safe:
                    safe2 += 1
                    break

    print(safe1, safe2)
