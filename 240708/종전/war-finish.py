dx = [-1, -1, 1, 1]
dy = [1, -1, -1, 1]


def in_range(x, y):
    if x < 0 or x >= n or y < 0 or y >= n: return False
    return True


def get_coordinates(x, y):
    ret = []

    for l_13 in range(1, 4):
        for l_24 in range(1, 4):
            bx, by = x, y
            rx, ry = bx + dx[0] * l_13, by + dy[0] * l_13
            tx, ty = rx + dx[1] * l_24, ry + dy[1] * l_24
            lx, ly = tx + dx[2] * l_13, ty + dy[2] * l_13

            if in_range(bx, by) and in_range(rx, ry) and in_range(tx, ty) and in_range(lx, ly):
                ret.append([(bx, by), (rx, ry), (tx, ty), (lx, ly)])

    return ret


def area_2(coord):
    (bx, by), (rx, ry), (tx, ty), (lx, ly) = coord

    ret = 0
    for x in range(lx):
        for y in range(ty+1):
            if x+y < tx+ty:
                ret += board[x][y]

    return ret


def area_3(coord):
    (bx, by), (rx, ry), (tx, ty), (lx, ly) = coord

    ret = 0
    for x in range(rx+1):
        for y in range(ty+1, n):
            if y-x > ty-tx:
                ret += board[x][y]

    return ret


def area_4(coord):
    (bx, by), (rx, ry), (tx, ty), (lx, ly) = coord

    ret = 0
    for x in range(lx, n):
        for y in range(by):
            if x-y > lx-ly:
                ret += board[x][y]

    return ret


def area_5(coord):
    (bx, by), (rx, ry), (tx, ty), (lx, ly) = coord

    ret = 0
    for x in range(rx+1, n):
        for y in range(by, n):
            if x+y > bx+by:
                ret += board[x][y]

    return ret


def get_area(coord):
    areas = [0 for _ in range(5)]

    areas[1] = area_2(coord)
    areas[2] = area_3(coord)
    areas[3] = area_4(coord)
    areas[4] = area_5(coord)
    areas[0] = tot - (areas[1] + areas[2] + areas[3] + areas[4])

    return areas


if __name__ == "__main__":
    n = int(input())
    board = [list(map(int, input().split())) for _ in range(n)]
    tot = 0
    for row in board:
        tot += sum(row)

    ans = 1e9
    for x in range(2, n):
        for y in range(1, n-1):
            coords = get_coordinates(x, y)

            for coord in coords:
                areas = get_area(coord)
                ans = min(max(areas)-min(areas), ans)

    print(ans)