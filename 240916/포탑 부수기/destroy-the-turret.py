# import heapq
# from collections import deque


# dx = [0, 1, 0, -1, -1, -1, 1, 1]
# dy = [1, 0, -1, 0, -1, 1, 1, -1]


# def pick_attacker():
#     q = []
#     for x in range(N):
#         for y in range(M):
#             if board[x][y] == 0: continue

#             heapq.heappush(q, (board[x][y], -attack_time[x][y], -(x+y), -y, x, y))

#     board[q[0][-2]][q[0][-1]] += N+M
#     return q[0][-2], q[0][-1]


# def pick_target(attacker_x, attacker_y):
#     q = []
#     for x in range(N):
#         for y in range(M):
#             if board[x][y] == 0 or (x == attacker_x and y == attacker_y): continue

#             heapq.heappush(q, (-board[x][y], attack_time[x][y], (x + y), y, x, y))

#     # if not q: return float('inf'), float('inf')
#     return q[0][-2], q[0][-1]


# def laser(attacker_x, attacker_y):
#     target_x, target_y = pick_target(attacker_x, attacker_y)
#     # if target_x == float('inf') and target_y == float('inf'): return False

#     q = deque([])
#     visited = [[False for _ in range(M)] for _ in range(N)]

#     q.append((attacker_x, attacker_y, []))
#     visited[attacker_x][attacker_y] = True
#     relate_attack[attacker_x][attacker_y] = True
#     attack_time[attacker_x][attacker_y] = t
#     while q:
#         x, y, route = q.popleft()

#         for i in range(4):
#             nx = (x + dx[i]) % N
#             ny = (y + dy[i]) % M

#             if visited[nx][ny]:
#                 continue
#             if board[nx][ny] == 0:
#                 continue

#             if nx == target_x and ny == target_y:   # 도달
#                 relate_attack[nx][ny] = True
#                 board[nx][ny] -= board[attacker_x][attacker_y]
#                 for rx, ry in route:
#                     board[rx][ry] -= board[attacker_x][attacker_y] // 2
#                     relate_attack[rx][ry] = True
#                 return True

#             tmp_route = route[:]
#             tmp_route.append((nx, ny))
#             q.append((nx, ny, tmp_route))
#             visited[nx][ny] = True

#     return False


# def bomb(attacker_x, attacker_y):
#     target_x, target_y = pick_target(attacker_x, attacker_y)
#     if target_x == float('inf') and target_y == float('inf'): return False
#     relate_attack[attacker_x][attacker_y] = True
#     attack_time[attacker_x][attacker_y] = t
#     board[target_x][target_y] -= board[attacker_x][attacker_y]
#     relate_attack[target_x][target_y] = True

#     for i in range(8):
#         nx = (target_x + dx[i]) % N
#         ny = (target_y + dy[i]) % M

#         if board[nx][ny] == 0 or (nx == attacker_x and ny == attacker_y): continue

#         board[nx][ny] -= board[attacker_x][attacker_y] // 2
#         relate_attack[nx][ny] = True

#     # return True

# def broken_turret():
#     for x in range(N):
#         for y in range(M):
#             if board[x][y] < 0: board[x][y] = 0


# def repair_turret():
#     for x in range(N):
#         for y in range(M):
#             if relate_attack[x][y] or board[x][y] == 0: continue

#             board[x][y] += 1


# if __name__ == "__main__":
#     N, M, K = map(int, input().split())
#     board = []
#     for _ in range(N):
#         tmp = list(map(int, input().split()))
#         board.append(tmp)

#     attack_time = [[-1 for _ in range(M)] for _ in range(N)]
#     for t in range(K):
#         relate_attack = [[False for _ in range(M)] for _ in range(N)]

#         r, c = pick_attacker()
#         relate_attack[r][c] = True
#         attack_time[r][c] = t

#         can_laser = laser(r, c)
#         if not can_laser:
#             bomb(r, c)
#             # if not flag: break

#         broken_turret()

#         repair_turret()

#         cnt = 0
#         for x in range(N):
#             for y in range(M):
#                 if board[x][y] != 0: cnt += 1
#         if cnt == 1: break

