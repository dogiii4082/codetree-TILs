dx = [-1, 1, 0, 0, -1, -1, 1, 1]
dy = [0, 0, -1, 1, 1, -1, 1, -1]

def is_tree(x, y):
    return board[x][y] > 0

def in_range(x, y):
    return 0 <= x < n and 0 <= y < n

def count_adj_tree(x, y):
    return sum(1 for i in range(4) if in_range(x + dx[i], y + dy[i]) and is_tree(x + dx[i], y + dy[i]))

def grow():
    for x in range(n):
        for y in range(n):
            if is_tree(x, y):
                board[x][y] += count_adj_tree(x, y)

def spread():
    tmp = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if is_tree(x, y):
                empty_cells = [(x + dx[i], y + dy[i]) for i in range(4) if in_range(x + dx[i], y + dy[i]) and board[x + dx[i]][y + dy[i]] == 0 and herbicide[x + dx[i]][y + dy[i]] == 0]
                if empty_cells:
                    spread_amount = board[x][y] // len(empty_cells)
                    for nx, ny in empty_cells:
                        tmp[nx][ny] += spread_amount
    for x in range(n):
        for y in range(n):
            board[x][y] += tmp[x][y]

def count_kill(x, y):
    if not is_tree(x, y):
        return 0
    ret = board[x][y]
    for i in range(4, 8):
        for k in range(1, K + 1):
            nx, ny = x + dx[i] * k, y + dy[i] * k
            if not in_range(nx, ny) or board[nx][ny] <= 0:
                break
            ret += board[nx][ny]
    return ret

def kill(m):
    global ans
    max_kill, kx, ky = 0, -1, -1
    for x in range(n):
        for y in range(n):
            if is_tree(x, y):
                kill_count = count_kill(x, y)
                if kill_count > max_kill:
                    max_kill, kx, ky = kill_count, x, y

    if max_kill > 0:
        ans += max_kill
        herbicide[kx][ky] = c
        board[kx][ky] = 0
        for i in range(4, 8):
            for k in range(1, K + 1):
                nx, ny = kx + dx[i] * k, ky + dy[i] * k
                if not in_range(nx, ny) or board[nx][ny] <= 0:
                    break
                herbicide[nx][ny] = c
                board[nx][ny] = 0

def update_herbicide():
    for x in range(n):
        for y in range(n):
            if herbicide[x][y] > 0:
                herbicide[x][y] -= 1

if __name__ == "__main__":
    n, M, K, c = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    herbicide = [[0] * n for _ in range(n)]
    ans = 0

    for m in range(1, M + 1):
        grow()
        spread()
        kill(m)
        update_herbicide()

    print(ans)