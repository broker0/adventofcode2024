from collections import Counter


def blink(stones):
    new_stones = Counter()
    for (stone, stone_count) in stones.items():
        if stone == 0:
            new_stones[1] += stone_count
        elif len(str(stone)) % 2 == 0:
            digits = str(stone)
            stone1 = digits[:len(digits) // 2]
            stone2 = digits[len(digits) // 2:]
            new_stones[int(stone1)] += stone_count
            new_stones[int(stone2)] += stone_count
        else:
            new_stones[stone * 2024] += stone_count

    return new_stones


def blinks(stones, count):
    for _ in range(count):
        stones = blink(stones)

    return sum(stones.values())


with open('day11.txt', 'rt') as fl:
    stones = Counter(map(int, fl.readline().strip().split()))

    print(blinks(stones, 25))
    print(blinks(stones, 75))
