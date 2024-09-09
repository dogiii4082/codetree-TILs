import copy
from collections import deque

MAX_M = 300
grid = [[0 for _ in range(5)] for _ in range(5)]
rotate_goal = []
dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]
ans = []

def rotate(x, y, deg):
    next_grid = copy.deepcopy(grid)

    if deg == 90:
        next_grid[x - 1][y - 1] = grid[x + 1][y - 1]
        next_grid[x - 1][y] = grid[x][y - 1]
        next_grid[x - 1][y + 1] = grid[x - 1][y - 1]

        next_grid[x][y - 1] = grid[x + 1][y]
        next_grid[x][y + 1] = grid[x - 1][y]

        next_grid[x + 1][y - 1] = grid[x + 1][y + 1]
        next_grid[x + 1][y] = grid[x][y + 1]
        next_grid[x + 1][y + 1] = grid[x - 1][y + 1]

    elif deg == 180:
        next_grid[x - 1][y - 1] = grid[x + 1][y + 1]
        next_grid[x - 1][y] = grid[x + 1][y]
        next_grid[x - 1][y + 1] = grid[x + 1][y - 1]

        next_grid[x][y - 1] = grid[x][y + 1]
        next_grid[x][y + 1] = grid[x][y - 1]

        next_grid[x + 1][y - 1] = grid[x - 1][y + 1]
        next_grid[x + 1][y] = grid[x - 1][y]
        next_grid[x + 1][y + 1] = grid[x - 1][y - 1]

    else:
        next_grid[x - 1][y - 1] = grid[x - 1][y + 1]
        next_grid[x - 1][y] = grid[x][y + 1]
        next_grid[x - 1][y + 1] = grid[x + 1][y + 1]

        next_grid[x][y - 1] = grid[x - 1][y]
        next_grid[x][y + 1] = grid[x + 1][y]

        next_grid[x + 1][y - 1] = grid[x - 1][y - 1]
        next_grid[x + 1][y] = grid[x][y - 1]
        next_grid[x + 1][y + 1] = grid[x + 1][y - 1]

    return next_grid


def in_range(x, y):
    return 0 <= x < 5 and 0 <= y < 5


def bfs(x, y, visited, grid):

    q = deque([(x, y)])
    visited[x][y] = True
    cnt = 1
    coords = [(x, y)]

    while q:
        x, y = q.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if not in_range(nx, ny): continue
            if visited[nx][ny]: continue

            if grid[nx][ny] == grid[x][y]:
                q.append((nx, ny))
                visited[nx][ny] = True
                cnt += 1
                coords.append((nx, ny))

    return cnt, coords

def start():
    rotate_goal.clear()

    for cx in range(1, 4):
        for cy in range(1, 4):

            for deg in [90, 180, 270]:
                next_grid = rotate(cx, cy, deg)

                visited = [[False for _ in range(5)] for _ in range(5)]
                cnt = 0
                coords = []
                for x in range(5):
                    for y in range(5):
                        tmp_cnt, tmp_coords = bfs(x, y, visited, next_grid)
                        # print(cx, cy, deg, tmp_cnt, tmp_coords)
                        if tmp_cnt >= 3:
                            cnt += tmp_cnt
                            coords.extend(tmp_coords)

                rotate_goal.append((-cnt, deg, cy, cx, coords))

    rotate_goal.sort()


if __name__ == "__main__":
    K, M = map(int, input().split())
    for x in range(5):
        row = list(map(int, input().split()))
        for col in range(5):
            grid[x][col] = row[col]
    nums = deque(list(map(int, input().split())))

    for _ in range(K):
        ans_tmp = 0

        start()
        cnt, deg, y, x, coords = rotate_goal[0]; cnt *= -1
        if cnt < 3: break
        ans_tmp += cnt
        grid = rotate(x, y, deg)
        for i, j in coords:
            grid[i][j] = 0
        coords.sort(key=lambda x: (x[1], -x[0]))
        for i in range(len(coords)):
            num = nums.popleft()
            tx, ty = coords[i]
            grid[tx][ty] = num


        # 유믈 연쇄 획득
        while True:
            cnt = 0
            coords = []
            visited = [[False for _ in range(5)] for _ in range(5)]
            for x in range(5):
                for y in range(5):
                    tmp_cnt, tmp_coords = bfs(x, y, visited, grid)
                    if tmp_cnt >= 3:
                        cnt += tmp_cnt
                        coords.extend(tmp_coords)

            if cnt < 3: break

            coords.sort(key=lambda x: (x[1], -x[0]))
            for i in range(len(coords)):
                num = nums.popleft()
                tx, ty = coords[i]
                grid[tx][ty] = num
            ans_tmp += cnt
        ans.append(ans_tmp)

    print(*ans)