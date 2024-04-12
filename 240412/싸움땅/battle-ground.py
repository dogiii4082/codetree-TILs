dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


oppo = {
    0: 2,
    1: 3,
    2: 0,
    3: 1
}


def battle(ids):
    global points

    a, b = ids
    # winner = 0
    # loser = 0

    if S[a] + guns[a] == S[b] + guns[b]:
        winner, loser = (a, b) if S[a] > S[b] else (b, a)
    else:
        winner, loser = (a, b) if S[a] + guns[a] > S[b] + guns[b] else (b, a)

    points[winner] += abs((S[a] + guns[a]) - (S[b] + guns[b]))
    return winner, loser


def move(x, y, d, s, i):
    global n

    nx = x + dx[d]
    ny = y + dy[d]
    if nx < 1 or nx > n:
        d = oppo[d]
        nx = x + dx[d]
    elif ny < 1 or ny > n:
        d = oppo[d]
        ny = y + dy[d]

    players[i] = [nx, ny, d, s]
    X[i] = nx
    Y[i] = ny
    cnt_players = 0
    for j in range(1, m+1):
        x, y, _, _ = players[j]
        if x == nx and y == ny: cnt_players += 1

    if cnt_players == 1:    # 플레이어가 없다면
        if board[nx][ny] != [0] and board[nx][ny]:   # 총이 있으면
            if guns[i]:     # 플레이어가 이미 총 가지고 있으면
                temp = board[nx][ny] + [guns[i]]
                M = max(temp)
                temp.pop(temp.index(M))
                board[nx][ny] = temp
                guns[i] = M
            else:           # 플레이어가 총 없으면
                guns[i] = max(board[nx][ny])
                board[nx][ny].pop(board[nx][ny].index(guns[i]))
        # print(board)
        # print(guns)
        # print(players)

    else:   # 플레이어 있으면 배틀
        tmp = []
        for i in range(1, m+1):
            if players[i][0] == nx and players[i][1] == ny:
                tmp.append(i)

        win, lose = battle(tmp)
        board[nx][ny].append(guns[lose])
        guns[lose] = 0
        nnx = nx + dx[players[lose][2]]
        nny = ny + dy[players[lose][2]]

        try:
            cnt_players = 0
            for u in range(1, m + 1):
                x, y, _, _ = players[u]
                if x == nnx and y == nny: cnt_players += 1
        except:
            pass

        if cnt_players > 0 or nnx < 1 or nnx > n or nny < 1 or nny > n:
            for q in range(players[lose][2]+1, players[lose][2]+4): # 3, 4, 5
                nnx = nx + dx[q % 4]
                nny = ny + dy[q % 4]

                cnt_players = 0
                for w in range(1, m + 1):
                    x, y, _, _ = players[w]
                    if x == nnx and y == nny: cnt_players += 1

                if cnt_players > 1 or nnx < 1 or nnx > n or nny < 1 or nny > n: continue
                players[lose] = [nnx, nny, q % 4, players[lose][3]]
                if board[nnx][nnx] != [0] and board[nnx][nnx] != []:
                    M = max(board[nnx][nny])
                    guns[lose] = M
                    board[nnx][nny].pop(board[nnx][nny].index(M))
                break
        else:
            players[lose] = [nnx, nny, d, players[lose][3]]
            if board[nnx][nny]:
                M = max(board[nnx][nny])
                guns[lose] = M
                board[nnx][nny].pop(board[nnx][nny].index(M))

        tmp_win = board[nx][ny] + [guns[win]]
        guns[win] = max(tmp_win)
        tmp_win.pop(tmp_win.index(guns[win]))
        board[nx][ny] = tmp_win



if __name__ == "__main__":
    n, m, k = map(int, input().split())     # n: 격자의 크기, m: 플레이어의 수, k: 라운드의 수
    board = [[[] for _ in range(n+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        temp = list(map(int, input().split()))
        for idx, j in enumerate(temp):
            board[i][idx+1].append(j)

    players = [[]]
    X = [0]
    Y = [0]
    D = [0]
    S = [0]
    for _ in range(m):
        x, y, d, s = map(int, input().split())  # d: 방향, s: 초기 능력치
        players.append([x, y, d, s])
        X.append(x)
        Y.append(y)
        D.append(d)
        S.append(s)

    guns = [0 for _ in range(m+1)]
    points = [0 for _ in range(m+1)]
    for _ in range(k):
        for i in range(1, m+1):
            x, y, d, s = players[i]

            move(x, y, d, s, i)
    print(*points[1:])