# dx = [-1, 0, 1, 0]
# dy = [0, 1, 0, -1]


# oppo = {
#     0: 2,
#     1: 3,
#     2: 0,
#     3: 1
# }


# def battle(ids):
#     # print(ids)
#     global points

#     a, b = ids

#     if S[a] + guns[a] == S[b] + guns[b]:
#         winner, loser = (a, b) if S[a] > S[b] else (b, a)
#     else:
#         winner, loser = (a, b) if S[a] + guns[a] > S[b] + guns[b] else (b, a)

#     points[winner] += abs((S[a] + guns[a]) - (S[b] + guns[b]))

#     return winner, loser


# def move(x, y, d, s, i):
#     global n

#     nx = x + dx[d]
#     ny = y + dy[d]
#     if nx < 1 or nx > n:
#         d = oppo[d]
#         nx = x + dx[d]
#     elif ny < 1 or ny > n:
#         d = oppo[d]
#         ny = y + dy[d]

#     players[i] = [nx, ny, d, s]
#     X[i] = nx
#     Y[i] = ny
#     cnt_players = 0
#     for j in range(1, m+1):
#         x, y, _, _ = players[j]
#         if x == nx and y == ny: cnt_players += 1

#     if cnt_players == 1:    # 플레이어가 없다면
#         if any(board[nx][ny]):   # 총이 있으면
#             if guns[i]:     # 플레이어가 이미 총 가지고 있으면
#                 temp = board[nx][ny] + [guns[i]]
#                 M = max(temp)
#                 temp.pop(temp.index(M))
#                 board[nx][ny] = temp
#                 guns[i] = M
#             else:           # 플레이어가 총 없으면
#                 guns[i] = max(board[nx][ny])
#                 board[nx][ny].pop(board[nx][ny].index(guns[i]))

#     else:   # 플레이어 있으면 배틀
#         tmp = []
#         for i in range(1, m+1):
#             if players[i][0] == nx and players[i][1] == ny:
#                 tmp.append(i)

#         win, lose = battle(tmp)
#         board[nx][ny].append(guns[lose])
#         guns[lose] = 0
#         nnx = nx + dx[players[lose][2]]
#         nny = ny + dy[players[lose][2]]

#         cnt_players = 0
#         try:
#             for u in range(1, m + 1):
#                 x, y, _, _ = players[u]
#                 if x == nnx and y == nny: cnt_players += 1
#         except:
#             pass

#         if cnt_players > 0 or nnx < 1 or nnx > n or nny < 1 or nny > n:
#             for q in range(players[lose][2]+1, players[lose][2]+4): # 3, 4, 5
#                 nnx = nx + dx[q % 4]
#                 nny = ny + dy[q % 4]

#                 cnt_players = 0
#                 for w in range(1, m + 1):
#                     x, y, _, _ = players[w]
#                     if x == nnx and y == nny: cnt_players += 1

#                 if cnt_players > 0 or nnx < 1 or nnx > n or nny < 1 or nny > n: continue
#                 players[lose] = [nnx, nny, q % 4, players[lose][3]]
#                 if any(board[nnx][nny]):
#                     M = max(board[nnx][nny])
#                     guns[lose] = M
#                     board[nnx][nny].pop(board[nnx][nny].index(M))
#                 break
#         else:
#             players[lose] = [nnx, nny, players[lose][2], players[lose][3]]
#             if board[nnx][nny]:
#                 M = max(board[nnx][nny])
#                 guns[lose] = M
#                 board[nnx][nny].pop(board[nnx][nny].index(M))

#         tmp_win = board[nx][ny] + [guns[win]]
#         guns[win] = max(tmp_win)
#         tmp_win.pop(tmp_win.index(guns[win]))
#         board[nx][ny] = tmp_win



# if __name__ == "__main__":
#     n, m, k = map(int, input().split())     # n: 격자의 크기, m: 플레이어의 수, k: 라운드의 수
#     board = [[[] for _ in range(n+1)] for _ in range(n+1)]
#     for i in range(1, n+1):
#         temp = list(map(int, input().split()))
#         for idx, j in enumerate(temp):
#             board[i][idx+1].append(j)

