# import copy

# dx = [-1, 1, 0, 0]
# dy = [0, 0, -1, 1]

# def dist(x1, y1, x2, y2):
#     return abs(x1-x2) + abs(y1-y2)

# def move(person):
#     global ans

#     x, y = person

#     for i in range(4):
#         nx = x + dx[i]
#         ny = y + dy[i]

#         if nx < 1 or nx > N or ny < 1 or ny > N: continue
#         if board[nx][ny] != 0: continue

#         # print(ex, ey, nx, ny, '!!!!!!!!!')
#         if dist(ex, ey, nx, ny) < dist(ex, ey, x, y):
#             ans += 1
#             return nx, ny
        
#     return x, y

# def is_contain_both(x, y, d):
#     is_person = False
#     is_exit = False

#     for r in range(x, x+d):
#         for c in range(y, y+d):
#             for px, py in people:
#                 if px == ex and py == ey: continue
#                 if x <= px <= x+d-1 and y <= py <= y+d-1:
#                     is_person = True
#             if r == ex and c == ey:
#                 is_exit = True

#     return is_person and is_exit

# def rotate(x, y, d):
#     ret = copy.deepcopy(board)

#     for r in range(x, x+d):
#         for c in range(y, y+d):
#             ox, oy = r-x, c-y
#             rx, ry = oy, d-ox-1
#             ret[rx+x][ry+y] = board[r][c]

#     for r in range(x, x+d):
#         for c in range(y, y+d):
#             if ret[r][c]:
#                 ret[r][c] -= 1

#     return ret


# if __name__ == "__main__":
#     N, M, K = map(int, input().split())
#     board = [[0 for _ in range(N+1)]]
#     for _ in range(N):
#         temp = list(map(int, input().split()))
#         row = list([0] + temp)
#         board.append(row)
#     people = [list(map(int, input().split())) for _ in range(M)]
#     ex, ey = map(int, input().split())

#     ans = 0
#     for _ in range(K):
#         # print(_+1, "@@@@@@@@@@@")
#         # print(people)
#         for idx, person in enumerate(people):
#             if person[0] == ex and person[1] == ey: continue
#             nx, ny = move(person)
#             # if nx == ex and ny == ey:
#             #     people = people[:idx] + people[idx+1:]
#             # else:
#             people[idx] = [nx, ny]

#         is_all_escaped = True
#         for px, py in people:
#             if px != ex or py != ey:
#                 is_all_escaped = False

#         # 만약 모든 사람이 출구로 탈출했으면 바로 종료합니다.
#         if is_all_escaped: 
#             break

#         lx, ly, d = int(1e9), int(1e9), int(1e9)
#         for _d in range(2, N+1):
#             for x in range(1, N-_d+2):
#                 for y in range(1, N-_d+2):
#                     if is_contain_both(x, y, _d) and x < lx and y < ly and _d < d:
#                         lx, ly, d = x, y, _d
#         # print(lx, ly, d)
#         board = rotate(lx, ly, d)               # 판 회전
#         for idx, person in enumerate(people):   # 사람 회전
#             x, y = person

#             if lx <= x < lx+d and ly <= y < ly+d:
#                 ox, oy = x - lx, y - ly
#                 rx, ry = oy, d - ox - 1
#                 people[idx] = [rx + lx, ry + ly]

#         ox, oy = ex - lx, ey - ly
#         rx, ry = oy, d - ox - 1
#         ex, ey = rx + lx, ry + ly

#         # print(board)
#         # print(people)
#         # print("EXIT", ex, ey)
#         # print("rotate", lx, ly, d)
#     print(ans)
#     print(ex, ey)

MAX_N = 11
MAX_M = 11

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

grid = [[0 for _ in range(MAX_N)] for _ in range(MAX_N)]
PX = [0 for _ in range(MAX_M)]
PY = [0 for _ in range(MAX_M)]
is_end = [False for _ in range(MAX_M)]


def is_wall(x, y):
    return 1 <= grid[x][y] <= 9


def is_empty(x, y):
    return grid[x][y] == 0


def is_exit(x, y):
    return x == ex and y == ey


def distance(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)


def in_range(x, y):
    return 1 <= x <= N and 1 <= y <= N


def move():
    global ans

    for pid in range(1, M+1):

        if is_end[pid]: continue

        x, y = PX[pid], PY[pid]
        cur_dist = distance(x, y, ex, ey)
        tx, ty = x, y

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if not in_range(nx, ny): continue
            if is_wall(nx, ny): continue

            if distance(nx, ny, ex, ey) < cur_dist:
                tx, ty = nx, ny
                break

        if (x, y) != (tx, ty): ans += 1

        if (tx, ty) == (ex, ey): is_end[pid] = True

        PX[pid] = tx
        PY[pid] = ty


def is_p_and_exit(r, x, y):
    for pid in range(1, M+1):
        if is_end[pid]: continue
        if x <= PX[pid] <= x + r - 1 and y <= PY[pid] <= y + r - 1 and x <= ex <= x + r - 1 and y <= ey <= y + r - 1:
            return True
    return False


def rotate_people_exit(d, x, y):
    global ex, ey

    ox, oy = ex - x, ey - y
    rx, ry = oy, d - ox - 1
    ex = rx + x
    ey = ry + y

    for pid in range(1, M+1):
        if is_end[pid]: continue
        if x <= PX[pid] <= x + d - 1 and y <= PY[pid] <= y + d - 1:
            ox, oy = PX[pid] - x, PY[pid] - y
            rx, ry = oy, d - ox - 1
            PX[pid] = rx + x
            PY[pid] = ry + y


def rotate():
    ret = [grid[row][:] for row in range(MAX_N)]

    for d in range(1, N+1):
        for x in range(1, N+1):
            for y in range(1, N+1):
                if not is_p_and_exit(d, x, y): continue

                for r in range(x, x + d):
                    for c in range(y, y + d):
                        ox, oy = r - x, c - y
                        rx, ry = oy, d - ox - 1
                        ret[rx + x][ry + y] = grid[r][c]

                for r in range(x, x+d):
                    for c in range(y, y+d):
                        if ret[r][c] != 0: ret[r][c] -= 1

                rotate_people_exit(d, x, y)

                return ret

    return ret


if __name__ == "__main__":
    N, M, K = map(int, input().split())
    for x in range(1, N+1):
        row = list(map(int, input().split()))
        for y in range(1, N+1):
            grid[x][y] = row[y-1]
    for pid in range(1, M+1):
        x, y = map(int, input().split())
        PX[pid] = x
        PY[pid] = y
    ex, ey = map(int, input().split())

    ans = 0
    for k in range(1, K+1):
        move()
        if all(is_end[1:M+1]): break
        grid = rotate()
    print(ans)
    print(ex, ey)