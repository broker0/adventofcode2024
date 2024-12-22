from collections import defaultdict


class NumGenerator:
    def __init__(self, secret):
        self.secret = secret

    def next_num(self):
        self.secret = self.secret * 64 ^ self.secret
        self.secret = self.secret % 16777216

        self.secret = self.secret // 32 ^ self.secret
        self.secret = self.secret % 16777216

        self.secret = self.secret * 2048 ^ self.secret
        self.secret = self.secret % 16777216
        return self.secret


with open('day22.txt') as fl:
    secrets = []
    for line in fl:
        secrets.append(int(line.strip()))


sellers_data = []

total_sum = 0
for secret in secrets:
    g = NumGenerator(secret)

    prices = [g.secret % 10]
    for _ in range(2000):
        g.next_num()
        prices.append(g.secret % 10)

    total_sum += g.secret

    changes = [(next_price - prev_price) for (prev_price, next_price) in zip(prices, prices[1:])]
    price_and_change = list((price, change) for (price, change) in zip(prices[1:], changes))
    four_changes = [tuple(price_and_change[i:i + 4]) for i in range(len(price_and_change) - 3)]
    sellers_data.append(four_changes)

print(total_sum)
changes_sum = defaultdict(int)

for (i, data) in enumerate(sellers_data):
    curr_change_set = set()
    for four_change in data:
        change_seq = (four_change[0][1], four_change[1][1], four_change[2][1], four_change[3][1])
        if change_seq not in curr_change_set:
            curr_change_set.add(change_seq)
            changes_sum[change_seq] += four_change[3][0]

print(max(s for s in changes_sum.values()))

