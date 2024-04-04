dx = [1, -1, 0, 0, 1, -1, 1, -1]
dy = [0, 0, -1, 1, 1, -1, -1, 1]

def grow(x, y):
    cnt = 0

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]

        if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
        if board[nx][ny] == 0 or board[nx][ny] == -1 or int(board[nx][ny]) != board[nx][ny]: continue

        cnt += 1

    return cnt

def new_tree(x, y, board, prev):
    n_0 = 0
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]

        if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
        if prev[nx][ny] == 0:
            n_0 += 1

    temp = []
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]

        if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
        if prev_board[nx][ny] == 0:
            board[nx][ny] += board[x][y] // n_0
            temp.append((nx, ny))

    return temp

def cnt_kill(x, y):
    cnt = board[x][y]

    for i in range(4, 8):
        for _k in range(1, k+1):
            nx = x + (dx[i] * _k)
            ny = y + (dy[i] * _k)

            if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
            if board[nx][ny] == -1: break
            
            if int(board[nx][ny]) != board[nx][ny]: continue

            cnt += board[nx][ny]

    return cnt


def kill(x, y, board):
    kill_xy = []

    for i in range(4, 8):
        for _k in range(k+1):
            nx = x + (dx[i] * _k)
            ny = y + (dy[i] * _k)

            if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
            if board[nx][ny] != int(board[nx][ny]): continue
            if board[nx][ny] == -1: break

            board[nx][ny] = 0.1 * c
            kill_xy.append([nx, ny])

    return kill_xy

import copy
if __name__ == "__main__":
    n, m, k, c = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    ans = 0
    kill_xy = []

    for year in range(m):
        prev_board = copy.deepcopy(board)

        tree_loc = []
        for x in range(n):
            for y in range(n):
                if board[x][y] != -1 and int(board[x][y]) == board[x][y] and board[x][y] != 0: 
                    tree_loc.append((x, y))

        for x in range(n):
            for y in range(n):
                if board[x][y] == -1 or board[x][y] == 0 or int(board[x][y]) != board[x][y]: continue

                board[x][y] += grow(x, y)

        temp = []
        for x, y in tree_loc:
            temp += new_tree(x, y, board, prev_board)

        max_kill = -1e9
        max_xy = [0, 0]
        for x in range(n):
            for y in range(n):
                if board[x][y] == -1: continue
                if cnt_kill(x, y) > max_kill:
                    max_kill = cnt_kill(x, y)
                    max_xy = [x, y]

        for x, y in kill_xy:
            board[x][y] -= 0.1

        ans += cnt_kill(max_xy[0], max_xy[1])
        kill_xy += kill(max_xy[0], max_xy[1], board)
    
    print(int(ans))