import heapq
from collections import deque


dx = [0, 1, 0, -1, -1, -1, 1, 1]
dy = [1, 0, -1, 0, -1, 1, 1, -1]


def pick_attacker():
    q = []
    for x in range(1, N+1):
        for y in range(1, M+1):
            if board[x][y] <= 0: continue

            heapq.heappush(q, (board[x][y], -attack_time[x][y], -(x+y), -y, x, y))

    board[q[0][-2]][q[0][-1]] += N+M
    return q[0][-2], q[0][-1]


def pick_target(attacker_x, attacker_y):
    q = []
    for x in range(1, N + 1):
        for y in range(1, M + 1):
            if board[x][y] <= 0 or (x == attacker_x and y == attacker_y): continue

            heapq.heappush(q, (-board[x][y], attack_time[x][y], (x + y), y, x, y))

    return q[0][-2], q[0][-1]


def distance(r1, c1, r2, c2):
    q = deque([r1, c1])
    visited = [[float('inf') for _ in range(M+1)] for _ in range(N+1)]
    visited[r1][c1] = 0
    while q:
        x, y = q.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if nx < 1 or nx > N or ny < 1 or ny > M: continue
            if visited[nx][ny] != float('inf') or board[nx][ny] == 0: continue

            q.append((nx, ny))
            visited[nx][ny] += 1

    return visited[r2][c2]


def laser(attacker_x, attacker_y):
    target_x, target_y = pick_target(attacker_x, attacker_y)

    q = deque([])
    visited = [[False for _ in range(M+1)] for _ in range(N+1)]

    q.append((attacker_x, attacker_y, []))
    visited[attacker_x][attacker_y] = True
    relate_attack[attacker_x][attacker_y] = True
    attack_time[attacker_x][attacker_y] = t
    while q:
        x, y, route = q.popleft()

        for i in range(4):
            nx = x + dx[i] if x + dx[i] <= N else (x + dx[i]) % N
            ny = y + dy[i] if y + dy[i] <= M else (y + dy[i]) % M

            if visited[nx][ny]:
                continue
            if board[nx][ny] <= 0:
                continue

            if nx == target_x and ny == target_y:   # 도달
                relate_attack[nx][ny] = True
                board[nx][ny] -= board[attacker_x][attacker_y]
                for rx, ry in route:
                    board[rx][ry] -= board[attacker_x][attacker_y] // 2
                    relate_attack[rx][ry] = True
                return True

            tmp_route = route[:]
            tmp_route.append((nx, ny))
            q.append((nx, ny, tmp_route))
            visited[nx][ny] = True

    return False


def bomb(attacker_x, attacker_y):
    target_x, target_y = pick_target(attacker_x, attacker_y)
    relate_attack[attacker_x][attacker_y] = True
    attack_time[attacker_x][attacker_y] = t
    board[target_x][target_y] -= board[attacker_x][attacker_y]

    for i in range(8):
        nx = target_x + dx[i] if target_x + dx[i] <= N else (target_x + dx[i]) % N
        ny = target_y + dy[i] if target_y + dy[i] <= N else (target_y + dy[i]) % N

        if board[nx][ny] <= 0: continue

        board[nx][ny] -= board[attacker_x][attacker_y] // 2
        relate_attack[nx][ny] = True


def broken_turret():
    for x in range(1, N+1):
        for y in range(1, M+1):
            if board[x][y] < 0: board[x][y] = 0


def repair_turret():
    for x in range(1, N+1):
        for y in range(1, M+1):
            if relate_attack[x][y] or board[x][y] == 0: continue

            board[x][y] += 1


if __name__ == "__main__":
    N, M, K = map(int, input().split())
    board = [[0 for _ in range(M+1)]]
    for _ in range(N):
        tmp = list(map(int, input().split()))
        board.append([0]+tmp)

    attack_time = [[-1 for _ in range(M+1)] for _ in range(N+1)]
    for t in range(K):
        relate_attack = [[False for _ in range(M+1)] for _ in range(N+1)]

        r, c = pick_attacker()
        relate_attack[r][c] = True
        attack_time[r][c] = t

        can_laser = laser(r, c)
        if not can_laser:
            bomb(r, c)

        broken_turret()

        repair_turret()

    ans = -1
    for x in range(1, N+1):
        for y in range(1, M+1):
            ans = max(ans, board[x][y])
    print(ans)