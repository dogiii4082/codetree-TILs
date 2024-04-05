from collections import deque
import copy
import itertools

dx = [1, -1, 0, 0]
dy = [0, 0, -1, 1]

def BFS(x, y, visited):
    q = deque([(x, y)])
    visited[x][y] = True

    while q:
        x, y = q.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
            if visited[nx][ny] or board[x][y] != board[nx][ny]: continue

            q.append((nx, ny))
            visited[nx][ny] = True


# def get_group_N():
#     cnt = 0
#     visited = [[False for _ in range(n)] for _ in range(n)]

#     for x in range(n):
#         for y in range(n):
#             if not visited[x][y]:
#                 BFS(x, y, visited)
#                 cnt += 1

#     return cnt

def give_id(x, y, id, id_board, area):
    q = deque([(x, y)])
    visited[x][y] = True
    id_board[x][y] = id
    area[id] += 1

    while q:
        x, y = q.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
            if visited[nx][ny] or board[x][y] != board[nx][ny]: continue

            q.append((nx, ny))
            visited[nx][ny] = True
            id_board[nx][ny] = id
            area[id] += 1


def rotate_1():
    ret = copy.deepcopy(board)

    for c in range(n):
        ret[n//2][c] = board[c][n//2]
    
    for r in range(n):
        ret[r][n//2] = board[n//2][n-1-r]

    return ret


def rotate_2():
    ret = copy.deepcopy(board)

    for i in range(n//2):
        for j in range(n//2):
            ox, oy = i - 0, j - 0

            rx, ry = oy, n // 2 - ox - 1

            ret[rx + 0][ry + 0] = board[i][j]

    for i in range(0, 0+n // 2):
        for j in range(n//2+1, n//2+1+n // 2):
            ox, oy = i - 0, j - (n//2+1)

            rx, ry = oy, n // 2 - ox - 1

            ret[rx + 0][ry + (n//2+1)] = board[i][j]

    for i in range(n//2+1, (n//2+1)+n // 2):
        for j in range(0, 0+n // 2):
            ox, oy = i - (n//2+1), j - 0

            rx, ry = oy, (n // 2) - ox - 1

            ret[rx + (n//2+1)][ry + 0] = board[i][j]

    for i in range((n//2+1), (n//2+1)+(n // 2)):
        for j in range((n//2+1), (n//2+1)+(n // 2)):
            ox, oy = i - (n//2+1), j - (n//2+1)

            rx, ry = oy, (n // 2) - ox - 1

            ret[rx + (n//2+1)][ry + (n//2+1)] = board[i][j]

    return ret


if __name__ == '__main__':
    n = int(input())
    board = [list(map(int, input().split())) for _ in range(n)]
    ans = 0

    for _ in range(4):
        id = 0
        N = 0
        visited = [[False for _ in range(n)] for _ in range(n)]
        id_board = [[0 for _ in range(n)] for _ in range(n)]
        area = [0 for _ in range(n*n+1)]
        board_num = [0 for _ in range(n*n+1)]
        for x in range(n):
            for y in range(n):
                if not visited[x][y]:
                    id += 1
                    N += 1
                    board_num[id] = board[x][y]
                    give_id(x, y, id, id_board, area)

        for a, b in itertools.combinations([i for i in range(1, N+1)], 2):
            k = 0   # 맞닿아 있는 변의 수
            for x in range(n):
                for y in range(n):
                    if id_board[x][y] == a:
                        for i in range(4):
                            nx = x + dx[i]
                            ny = y + dy[i]

                            if nx < 0 or nx >= n or ny < 0 or ny >= n: continue

                            if id_board[nx][ny] == b:
                                k += 1
            ans  += (area[a] + area[b]) * board_num[a] * board_num[b] * k

        board = rotate_1()
        board = rotate_2()

    print(ans)