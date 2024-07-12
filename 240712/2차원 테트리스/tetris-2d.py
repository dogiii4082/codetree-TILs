import copy


def move_yellow(t, x, y):
    if t == 1:
        for i in range(6):
            if yellow[i][y]:
                yellow[i-1][y] = 1
                return
            elif i == 5:
                yellow[5][y] = 1
                return

    elif t == 2:
        for i in range(6):
            if yellow[i][y] or yellow[i][y+1]:
                yellow[i-1][y] = 1
                yellow[i-1][y+1] = 1
                return
            elif i == 5:
                yellow[5][y] = 1
                yellow[5][y+1] = 1
                return

    elif t == 3:
        for i in range(5):
            if i == 4:
                yellow[5][y] = 1
                yellow[4][y] = 1
                return
            elif yellow[i+2][y]:
                yellow[i][y] = 1
                yellow[i+1][y] = 1
                return


def move_red(t, x, y):
    if t == 1:
        for i in range(6):
            if red[i][3-x]:
                red[i-1][3-x] = 1
                return
            elif i == 5:
                red[5][3-x] = 1
                return

    elif t == 2:
        for i in range(5):
            if i == 4:
                red[5][3-x] = 1
                red[4][3-x] = 1
                return
            elif red[i+2][3-x]:
                red[i][3-x] = 1
                red[i+1][3-x] = 1
                return

    elif t == 3:
        for i in range(6):
            if red[i][3-x] or red[i][3-x-1]:
                red[i-1][3-x] = 1
                red[i-1][3-x-1] = 1
                return
            elif i == 5:
                red[5][3-x] = 1
                red[5][3-x-1] = 1
                return


def is_full_yellow(r):
    for i in range(4):
        if not yellow[r][i]: return False
    global ans
    ans += 1
    return True


def is_full_red(c):
    for i in range(4):
        if not red[c][i]: return False
    global ans
    ans += 1
    return True


def delete_yellow():
    for i in range(6):
        tmp = copy.deepcopy(yellow)
        while is_full_yellow(i):
            for j in range(1, i+1):
                yellow[j] = tmp[j-1]


def delete_red():
    for i in range(6):
        tmp = copy.deepcopy(red)
        while is_full_red(i):
            for j in range(1, i + 1):
                red[j] = tmp[j - 1]


def delete_smoke_red(cnt):
    tmp = copy.deepcopy(red)
    for i in range(2, 6):
        red[i] = tmp[i-cnt]


def delete_smoke_yellow(cnt):
    tmp = copy.deepcopy(yellow)
    for i in range(2, 6):
        yellow[i] = tmp[i-cnt]


if __name__ == "__main__":
    blue = [[0 for _ in range(4)] for _ in range(4)]
    yellow = [[0 for _ in range(4)] for _ in range(6)]
    red = [[0 for _ in range(4)] for _ in range(6)]

    k = int(input())
    ans = 0
    for _ in range(k):
        t, x, y = map(int, input().split())

        move_yellow(t, x, y)
        move_red(t, x, y)

        delete_yellow()
        delete_red()

        y_cnt = 0
        for i in range(2):
            if any(yellow[i]): y_cnt += 1
        delete_smoke_yellow(y_cnt)
        for i in range(2):
            yellow[i] = [0, 0, 0, 0]

        r_cnt = 0
        for i in range(2):
            if any(red[i]): r_cnt += 1
        delete_smoke_red(r_cnt)
        for i in range(2):
            red[i] = [0, 0, 0, 0]



    y_cnt, r_cnt = 0, 0
    for i in range(2, 6):
        y_cnt += yellow[i].count(1)
        r_cnt += red[i].count(1)

    print(ans)
    print(y_cnt + r_cnt)