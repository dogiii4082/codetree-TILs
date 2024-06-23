dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


from collections import deque


def BFS(r, c):
    visited = [[False for _ in range(Y)] for _ in range(X)]

    result = r
    q = deque([(r, c)])
    visited[r][c] = True
    while q:
        x, y = q.popleft()

        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]

            if nx < 0 or nx >= X or ny < 0 or ny >= Y: continue
            if board[nx][ny] == 0 or visited[nx][ny]: continue

            if board[nx][ny] == board[x][y] or is_exit[x][y]:
                q.append((nx, ny))
                visited[nx][ny] = True
                result = max(result, nx+1)

    return result


def reset():
    for x in range(X):
        for y in range(Y):
            board[x][y] = 0
            is_exit[x][y] = False


def move(i):
    global ans

    c = C[i]

    r = -2
    while r <= X-3:

        # 밑으로 내려갈 수 있음
        if board[r+2][c] == 0 and board[r+1][c-1] == 0 and board[r+1][c+1] == 0:
            r += 1

        # 서쪽 아래로
        elif (board[r+2][c] != 0 or board[r+1][c-1] != 0 or board[r+1][c+1] != 0) and c-2 >= 0 and r+2 <= X-1 and board[r-1][c-1] == 0 and board[r][c-2] == 0 and board[r+1][c-1] == 0 and board[r+1][c-2] == 0 and board[r+2][c-1] == 0:
            r += 1
            c -= 1
            D[i] = (D[i] + 3) % 4

        # 동쪽 아래로
        elif (board[r+2][c] != 0 or board[r+1][c-1] != 0 or board[r+1][c+1] != 0) and c+2 <= Y-1 and r+2 <= X-1 and board[r-1][c+1] == 0 and board[r][c+2] == 0 and board[r+1][c+1] == 0 and board[r+1][c+2] == 0 and board[r+2][c+1] == 0:
            r += 1
            c += 1
            D[i] = (D[i] + 1) % 4

        # 다 불가능
        else:
            if r-1 < 0:     # 골렘의 일부가 밖에
                reset()
                return
            break

    board[r][c] = i+1
    for j in range(4):
        board[r+dx[j]][c+dy[j]] = i+1
    is_exit[r+dx[D[i]]][c+dy[D[i]]] = True

    ans += BFS(r, c)


if __name__ == "__main__":
    X, Y, K = map(int, input().split())
    board = [[0 for _ in range(Y)]]
    for _ in range(X):
        board.append([0 for _ in range(Y)])
    C = []; D = []  # D: [북, 동, 남, 서]
    is_exit = [[False for _ in range(Y)] for _ in range(X)]
    ans = 0
    for _ in range(K):
        c, d = map(int, input().split())
        C.append(c-1)
        D.append(d)

    ans = 0
    for i in range(K):
        move(i)
    print(ans)