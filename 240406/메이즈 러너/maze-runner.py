import copy

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def dist(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

def move(person):
    global ans

    x, y = person

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]

        if nx < 1 or nx > N or ny < 1 or ny > N: continue
        if board[nx][ny] != 0: continue

        # print(ex, ey, nx, ny, '!!!!!!!!!')
        if dist(ex, ey, nx, ny) < dist(ex, ey, x, y):
            ans += 1
            return nx, ny
        
    return x, y

def is_contain_both(x, y, d):
    is_person = False
    is_exit = False

    for r in range(x, x+d):
        for c in range(y, y+d):
            for px, py in people:
                if px == ex and py == ey: continue
                if x <= px <= x+d-1 and y <= py <= y+d-1:
                    is_person = True
            if r == ex and c == ey:
                is_exit = True

    return is_person and is_exit

def rotate(x, y, d):
    ret = copy.deepcopy(board)

    for r in range(x, x+d):
        for c in range(y, y+d):
            ox, oy = r-x, c-y
            rx, ry = oy, d-ox-1
            ret[rx+x][ry+y] = board[r][c]

    for r in range(x, x+d):
        for c in range(y, y+d):
            if ret[r][c]:
                ret[r][c] -= 1

    return ret


if __name__ == "__main__":
    N, M, K = map(int, input().split())
    board = [[0 for _ in range(N+1)]]
    for _ in range(N):
        temp = list(map(int, input().split()))
        row = list([0] + temp)
        board.append(row)
    people = [list(map(int, input().split())) for _ in range(M)]
    ex, ey = map(int, input().split())

    ans = 0
    for _ in range(K):
        # print(_+1, "@@@@@@@@@@@")
        # print(people)
        for idx, person in enumerate(people):
            if person[0] == ex and person[1] == ey: continue
            nx, ny = move(person)
            # if nx == ex and ny == ey:
            #     people = people[:idx] + people[idx+1:]
            # else:
            people[idx] = [nx, ny]

        is_all_escaped = True
        for px, py in people:
            if px != ex or py != ey:
                is_all_escaped = False

        # 만약 모든 사람이 출구로 탈출했으면 바로 종료합니다.
        if is_all_escaped: 
            break

        lx, ly, d = int(1e9), int(1e9), int(1e9)
        for _d in range(2, N+1):
            for x in range(1, N-_d+2):
                for y in range(1, N-_d+2):
                    if is_contain_both(x, y, _d) and x < lx and y < ly and _d < d:
                        lx, ly, d = x, y, _d
        # print(lx, ly, d)
        board = rotate(lx, ly, d)               # 판 회전
        for idx, person in enumerate(people):   # 사람 회전
            x, y = person

            if lx <= x < lx+d and ly <= y < ly+d:
                ox, oy = x - lx, y - ly
                rx, ry = oy, d - ox - 1
                people[idx] = [rx + lx, ry + ly]

        ox, oy = ex - lx, ey - ly
        rx, ry = oy, d - ox - 1
        ex, ey = rx + lx, ry + ly

        # print(board)
        # print(people)
        # print("EXIT", ex, ey)
        # print("rotate", lx, ly, d)
    print(ans)
    print(ex, ey)