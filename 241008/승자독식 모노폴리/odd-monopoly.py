# 1. 아무도 독점 계약을 맺지 않은 칸
# 2. 본인이 독점 계약한 칸

# 상, 하, 좌, 우

dx = [0, -1, 1, 0, 0]
dy = [0, 0, 0, -1, 1]


def in_range(x, y):
    return 0 <= x < N and 0 <= y < N


def move():
    nxt_contract_grid = [row[:] for row in contract_grid]
    for x in range(N):
        for y in range(N):
            if nxt_contract_grid[x][y] == 0: nxt_contract_grid[x][y] = 30

    for pid in range(1, M+1):
        if is_end[pid]: continue

        x = X[pid]
        y = Y[pid]
        d = D[pid]

        dir = priority[pid][d]

        for i in dir:
            nx = x + dx[i]
            ny = y + dy[i]

            if not in_range(nx, ny): continue

            if contract_grid[nx][ny] == 0:      # 아무도 독점 계약 X
                X[pid] = nx
                Y[pid] = ny

                if nxt_contract_grid[nx][ny] > pid:
                    nxt_contract_grid[nx][ny] = pid
                    is_end[contract_grid[nx][ny]] = True
                else:
                    is_end[pid] = True

                time_grid[nx][ny] = K
                break

        else:
            for i in dir:
                nx = x + dx[i]
                ny = y + dy[i]

                if not in_range(nx, ny): continue

                if contract_grid[nx][ny] == pid:
                    X[pid] = nx
                    Y[pid] = ny
                    time_grid[nx][ny] = K
                    break

    for x in range(N):
        for y in range(N):
            if nxt_contract_grid[x][y] == 30: nxt_contract_grid[x][y] = 0

    return nxt_contract_grid


def time():
    for x in range(N):
        for y in range(N):
            if time_grid[x][y] == 0: continue
            time_grid[x][y] -= 1


def is_only_one():
    for pid in range(2, M+1):
        if not is_end[pid]: return False
    return True


if __name__ == "__main__":
    N, M, K = map(int, input().split())
    X = [0 for _ in range(M+1)]
    Y = [0 for _ in range(M+1)]
    is_end = [False for _ in range(M+1)]
    contract_grid = [list(map(int, input().split())) for _ in range(N)]
    time_grid = [[0] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if not contract_grid[x][y]: continue
            time_grid[x][y] = K
            X[contract_grid[x][y]] = x
            Y[contract_grid[x][y]] = y
    priority = [[[]] for _ in range(M+1)]
    D = [0] + list(map(int, input().split())) # [4, 1, 1, 3]
    for pid in range(1, M+1):
        for d in range(4):
            dir = list(map(int, input().split()))
            priority[pid].append(dir)

    for t in range(1, 1000):
        # print(f'====={t}=====')
        time()
        contract_grid = move()

        # print("CONTRACT_GRID")
        # for row in contract_grid:
        #     print(*row)
        # print()
        # print("TIME_GRID")
        # for row in time_grid:
        #     print(*row)
        # print()
        # print(is_end)
        # print()
        if is_only_one():
            print(t)
            break

    else:
        print(-1)