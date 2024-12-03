import re

with open("day03.txt", "rt") as fl:
    data = fl.read()
    re = re.compile(r"(mul\((\d+),(\d+)\))|(do\(\))|(don\'t\(\))", re.MULTILINE)
    ops = re.findall(data)

    enable = True
    sum1 = 0
    sum2 = 0

    for op in ops:
        if op[0]:
            sum1 += int(op[1]) * int(op[2])
            if enable:
                sum2 += int(op[1]) * int(op[2])
        elif op[3]:
            enable = True
        elif op[4]:
            enable = False
        else:
            raise ValueError

print(sum1, sum2)
