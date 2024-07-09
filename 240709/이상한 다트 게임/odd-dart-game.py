import copy

rotate_dict = {
    0: -1,
    1: 1
}

dr = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]

def rotate(x, d, k, board):
    board = copy.deepcopy(board)

    for r in range(1, n + 1):
        if r % x != 0: continue

        row = board[r]
        tmp = []
        for i in range(m):
            tmp.append(row[(rotate_dict[d] * k + i) % m])
        board[r] = tmp

    return board


def delete(board):
    tmp = copy.deepcopy(board)

    is_del = 0
    for r in range(1, n+1):
        for j in range(m):
            curr = board[r][j]

            if curr == -1: continue

            cnt = 0
            for i in range(4):
                nr = r + dr[i]
                nj = (j + dj[i]) % m

                if not 1 <= nr <= n: continue

                if board[nr][nj] == curr:
                    cnt += 1
                    tmp[nr][nj] = -1
                    is_del += 1

            if cnt > 0:
                tmp[r][j] = -1

    return tmp, is_del


def normalization():
    global board

    tot, cnt = 0, 0
    for r in range(1, n+1):
        for j in range(m):
            if board[r][j] == -1: continue

            tot += board[r][j]
            cnt += 1

    avg = tot // cnt
    for r in range(1, n+1):
        for j in range(m):
            if board[r][j] == -1: continue
            
            if board[r][j] > avg:
                board[r][j] -= 1
            elif board[r][j] < avg:
                board[r][j] += 1


def get_is_any():
    for r in range(1, n+1):
        for j in range(m):
            if board[r][j] != -1: return True

    return False

if __name__ == "__main__":
    n, m, q = map(int, input().split())
    board = [[0 for _ in range(m)]] + [list(map(int, input().split())) for _ in range(n)]
    rotate_info = []
    for _ in range(q):
        x, d, k = map(int, input().split())
        rotate_info.append((x, d, k))

    for x, d, k in rotate_info:
        board = rotate(x, d, k, board)

        board, is_deleted = delete(board)

        is_any = get_is_any()

        if not is_deleted and is_any:
            normalization()

    ans = 0
    for r in range(1, n+1):
        for j in range(m):
            if board[r][j] == -1: continue
            ans += board[r][j]
    print(ans)