import re

with open("day03.txt", "rt") as fl:
    data = fl.read()
    re = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)", re.MULTILINE)

    enabled = 1
    sum1 = 0
    sum2 = 0

    for match in re.finditer(data):
        op = match.group()
        if op.startswith("mul"):
            x, y = map(int, match.groups())
            sum1 += x * y
            sum2 += (x * y) * enabled
        elif op.startswith("do()"):
            enabled = 1
        elif op.startswith("don't()"):
            enabled = 0
        else:
            raise ValueError

print(sum1, sum2)
