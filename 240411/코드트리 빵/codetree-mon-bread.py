dr = [1, 0, 0, -1]
dc = [0, 1, -1, 0]


def dist(r1, c1, r2, c2):
    return abs(r1-r2) + abs(c1-c2)


def get_base(sx, sy):   # 2, 3
    bx, by = 0, 0
    m_dist = int(1e9)

    for x in range(1, n+1):
        for y in range(1, n+1):
            if board[x][y] == 1 and dist(x, y, sx, sy) < m_dist:
                bx, by = x, y
                m_dist = dist(x, y, sx, sy)

    return bx, by   # 1, 2


def act_1():
    for idx, [px, py] in enumerate(people[1:]):
        if px < 1 or px > n or py < 1 or py > n: continue

        m_dist = int(1e9)
        sx, sy = stores[idx+1][0], stores[idx+1][1]
        tx, ty = 0, 0
        for i in range(4):
            nx = px + dr[i]
            ny = py + dc[i]

            if nx < 1 or nx > n or ny < 1 or ny > n: continue
            if board[nx][ny] == -int(1e9): continue

            if dist(nx, ny, sx, sy) <= m_dist:
                m_dist = dist(nx, ny, sx, sy)
                tx, ty = nx, ny
        people[idx+1] = [tx, ty]

        if [tx, ty] == [sx, sy]:
            is_end[idx+1] = True
            board[sx][sy] = -int(1e9)



if __name__ == "__main__":
    n, m = map(int, input().split())    # n = 5, m = 3
    board = [[0 for _ in range(n+1)]]
    for _ in range(n):
        row = [0] + list(map(int, input().split()))
        board.append(row)
    # board -> 0: 빈 칸, 1: 베이스 캠프

    people = [[0, 0] for _ in range(m+1)]

    stores = [[]]
    for i in range(1, m+1):
        x, y = map(int, input().split())
        board[x][y] = -i
        stores.append([x, y])

    is_end = [True] + [False for _ in range(m)]

    t = 0
    while True:
        if all(is_end): break

        t += 1

        act_1()

        if t <= m:
            bx, by = get_base(stores[t][0], stores[t][1])
            board[bx][by] = -int(1e9)
            people[t] = [bx, by]

    print(t)