#     players = [[]]
#     X = [0]
#     Y = [0]
#     D = [0]
#     S = [0]
#     for _ in range(m):
#         x, y, d, s = map(int, input().split())  # d: 방향, s: 초기 능력치
#         players.append([x, y, d, s])
#         X.append(x)
#         Y.append(y)
#         D.append(d)
#         S.append(s)

#     guns = [0 for _ in range(m+1)]
#     points = [0 for _ in range(m+1)]
#     for _ in range(k):
#         # print(_+1, '@@@@@@')
#         for i in range(1, m+1):
#             x, y, d, s = players[i]

#             move(x, y, d, s, i)
#         # print(board)
#         # print('guns', guns)
#         # print('players', players)
#     print(*points[1:])



dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


def in_range(x, y):
    return 1 <= x <= n and 1 <= y <= n


def is_player(x, y, pid):
    for i in range(1, m+1):
        if i == pid: continue
        if (X[i], Y[i]) == (x, y): return True
    return False


def other_player(x, y, pid):
    for i in range(1, m+1):
        if i == pid: continue
        if (X[i], Y[i]) == (x, y): return i


def is_gun(x, y):
    return grid[x][y] != 0


def player_has_gun(pid):
    return G[pid] != 0


def get_max_gun(x, y, pid):
    tmp = grid[x][y] + [G[pid]]
    M_idx = None
    for idx, g in enumerate(tmp):
        if g == max(tmp):
            M_idx = idx
            break
    G[pid] = tmp[M_idx]
    tmp.pop(M_idx)
    grid[x][y] = tmp[:]


def move_lose(x, y, lose):
    if player_has_gun(lose):
        grid[x][y].extend([G[lose]])
        G[lose] = 0

    def can_go(x, y, pid):
        return in_range(x, y) and not is_player(x, y, pid)

    while True:
        nx = x + dx[D[lose]]
        ny = y + dy[D[lose]]
        if can_go(nx, ny, lose):
            X[lose] = nx
            Y[lose] = ny
            get_max_gun(nx, ny, lose)
            return
        D[lose] = (D[lose] + 1) % 4


def move(pid):
    x = X[pid]
    y = Y[pid]
    d = D[pid]

    nx = x + dx[d]
    ny = y + dy[d]
    if not in_range(nx, ny):
        d = (d + 2) % 4
        nx = x + dx[d]
        ny = y + dy[d]

    if not is_player(nx, ny, pid):
        X[pid] = nx
        Y[pid] = ny
        D[pid] = d

        if is_gun(nx, ny):

            if player_has_gun(pid):
                get_max_gun(nx, ny, pid)

            else:
                get_max_gun(nx, ny, pid)

    else:
        other = other_player(nx, ny, pid)
        if S[pid] + G[pid] == S[other] + G[other]:
            if S[pid] > S[other]:
                win = pid
                lose = other
            else:
                win = other
                lose = pid
        else:
            if S[pid] + G[pid] > S[other] + G[other]:
                win = pid
                lose = other
            else:
                win = other
                lose = pid

        ans[win] += (S[win] + G[win]) - (S[lose] + G[lose])

        X[pid] = nx
        Y[pid] = ny
        move_lose(nx, ny, lose)
        get_max_gun(nx, ny, win)


if __name__ == "__main__":
    n, m, k = map(int, input().split())
    grid = [[[0] for _ in range(n+1)]]
    for _ in range(n):
        row = [[0]]
        tmp = list(map(int, input().split()))
        for c in tmp:
            row.append([c])
        grid.append(row)

    X = [0]; Y = [0]; D = [0]; S = [0]; G = [0]
    for _ in range(m):
        x, y, d, s = map(int, input().split())
        X.append(x)
        Y.append(y)
        D.append(d)
        S.append(s)
        G.append(0)

    ans = [0 for _ in range(m+1)]
    for _ in range(k):
        for pid in range(1, m+1):
            move(pid)
            
    print(*ans[1:])