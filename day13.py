from collections import namedtuple
import re
import math

ClawMachine = namedtuple('ClawMachine', ["ax", "ay", "bx", "by", "dx", "dy"])


def read_claw_machine(fl):
    line = fl.readline()
    if not line:
        return None

    btn_a = re.match(r"Button A: X(\+?\d+), Y(\+?\d+)", line)
    btn_b = re.match(r"Button B: X(\+?\d+), Y(\+?\d+)", fl.readline().strip())
    prize = re.match(r"Prize: X=(\d+), Y=(\d+)", fl.readline().strip())
    fl.readline()

    return ClawMachine(
        int(btn_a[1]), int(btn_a[2]),
        int(btn_b[1]), int(btn_b[2]),
        int(prize[1]), int(prize[2]),
    )


def get_solves1(ax, bx, dx, ay, by, dy):
    xgcd = math.gcd(ax, bx)
    ygcd = math.gcd(ay, by)

    if dx % xgcd:
        return []

    if dy % ygcd:
        return []

    k = []

    for ak in range(100):
        for bk in range(100):
            if ax * ak + bx * bk == dx and ay * ak + by * bk == dy:
                k.append((ak, bk))

    return k


def get_solves2(ax, bx, dx, ay, by, dy):
    xgcd = math.gcd(ax, bx)
    ygcd = math.gcd(ay, by)

    dx += 10000000000000
    dy += 10000000000000

    if dx % xgcd:
        return []

    if dy % ygcd:
        return []

    d = ax*by-ay*bx

    if d == 0:
        return []

    n1 = dx*by-dy*bx
    n2 = ax*dy-ay*dx

    if n1 % d or n2 % d:
        return []

    return [(n1 // d, n2 // d)]


with open('day13.txt') as fl:
    total_cost1 = 0
    total_cost2 = 0
    while m := read_claw_machine(fl):
        if cost := get_solves1(m.ax, m.bx, m.dx, m.ay, m.by, m.dy):
            total_cost1 += cost[0][0]*3+cost[0][1]*1

        if cost := get_solves2(m.ax, m.bx, m.dx, m.ay, m.by, m.dy):
            total_cost2 += cost[0][0]*3+cost[0][1]*1

    print(total_cost1, total_cost2)
