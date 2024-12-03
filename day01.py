from collections import Counter

l1 = []
l2 = []
with open("day01.txt", "rt") as fl:
    for line in fl.readlines():
        left, right = line.strip().split()
        l1.append(int(left))
        l2.append(int(right))

l1.sort()
l2.sort()

d = sum([abs(l-r) for (l, r) in zip(l1, l2)])
print(d)


cnt = Counter(l2)
d = sum([l*cnt[l] for l in l1])
print(d)
