from collections import deque

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def get_team(x, y, arr):     # 0, 2
    if board[x][y] == 3:
        return arr

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]

        if nx < 0 or nx >= n or ny < 0 or ny >= n: continue

        if board[nx][ny] == 2 or board[nx][ny] == 3:
            if [nx, ny] not in arr:
                arr.append([nx, ny])
                arr = get_team(nx, ny, arr)

    return arr


def move(t):
    team = deque(teams[t])     # [ [0, 2], [0, 1], [0, 0] ]
    x, y = team.pop()
    board[x][y] = 4
    hx, hy = team[0][0], team[0][1]

    for i in range(4):
        nx = hx + dx[i]
        ny = hy + dy[i]

        if nx < 0 or nx >= n or ny < 0 or ny >= n: continue

        if board[nx][ny] == 4:
            team.appendleft([nx, ny])
            break

    return team


def ball(r):
    r %= 4*n

    x, y = -1, -1

    if r // n == 0:
        for i in range(n):
            if board[r][i] in [1, 2, 3]:
                x, y = r, i
                break

    elif r // n == 1:
        for i in range(n-1, -1, -1):
            if board[i][r%n] in [1, 2, 3]:
                x, y = i, r%n
                break

    elif r // n == 2:
        for i in range(n-1, -1, -1):
            if board[3*n-r-1][i] in [1, 2, 3]:
                x, y = 3*n-r-1, i
                break

    else:
        for i in range(n):
            if board[i][4*n-r-1] in [1, 2, 3]:
                x, y = i, 4*n-r-1
                break

    return [x, y]


if __name__ == "__main__":
    n, m, k = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]

    head = []
    for x in range(n):
        for y in range(n):
            if board[x][y] == 1: head.append([x, y])

    teams = []
    for i in range(len(head)):
        tmp = get_team(head[i][0], head[i][1], [head[i]])
        teams.append(tmp)


    ans = 0
    for r in range(k):
        for t in range(len(teams)):
            teams[t] = move(t)

        for x in range(n):
            for y in range(n):
                if board[x][y] != 0: board[x][y] = 4

        for t in range(len(teams)):
            for idx, (x, y) in enumerate(teams[t]):
                if idx == 0:
                    board[x][y] = 1
                elif idx == len(teams[t]) - 1:
                    board[x][y] = 3
                else:
                    board[x][y] = 2

        x, y = ball(r)
        if x != -1 and y != -1:
            for idx, team in enumerate(teams):
                if [x, y] in team:
                    ans += (team.index([x, y]) + 1) ** 2
                    teams[idx] = list(team)[::-1]

    print(ans)