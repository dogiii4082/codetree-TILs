dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]


def attack(m):
    global ans

    d, p = attacks[m]
    for i in range(1, p+1):
        nx = ax + dx[d] * i
        ny = ay + dy[d] * i

        if grid[nx][ny] == 0: continue

        ans += grid[nx][ny]
        grid[nx][ny] = 0


def move():
    global ans

    x, y, d = ax, ay, 2     # 3, 3

    coords = []
    nums = []
    while x != 0 or y != 0:
        nx = x + dx[d]     # 3
        ny = y + dy[d]     # 2
        coords.append((nx, ny))
        if grid[nx][ny] != 0: nums.append(grid[nx][ny])

        if nx <= ax and nx == ny + 1: d = 1
        elif nx > ax and nx + ny == ax + ay: d = 0
        elif nx > ax and nx == ny: d = 3
        elif nx < ax and nx + ny == ax + ay: d = 2

        x = nx
        y = ny
    while True:
        dp = [1] * len(nums)
        for i in range(1, len(nums)):
            if nums[i-1] == nums[i]:
                dp[i] = dp[i-1] + 1
            else:
                dp[i] = 1
        for i in range(len(dp)-1, 0, -1):
            if nums[i] == nums[i-1]:
                dp[i-1] = dp[i]
        s = set()
        for i in range(len(dp)):
            if dp[i] >= 4:
                s.add((nums[i], dp[i]))
        temp = list(s)
        for n, c in temp:
            ans += n * c
        res = []
        for i in range(len(nums)):
            if dp[i] < 4:
                res.append(nums[i])
        if len(nums) == len(res):
            break
        nums = res

    nums.append(0)
    num = nums[0]
    cnt = 1
    ret = []
    for i in range(1, len(nums)):
        if nums[i] == num:
            cnt += 1
        else:
            ret.append(cnt)
            ret.append(num)
            num = nums[i]
            cnt = 1
    tmp2 = [[0] * N for _ in range(N)]
    for i in range(len(ret)):
        try:
            tmp2[coords[i][0]][coords[i][1]] = ret[i]
        except:
            break
    return tmp2


if __name__ == "__main__":
    N, M = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(N)]
    attacks = [list(map(int, input().split())) for _ in range(M)]
    ax, ay = N // 2, N // 2

    ans = 0
    for m in range(M):
        # print(f'====={m}=====')
        attack(m)
        # for row in grid:
        #     print(*row)
        # print()
        grid = move()
        # for row in grid:
        #     print(*row)
        # print()
    print(ans)