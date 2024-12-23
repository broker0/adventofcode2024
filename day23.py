from collections import defaultdict
from itertools import combinations

network = defaultdict(set)

with open('day23.txt') as fl:
    while line := fl.readline().strip():
        pc1, pc2 = line.split('-')
        network[pc1].add(pc2)
        network[pc2].add(pc1)

triples = set()
for pc in network:
    neighbours = network[pc]
    for pc1, pc2 in combinations(neighbours, 2):
        if pc2 in network[pc1]:
            # print(sorted([pc, pc1, pc2]))
            triples.add(tuple(sorted([pc, pc1, pc2])))


print(sum(1 for triple in triples if any(pc.startswith('t') for pc in triple)))


connected_groups = set()

for pc in network:
    neighbours = network[pc]
    for group_size in range(1, len(neighbours)):
        for group in combinations(neighbours, group_size):
            # print(f"{pc} -> {group}")
            if all(pc2 in network[pc1] for pc1, pc2 in combinations(group, 2)):
                connected_groups.add(tuple(sorted([pc] + list(group))))


max_group = max(connected_groups, key=len)
print(",".join(sorted(max_group)))
