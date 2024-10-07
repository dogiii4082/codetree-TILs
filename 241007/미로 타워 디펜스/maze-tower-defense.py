dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]


def attack(m):
    global ans

    d, p = attacks[m]
    for i in range(1, p + 1):
        nx = ax + dx[d] * i
        ny = ay + dy[d] * i

        if not (0 <= nx < N and 0 <= ny < N):
            continue

        if grid[nx][ny] == 0:
            continue

        ans += grid[nx][ny]
        grid[nx][ny] = 0


def move():
    global ans

    x, y, d = ax, ay, 2

    coords = []
    nums = []
    while x != 0 or y != 0:
        nx = x + dx[d]
        ny = y + dy[d]
        if grid[nx][ny] != 0:
            nums.append(grid[nx][ny])
        coords.append((nx, ny))

        if nx <= ax and nx == ny + 1:
            d = 1
        elif nx > ax and nx + ny == ax + ay:
            d = 0
        elif nx > ax and nx == ny:
            d = 3
        elif nx < ax and nx + ny == ax + ay:
            d = 2

        x, y = nx, ny

    # 폭발 처리 로직
    while True:
        dp = [1] * len(nums)
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                dp[i] = dp[i - 1] + 1
        exploded = False
        for i in range(len(dp) - 1, -1, -1):
            if dp[i] >= 4:
                ans += nums[i] * dp[i]
                exploded = True
                for j in range(dp[i]):
                    nums[i - j] = 0  # 폭발한 그룹을 0으로 설정
        if not exploded:
            break
        nums = [num for num in nums if num != 0]  # 남은 숫자만 모아줌

    # 숫자 그룹 재정렬 및 grid 반영
    nums.append(0)
    num, cnt = nums[0], 1
    ret = []
    for i in range(1, len(nums)):
        if nums[i] == num:
            cnt += 1
        else:
            ret.extend([cnt, num])
            num, cnt = nums[i], 1
    new_grid = [[0] * N for _ in range(N)]
    for i in range(len(ret)):
        if i >= len(coords):
            break
        x, y = coords[i]
        new_grid[x][y] = ret[i]
    return new_grid


if __name__ == "__main__":
    N, M = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(N)]
    attacks = [list(map(int, input().split())) for _ in range(M)]
    ax, ay = N // 2, N // 2

    ans = 0
    for m in range(M):
        attack(m)
        grid = move()
    print(ans)