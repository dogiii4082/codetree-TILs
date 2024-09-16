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
            if (x, y) == (ax, ay): continue
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
            nx = (x + dx[i]) % N
            ny = (y + dy[i]) % M

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
        nx = (tx + dx[i]) % N
        ny = (ty + dy[i]) % M

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