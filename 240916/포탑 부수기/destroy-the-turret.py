import heapq
from collections import deque

dx = [0, 1, 0, -1, -1, -1, 1, 1]
dy = [1, 0, -1, 0, 1, -1, 1, -1]


def get_target():
    q = []
    for x in range(N):
        for y in range(M):
            if grid[x][y] == 0 or (x, y) == (ax, ay): continue
            heapq.heappush(q, (-grid[x][y], attack_time[x][y], (x + y), y, x, y))

    # if not q: return float('inf'), float('inf')
    return q[0][-2], q[0][-1]


def get_attacker():
    q = []
    for x in range(N):
        for y in range(M):
            if grid[x][y] == 0: continue
            heapq.heappush(q, (grid[x][y], -attack_time[x][y], -(x + y), -y, x, y))

    ax, ay = q[0][-2], q[0][-1]
    grid[ax][ay] += N + M
    return ax, ay


def try_laser():
    q = deque([(ax, ay)])
    visited = [[False for _ in range(M)] for _ in range(N)]
    visited[ax][ay] = True
    prev[ax][ay] = (ax, ay)

    while q:
        x, y = q.popleft()
        for i in range(4):
            nx, ny = (x + dx[i]) % N, (y + dy[i]) % M
            if visited[nx][ny] or grid[nx][ny] == 0: continue
            q.append((nx, ny))
            visited[nx][ny] = True
            prev[nx][ny] = (x, y)


def laser():
    attack_time[ax][ay] = t
    x, y = tx, ty
    path = []
    while prev[x][y] != (x, y):
        path.append((x, y))
        x, y = prev[x][y]
    path.append((ax, ay))

    for x, y in path:
        is_related[x][y] = True
        if (x, y) == (tx, ty):
            grid[x][y] -= grid[ax][ay]
        elif (x, y) != (ax, ay):
            grid[x][y] -= grid[ax][ay] // 2


def bomb():
    attack_time[ax][ay] = t
    grid[tx][ty] -= grid[ax][ay]
    is_related[tx][ty] = is_related[ax][ay] = True

    for i in range(8):
        nx, ny = (tx + dx[i]) % N, (ty + dy[i]) % M
        if grid[nx][ny] == 0 or (nx, ny) == (ax, ay): continue
        grid[nx][ny] -= grid[ax][ay] // 2
        is_related[nx][ny] = True


def repair():
    for x in range(N):
        for y in range(M):
            if grid[x][y] > 0 and not is_related[x][y]:
                grid[x][y] += 1


def broken_turret():
    for x in range(N):
        for y in range(M):
            grid[x][y] = max(0, grid[x][y])


def only_one():
    return sum(1 for row in grid for cell in row if cell > 0) == 1


if __name__ == "__main__":
    N, M, K = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(N)]
    attack_time = [[0 for _ in range(M)] for _ in range(N)]

    for t in range(1, K + 1):
        ax, ay = get_attacker()
        tx, ty = get_target()

        prev = [[(None, None) for _ in range(M)] for _ in range(N)]
        try_laser()

        is_related = [[False for _ in range(M)] for _ in range(N)]
        if prev[tx][ty] != (None, None):
            laser()
        else:
            bomb()

        broken_turret()
        repair()

        if only_one():
            break

    print(max(max(row) for row in grid))