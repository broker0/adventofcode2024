
class Computer:
    def __init__(self, a, b, c, code):
        self.a = a
        self.b = b
        self.c = c
        self.code = code
        self.ip = 0
        self.output = []

    def read_next(self):
        if self.ip >= len(self.code):
            return None

        v = self.code[self.ip]
        self.ip += 1
        return v

    def get_opcode(self):
        return self.read_next()

    def get_operand(self, opcode):
        v = self.read_next()
        if v is None:
            return None

        # opcodes BXL and JNZ has literal operands
        if opcode in [1, 3]:
            return v

        # combo operands
        match v:
            case 0 | 1 | 2 | 3:
                return v

            case 4:
                return self.a

            case 5:
                return self.b

            case 6:
                return self.c

            case 7:
                raise ValueError

    def step(self):
        opcode = self.get_opcode()
        operand = self.get_operand(opcode)
        if opcode is None or operand is None:
            return False

        match opcode:
            case 0:     # adv
                # print(f"adv {operand}")
                self.a = int(self.a // (2 ** operand))

            case 1:     # bxl
                # print(f"bxl {operand}")
                self.b = self.b ^ operand

            case 2:     # bst
                # print(f"bst {operand}")
                self.b = operand & 7

            case 3:     # jnz
                # print(f"jnz {operand}")
                if self.a != 0:
                    self.ip = operand

            case 4:     # bxc
                # print(f"bxc {operand} (ignore)")
                self.b ^= self.c

            case 5:     # out
                # print(f"out {operand}")
                v = operand & 7
                self.output.append(v)
                pass

            case 6:     # bdv
                # print(f"bdv {operand}")
                self.b = int(self.a // (2 ** operand))

            case 7:     # cdv
                # print(f"cdb {operand}")
                self.c = int(self.a // (2 ** operand))

        return True

    def run(self):
        while self.step():
            pass

    def reset(self):
        self.ip = 0

    def dump(self):
        print(f"IP: {self.ip} A: {self.a}, B: {self.b}, C: {self.c}")
        print(f"output: {",".join(map(str, self.output))}")
        print('---')


def get_digit(num, pos, radix):
    digit = (num // (radix ** pos)) % radix
    return digit


def set_digit(num, pos, v, radix):
    digit = (num // (radix ** pos)) % radix
    return num + (v - digit) * (radix ** pos)


def find_common_positions(lists):
    length = len(lists[0])
    common_positions = []

    for i in range(length):
        current_element = lists[0][i]
        if not all(sublist[i] == current_element for sublist in lists):
            common_positions.append(i)

    return common_positions


def find_A(comp, s):
    comp.reset()


with open('day17.txt') as fl:
    a = int(fl.readline().strip().split(': ')[1])
    b = int(fl.readline().strip().split(': ')[1])
    c = int(fl.readline().strip().split(': ')[1])
    fl.readline()
    prog = list(map(int, fl.readline().strip().split(': ')[1].split(',')))

    comp = Computer(a, b, c, prog)

    comp.run()
    print(",".join(map(str, comp.output)))

    A = 8**(len(prog)-1)

    candidates = [{A}]

    found = set()

    for i in reversed(range(len(prog))):
        # print(f"checking {i} {candidates[-1]}")
        good = set()
        for A in candidates[-1]:
            for v in range(8):
                A = set_digit(A, i, v, 8)
                comp = Computer(A, b, c, prog)
                comp.run()

                if len(comp.output) == len(comp.code):
                    if comp.code[i] == comp.output[i]:
                        good.add(A)
                        # print(f"found {v} for {i} pos {A:016o}", comp.output, comp.a, comp.b, comp.c, comp.code)
                        if comp.code == comp.output:
                            # print(f"found {v} for {i} pos {A:016o}", comp.output, comp.a, comp.b, comp.c, comp.code)
                            found.add(A)

        candidates.append(good)

    print(min(found))
