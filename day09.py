from collections import deque


def pack_files1(files: deque, disk_map: list):
    for (file_id, file_pos, file_size) in reversed(files):
        for i in range(file_size):
            j = disk_map.index(-1)
            if j > file_pos:
                break

            disk_map[j] = disk_map[file_pos+file_size-i-1]
            disk_map[file_pos+file_size-i-1] = -1


def pack_files2(files: deque, gaps: deque, disk_map: list):
    for (file_id, file_pos, file_size) in reversed(files):
        for i in range(len(gaps)):
            if gaps[i][1] >= file_size and file_pos > gaps[i][0]:
                gap_pos, gap_size = gaps[i]
                gaps[i] = (gap_pos+file_size, gap_size-file_size)

                for j in range(file_size):
                    disk_map[gap_pos+j] = disk_map[file_pos+j]
                    disk_map[file_pos+j] = -1

                break


with open('day09.txt') as fl:
    packed_disk_map = fl.readline().strip()

    files = deque()
    gaps = deque()
    position = 0
    disk_map = []

    for (i, n) in enumerate(packed_disk_map):
        if i % 2:
            gaps.append((position, int(n)))
            position += int(n)
            disk_map.extend([-1]*int(n))
        else:
            files.append((i//2, position, int(n)))
            position += int(n)
            disk_map.extend([i//2]*int(n))

    disk_map1 = disk_map.copy()
    pack_files1(files, disk_map1)
    print(sum(i*v for (i, v) in enumerate(disk_map1) if v >= 0))

    pack_files2(files, gaps, disk_map)
    print(sum(i*v for (i, v) in enumerate(disk_map) if v >= 0))
