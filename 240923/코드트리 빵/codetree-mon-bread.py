# from collections import deque


# dr = [1, 0, 0, -1]
# dc = [0, 1, -1, 0]


# def dist(r1, c1, r2, c2):
#     visited = [[False for _ in range(n+1)] for _ in range(n+1)]
#     dist_board = [[float('inf') for _ in range(n+1)] for _ in range(n+1)]

#     q = deque([(r1, c1)])
#     visited[r1][c1] = True
#     dist_board[r1][c1] = 0

#     while q:
#         x, y = q.popleft()

#         for i in range(4):
#             nx = x + dr[i]
#             ny = y + dc[i]

#             if nx < 1 or nx > n or ny < 1 or ny > n: continue
#             if visited[nx][ny]: continue
#             if board[nx][ny] == -int(1e9): continue

#             visited[nx][ny] = True
#             q.append((nx, ny))
#             dist_board[nx][ny] = dist_board[x][y] + 1

#     # return abs(r1-r2) + abs(c1-c2)
#     return dist_board[r2][c2]

# def get_base(sx, sy):   # 2, 3
#     bx, by = 0, 0
#     m_dist = int(1e9)

#     for x in range(1, n+1):
#         for y in range(1, n+1):
#             if board[x][y] == -int(1e9): continue

#             if board[x][y] == 1 and dist(x, y, sx, sy) < m_dist:
#                 bx, by = x, y
#                 m_dist = dist(sx, sy, x, y)

#     return bx, by   # 1, 2


# def act_1():
#     cant = []
#     for idx, [px, py] in enumerate(people[1:]):
#         if is_end[idx+1]: continue
#         if px < 1 or px > n or py < 1 or py > n: continue

#         m_dist = int(1e9)
#         sx, sy = stores[idx+1][0], stores[idx+1][1]
#         tx, ty = 0, 0
#         for i in range(4):
#             nx = px + dr[i]
#             ny = py + dc[i]

#             if nx < 1 or nx > n or ny < 1 or ny > n: continue
#             if board[nx][ny] == -int(1e9): continue

#             if dist(nx, ny, sx, sy) <= m_dist:
#                 m_dist = dist(nx, ny, sx, sy)
#                 tx, ty = nx, ny
#         people[idx+1] = [tx, ty]

#         if [tx, ty] == [sx, sy]:
#             is_end[idx+1] = True
#             cant.append([sx, sy])
#             # board[sx][sy] = -int(1e9)
#     for x, y in cant:
#         board[x][y] = -int(1e9)


# if __name__ == "__main__":
#     n, m = map(int, input().split())    # n = 5, m = 3
#     board = [[0 for _ in range(n+1)]]
#     for _ in range(n):
#         row = [0] + list(map(int, input().split()))
#         board.append(row)
#     # board -> 0: 빈 칸, 1: 베이스 캠프

#     people = [[0, 0] for _ in range(m+1)]

#     stores = [[]]
#     for i in range(1, m+1):
#         x, y = map(int, input().split())
#         board[x][y] = -i
#         stores.append([x, y])

#     is_end = [True] + [False for _ in range(m)]

#     t = 0
#     while True:
#         if all(is_end): break
#         # if t == 5: break

#         t += 1

#         act_1()

#         cant = []
#         if t <= m:
#             bx, by = get_base(stores[t][0], stores[t][1])
#             # board[bx][by] = -int(1e9)
#             cant.append([bx, by])
#             people[t] = [bx, by]
#         for x, y in cant:
#             board[x][y] = -int(1e9)
#     print(t)

from collections import deque

dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]


def distance(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)


def is_camp(x, y):
    return grid[x][y] == 1


def get_near_camp(sx, sy, pid):
    min_dist = int(1e9)
    cx, cy = 0, 0

    for x in range(1, n+1):
        for y in range(1, n+1):
            if not is_camp(x, y): continue
            if is_end[x][y]: continue

            if bfs(x, y, pid) < min_dist:
                min_dist = bfs(x, y, pid)
                cx = x
                cy = y

    return cx, cy


def go_to_camp(pid):
    sx, sy = SX[pid], SY[pid]
    cx, cy = get_near_camp(sx, sy, pid)

    PX[pid] = cx
    PY[pid] = cy
    is_end[cx][cy] = True


def in_grid(pid):
    px = PX[pid]
    py = PY[pid]

    return 1 <= px <= n and 1 <= py <= n


def in_range(x, y):
    return 1 <= x <= n and 1 <= y <= n


def bfs(sx, sy, pid):
    q = deque([])
    dist = [[int(1e9) for _ in range(n+1)] for _ in range(n+1)]

    q.append((sx, sy))
    dist[sx][sy] = 0

    while q:
        x, y = q.popleft()

        if x == SX[pid] and y == SY[pid]:
            return dist[x][y]

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if not in_range(nx, ny): continue
            if dist[nx][ny] != int(1e9): continue
            if is_end[nx][ny]: continue

            q.append((nx, ny))
            dist[nx][ny] = dist[x][y] + 1

    return dist[SX[pid]][SY[pid]]


def go_to_store(pid):
    px = PX[pid]
    py = PY[pid]
    min_dist = int(1e9)

    tx, ty = 0, 0
    for i in range(4):
        nx = px + dx[i]
        ny = py + dy[i]

        if not in_range(nx, ny): continue
        if is_end[nx][ny]: continue

        if min_dist > bfs(nx, ny, pid):
            tx = nx
            ty = ny
            min_dist = bfs(nx, ny, pid)

    PX[pid] = tx
    PY[pid] = ty


def arrive_store(pid):
    return PX[pid] == SX[pid] and PY[pid] == SY[pid]


def all_arive():
    for pid in range(1, m+1):
        if not arrive_store(pid): return False
    return True


if __name__ == "__main__":
    n, m = map(int, input().split())
    PX = [0 for _ in range(m+1)]
    PY = [0 for _ in range(m+1)]
    SX = [0]
    SY = [0]
    grid = [[0 for _ in range(n+1)]]
    is_end = [[False for _ in range(n+1)] for _ in range(n+1)]
    for _ in range(n):
        grid.append([0] + list(map(int, input().split())))
    for _ in range(m):
        x, y= map(int, input().split())
        SX.append(x)
        SY.append(y)

    t = 0
    while True:
        if all_arive() or t == 10:
            break
        t += 1

        # print(f'====={t}=====')

        # 1번
        for pid in range(1, m+1):
            if arrive_store(pid): continue
            if in_grid(pid): go_to_store(pid)

        # 2번
        for pid in range(1, m+1):
            if arrive_store(pid): is_end[PX[pid]][PY[pid]] = True

        # 3번
        if t <= m:
            go_to_camp(t)

        # print("=====is_end=====")
        # for row in is_end[1:]:
        #     print(*row[1:])
        #
        # print("=====PX, PY=====")
        # print(PX)
        # print(PY)
        # print()
    print(t)