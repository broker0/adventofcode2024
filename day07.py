import itertools


def calc_result(nums, ops):
    curr_result = nums[0]

    for n, op in zip(nums[1:], ops):
        match op:
            case '+':
                curr_result += n
            case '*':
                curr_result *= n
            case '|':
                curr_result = curr_result * (10 ** len(str(n))) + n

    return curr_result


with open('day07.txt') as fl:
    total_result1 = 0
    total_result2 = 0

    for line in fl:
        eq_result, nums = line.strip().split(":")
        eq_result = int(eq_result)
        nums = list(map(int, nums.split()))

        for ops in itertools.product('+*', repeat=len(nums)-1):
            if eq_result == (result := calc_result(nums, ops)):
                total_result1 += result
                break

        for ops in itertools.product('+*|', repeat=len(nums)-1):
            if eq_result == (result := calc_result(nums, ops)):
                total_result2 += result
                break

    print(total_result1, total_result2)
