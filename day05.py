from collections import deque


def check_update(update, rules):
    page_indices = {page: idx for idx, page in enumerate(update)}

    for a, b in rules:
        if a in page_indices and b in page_indices:
            if page_indices[a] > page_indices[b]:
                return False

    return True


def sort_update(update, rules):
    next_pages = {page: set() for page in update}
    in_pages = {page: 0 for page in update}

    for a, b in rules:
        if a in update and b in update:
            if b not in next_pages[a]:
                next_pages[a].add(b)
                in_pages[b] += 1

    queue = deque([page for page in update if in_pages[page] == 0])
    sorted_pages = []

    while queue:
        current_page = queue.popleft()
        sorted_pages.append(current_page)
        for next_page in next_pages[current_page]:
            in_pages[next_page] -= 1
            if in_pages[next_page] == 0:
                queue.append(next_page)

    return sorted_pages


with open("day05.txt", "rt") as fl:
    rules = []
    while line := fl.readline().strip():
        a, b = map(int, line.split('|'))
        rules.append((a, b))

    updates = []
    while line := fl.readline().strip():
        pages = list(map(int, line.split(',')))
        updates.append(pages)

    sum1 = 0
    sum2 = 0

    for update in updates:
        if check_update(update, rules):
            sum1 += update[len(update)//2]
        else:
            new_update = sort_update(update, rules)
            sum2 += new_update[len(new_update)//2]


print(sum1, sum2)
