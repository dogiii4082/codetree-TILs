dx = [0, -1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 0, -1, -1, -1, 0, 1, 1, 1]

p_moves = []
pdx = [-1, 0, 1, 0]
pdy = [0, -1, 0, 1]

def get_pacman_moves(cur):
    if len(cur) == 3:
        p_moves.append(cur[:])
        return

    for i in range(4):
        cur += str(i)
        get_pacman_moves(cur)
        cur = cur[:-1]

def clear_sub():
    for x in range(4):
        for y in range(4):
            sub_grid[x][y].clear()

def try_duplicate():
    for x in range(4):
        for y in range(4):
            if not grid[x][y]: continue
            sub_grid[x][y].extend(grid[x][y])

def in_range(x, y):
    return 0 <= x < 4 and 0 <= y < 4

def can_go(x, y):
    if not in_range(x, y): return False
    if (x, y) == (px, py): return False
    if dead_grid[x][y]: return False
    return True

def move_monster():
    nxt_grid = [[[] for _ in range(4)] for _ in range(4)]

    for x in range(4):
        for y in range(4):
            if not grid[x][y]: continue

            for i in grid[x][y]:

                d = i
                nx = x + dx[d]
                ny = y + dy[d]
                while not can_go(nx, ny):
                    d = max(1, (d+1)%9)
                    nx = x + dx[d]
                    ny = y + dy[d]
                    if d == i: break
            
                nxt_grid[nx][ny].append(d)

    return nxt_grid

def pacman_move(t):
    global px, py

    M = 0
    M_dir = ''

    for dir in p_moves:
        visited = [[False for _ in range(4)] for _ in range(4)]
        # dir = 000
        cnt = 0
        x = px
        y = py
        for d in dir:
            x = x + pdx[int(d)]
            y = y + pdy[int(d)]

            if not in_range(x, y): break
            if visited[x][y]: continue

            visited[x][y] = True
            cnt += len(grid[x][y])
        
        if cnt > M:
            M_dir = dir
            M = cnt

    for d in M_dir: # 033
        d = int(d)
        px += pdx[d]
        py += pdy[d]
        if grid[px][py]:
            dead_grid[px][py].extend([t for _ in grid[px][py]])
            grid[px][py].clear()

def dead_clear(t):
    for x in range(4):
        for y in range(4):
            if not dead_grid[x][y]: continue

            dead_grid[x][y] = [i for i in dead_grid[x][y] if i > t-2]

def done_duplicate():
    for x in range(4):
        for y in range(4):
            if not sub_grid[x][y]: continue
            grid[x][y].extend(sub_grid[x][y])

if __name__ == "__main__":
    get_pacman_moves('')

    grid = [[[] for _ in range(4)] for _ in range(4)]
    sub_grid = [[[] for _ in range(4)] for _ in range(4)]
    dead_grid = [[[] for _ in range(4)] for _ in range(4)]

    # Input
    m, T = map(int, input().split())
    px, py = map(int, input().split()); px -= 1; py -= 1
    for _ in range(m):
        x, y, d = map(int, input().split())
        grid[x-1][y-1].append(d)

    # Simulation
    for t in range(1, T+1):
        # print(f'====={t}=====')
        clear_sub()

        # print("=====GRID=====")
        # for row in grid:
        #     print(*row)

        try_duplicate()

        # print("=====try_duplicate=====")
        # for row in sub_grid:
        #     print(*row)

        grid = move_monster()

        # print("=====GRID=====")
        # for row in grid:
        #     print(*row)
        
        pacman_move(t)

        # print("=====GRID=====")
        # for row in grid:
        #     print(*row)

        dead_clear(t)

        # print("=====GRID=====")
        # for row in grid:
        #     print(*row)

        done_duplicate()

        # print(px, py)
        # print("=====GRID=====")
        # for row in grid:
        #     print(*row)
        # print("=====DEAD=====")
        # for row in dead_grid:
        #     print(*row)


    ans = 0
    for x in range(4):
        for y in range(4):
            ans += len(grid[x][y])
    print(ans)