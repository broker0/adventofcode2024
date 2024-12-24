from itertools import combinations, permutations


def calculate(wires, gates):
    visited = set()
    curr_path = set()

    def has_cycle(wire):
        if wire in curr_path:
            return True
        if wire in visited:
            return False

        visited.add(wire)
        curr_path.add(wire)

        if wire in gates:
            w1, op, w2 = gates[wire]
            if w1 in gates and has_cycle(w1):
                return True
            if w2 in gates and has_cycle(w2):
                return True

        curr_path.remove(wire)
        return False

    def get_value(wire):
        if wire in wires:
            return wires[wire]

        w1, op, w2 = gates[wire]

        if w1 not in wires:
            wires[w1] = get_value(w1)

        if w2 not in wires:
            wires[w2] = get_value(w2)

        if op == 'OR':
            wires[wire] = wires[w1] | wires[w2]
        elif op == 'XOR':
            wires[wire] = wires[w1] ^ wires[w2]
        elif op == 'AND':
            wires[wire] = wires[w1] & wires[w2]

        return wires[wire]

    for o in gates.keys():
        if has_cycle(o):
            return -1, -1, -1

    for o in gates.keys():
        if o not in wires:
            get_value(o)

    x = "".join((str(wires[w]) for w in sorted([k for k in wires.keys() if k.startswith('x')], reverse=True)))
    y = "".join((str(wires[w]) for w in sorted([k for k in wires.keys() if k.startswith('y')], reverse=True)))
    z = "".join((str(wires[w]) for w in sorted([k for k in wires.keys() if k.startswith('z')], reverse=True)))

    # print(x, y, z)
    return int(x, 2), int(y, 2), int(z, 2)


def p1(wires, gates):
    wires = {w: v for (w, v) in wires}
    gates = {o: (w1, op, w2) for (o, w1, op, w2) in gates}

    x, y, z = calculate(wires, gates)
    return z


def p2(wires, gates):
    wires = {w: v for (w, v) in wires}
    gates = {o: (w1, op, w2) for (o, w1, op, w2) in gates}

    g = tuple(sorted(gates.keys()))

    cnt = 0
    for (g1, g2, g3, g4, g5, g6, g7, g8) in permutations(g, 8):
        cnt += 1

        # print(cnt, g1, g2, g3, g4, g5, g6, g7, g8)
        if not cnt % 10000:
            print(cnt)

        # wires_temp = wires.copy()
        # gates_temp = gates.copy()
        # x, y, z = calculate(wires_temp, gates_temp)
        # print((g1, g2, g3, g4), x, y, z)
        # if x+y == z:
        #     print(g1, g2, g3, g4)
        #     break
        #
        # wires_temp = wires.copy()
        # gates_temp = gates.copy()
        # gates_temp[g2], gates_temp[g3] = gates[g3], gates[g2]
        # x, y, z = calculate(wires_temp, gates_temp)
        # print((g1, g3, g2, g4), x, y, z)
        # if x+y == z:
        #     print(g1, g2, g3, g4)
        #     break
        #
        # wires_temp = wires.copy()
        # gates_temp = gates.copy()
        # gates_temp[g2], gates_temp[g4] = gates[g4], gates[g2]
        # x, y, z = calculate(wires_temp, gates_temp)
        # print((g1, g4, g3, g2), x, y, z)
        # if x+y == z:
        #     print(g1, g2, g3, g4)
        #     break

        # print("----")


    print(cnt)


with open('day24.txt') as fl:
    wires = []
    while line := fl.readline().strip():
        wire, value = line.split(': ')
        wires.append((wire, int(value)))

    gates = []
    wires_remap = {}

    while line := fl.readline().strip():
        w1, op, w2, _, o = line.split(' ')
        w1, w2 = sorted((w1, w2))
        gates.append((o, w1, op, w2))


print(p1(wires, gates))
# print(p2(wires, gates))