#     ans = -1
#     for x in range(N):
#         for y in range(M):
#             ans = max(ans, board[x][y])
#     print(ans)
from collections import deque

dx = [0, 1, 0, -1, -1, -1, 1, 1]
dy = [1, 0, -1, 0, 1, -1, 1, -1]


def get_target():
    M_atk = -1
    for x in range(N):
        for y in range(M):
            if grid[x][y] == 0: continue
            if (x, y) == (ax, ay): continue
            M_atk = max(M_atk, grid[x][y])

    tmp = []
    for x in range(N):
        for y in range(M):
            if grid[x][y] == M_atk: tmp.append((x, y))

    tmp.sort(key=lambda x: (final_attack_time[x[0]][x[1]], (x[0] + x[1]), x[1]))
    return tmp[0][0], tmp[0][1]


def get_attacker():
    m_atk = 1e9
    for x in range(N):
        for y in range(M):
            if grid[x][y] == 0: continue
            m_atk = min(m_atk, grid[x][y])

    tmp = []
    for x in range(N):
        for y in range(M):
            if grid[x][y] == m_atk: tmp.append((x, y))

    tmp.sort(key=lambda x: (-final_attack_time[x[0]][x[1]], -(x[0] + x[1]), -x[1]))
    return tmp[0][0], tmp[0][1]


def try_laser():
    q = deque([])
    visited = [[False for _ in range(M)] for _ in range(N)]

    q.append((ax, ay))
    visited[ax][ay] = True
    prev[ax][ay] = (ax, ay)

    while q:
        x, y = q.popleft()

        for i in range(4):
            nx = (x + dx[i] + N) % N
            ny = (y + dy[i] + M) % M

            if visited[nx][ny]: continue
            if grid[nx][ny] == 0: continue

            q.append((nx, ny))
            visited[nx][ny] = True
            prev[nx][ny] = (x, y)


def can_laser():
    return prev[tx][ty] != (None, None)


def laser():
    final_attack_time[ax][ay] = t

    x, y = tx, ty
    path = [(x, y)]
    is_related[x][y] = True

    while prev[x][y] != (x, y):
        path.append(prev[x][y])
        x, y = prev[x][y]
        is_related[x][y] = True
    for x, y in path:
        if (x, y) == (ax, ay): continue
        if (x, y) == (tx, ty):
            grid[x][y] -= grid[ax][ay]
        else:
            grid[x][y] -= (grid[ax][ay]) // 2


def bomb():
    final_attack_time[ax][ay] = t

    grid[tx][ty] -= grid[ax][ay]
    is_related[tx][ty] = True
    is_related[ax][ay] = True

    for i in range(8):
        nx = (tx + dx[i] + N) % N
        ny = (ty + dy[i] + M) % M

        if grid[nx][ny] == 0: continue
        if (nx, ny) == (ax, ay): continue

        grid[nx][ny] -= (grid[ax][ay]) // 2
        is_related[nx][ny] = True


def repair():
    for x in range(N):
        for y in range(M):
            if grid[x][y] == 0: continue
            if is_related[x][y]: continue

            grid[x][y] += 1


def only_one():
    cnt = 0
    for x in range(N):
        for y in range(M):
           if grid[x][y] != 0: cnt += 1
    return cnt == 1

if __name__ == "__main__":
    N, M, K = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(N)]
    final_attack_time = [[0 for _ in range(M)] for _ in range(N)]
    for t in range(1, K+1):
        if only_one():
            break
        # print(f"====={t}턴=====")
        ax, ay = get_attacker()
        # print(f'ax, ay: {ax}, {ay}')
        grid[ax][ay] += N + M

        tx, ty = get_target()
        # print(f'tx, ty: {tx}, {ty}')

        prev = [[(None, None) for _ in range(M)] for _ in range(N)]
        try_laser()

        is_related = [[False for _ in range(M)] for _ in range(N)]
        if can_laser():
            laser()
        else:
            bomb()
        # print("공격")
        # for row in grid:
        #     print(*row)

        for x in range(N):
            for y in range(M):
                grid[x][y] = max(0, grid[x][y])


        repair()
        # print("정비")
        # for row in grid:
        #     print(*row)

    ans = 0
    for row in grid:
        ans = max(ans, max(row))
    print(ans)