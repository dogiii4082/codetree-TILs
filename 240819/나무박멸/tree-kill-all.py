import copy

dx = [-1, 1, 0, 0, -1, -1, 1, 1]
dy = [0, 0, -1, 1, 1, -1, 1, -1]


def is_tree(x, y):
    return board[x][y] > 0


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


def count_adj_tree(x, y):
    ret = 0
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if not in_range(nx, ny): continue
        if is_tree(nx, ny): ret += 1
    return ret


def grow():
    for x in range(n):
        for y in range(n):
            if not is_tree(x, y): continue
            cnt = count_adj_tree(x, y)
            board[x][y] += cnt


def count_adj_empty(x, y):
    ret = 0
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if not in_range(nx, ny): continue
        if board[nx][ny] == 0: ret += 1
    return ret


def spread():
    tmp = copy.deepcopy(board)

    for x in range(n):
        for y in range(n):
            if not is_tree(x, y): continue
            e = count_adj_empty(x, y)
            if e == 0: continue
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if not in_range(nx, ny): continue
                if board[nx][ny] == 0:
                    tmp[nx][ny] += board[x][y] // e

    return tmp


def count_kill(x, y):
    ret = board[x][y]
    if board[x][y] == 0: return 0
    for i in range(4, 8):
        for k in range(1, K + 1):
            nx = x + dx[i] * k
            ny = y + dy[i] * k

            if not in_range(nx, ny): continue
            # if board[nx][ny] == -1 or board[nx][ny] == 0: break
            if board[nx][ny] <= 0: break

            ret += board[nx][ny]

    return ret


def kill(m, c):
    global ans

    tmp = copy.deepcopy(board)

    cnt, kx, ky = -1, -1, -1
    for x in range(n):
        for y in range(n):
            if not is_tree(x, y): continue

            # print(count_kill(x, y), x, y)
            tmp[x][y] = count_kill(x, y)

            if tmp[x][y] > cnt:
                cnt = tmp[x][y]
                kx = x
                ky = y

    if cnt > 0: ans += cnt

    # print(kx, ky)
    board[kx][ky] = - (m + c)
    for i in range(4, 8):
        for k in range(1, K+1):
            nx = kx + dx[i]*k
            ny = ky + dy[i]*k

            if not in_range(nx, ny): continue
            if board[nx][ny] <= 0 or is_wall[nx][ny]:
                board[nx][ny] = - (m + c)
                break

            board[nx][ny] = - (m + c)


def end_kill(m):    # m년 까지 제초제 존재
    for x in range(n):
        for y in range(n):
            if board[x][y] < 0 and -board[x][y] <= m:
                if is_wall[x][y]: board[x][y] = -1
                else: board[x][y] = 0


def print_board():
    for row in board:
        print(*row)
    print()

if __name__ == "__main__":
    n, M, K, c = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]

    is_wall = [[0 for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if board[x][y] == -1:
                is_wall[x][y] = 1

    ans = 0

    for m in range(1, M+1):
        # print(f'--------{m}년-----------')
        # print()

        grow()
        # print("-------grow------")
        # print_board()

        board = spread()
        # print("-------spread------")
        # print_board()

        kill(m, c)
        # print("-------제초제 뿌리기------")
        # print_board()

        end_kill(m)
        # print("-------제초제 제거------")
        # print_board()

        # print(f'ans: {ans}')

    print(ans)