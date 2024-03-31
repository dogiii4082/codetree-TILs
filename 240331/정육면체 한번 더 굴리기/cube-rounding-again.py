from collections import deque

dx = [0, 0, -1, 1]
dy = [1, -1, 0, 0]

def score(x, y, visited):
    q = deque([(x, y)])
    visited[x][y] = True
    
    cnt = board[x][y]
    while q:
        x, y = q.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
            if board[nx][ny] != board[x][y] or visited[nx][ny]: continue

            q.append((nx, ny))
            visited[nx][ny] = True
            cnt += board[nx][ny]

    return cnt

def roll(direction):
    global dice
    global dice_loc

    if direction == 1:      # [4, 2, 1, 6, 5, 3]
        if dice_loc[1] + 1 >= n:
            dice[0], dice[2], dice[3], dice[5] = dice[2], dice[5], dice[0], dice[3]
            dice_loc = [dice_loc[0], dice_loc[1]-1]
        else:
            dice[0], dice[2], dice[3], dice[5] = dice[3], dice[0], dice[5], dice[2]
            dice_loc = [dice_loc[0], dice_loc[1]+1]

    elif direction == 2:    # [5, 1, 3, 4, 6, 2]
        if dice_loc[0] + 1 >= n:
            dice[0], dice[1], dice[4], dice[5] = dice[1], dice[5], dice[0], dice[4]
            dice_loc = [dice_loc[0]-1, dice_loc[1]]
        else:
            dice[0], dice[1], dice[4], dice[5] = dice[4], dice[0], dice[5], dice[1]
            dice_loc = [dice_loc[0]+1, dice_loc[1]]

    elif direction == 3:    # [3, 2, 6, 1, 5, 4]
        if dice_loc[1] - 1 >= n:
            dice[0], dice[2], dice[3], dice[5] = dice[3], dice[0], dice[5], dice[2]
            dice_loc = [dice_loc[0], dice_loc[1]+1]
        else:
            dice[0], dice[2], dice[3], dice[5] = dice[2], dice[5], dice[0], dice[3]
            dice_loc = [dice_loc[0], dice_loc[1]-1]

    elif direction == 4:    # [2, 6, 3, 4, 1, 5]
        if dice_loc[0] - 1 >= n:
            dice[0], dice[1], dice[4], dice[5] = dice[4], dice[0], dice[5], dice[1]
            dice_loc = [dice_loc[0]+1, dice_loc[1]]
        else:
            dice[0], dice[1], dice[4], dice[5] = dice[1], dice[5], dice[0], dice[4]
            dice_loc = [dice_loc[0]-1, dice_loc[1]]



if __name__ == '__main__':
    n, m = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    visited = [[False for _ in range(n)] for _ in range(n)]
    dice_loc = [0, 0]
    ans = 0
    direction = 1

    dice = [1, 2, 3, 4, 5, 6]   # 아래: dice[-1]
    roll(1)
    ans += score(dice_loc[0], dice_loc[1], visited)
    visited = [[False for _ in range(n)] for _ in range(n)]
    for _ in range(m-1):
        if dice[-1] > board[dice_loc[0]][dice_loc[1]]:      # 시계 방향
            if direction == 4:
                roll(1)
                ans += score(dice_loc[0], dice_loc[1], visited)
                visited = [[False for _ in range(n)] for _ in range(n)]
                direction = 1

            else:
                roll(direction+1)
                ans += score(dice_loc[0], dice_loc[1], visited)
                visited = [[False for _ in range(n)] for _ in range(n)]
                direction += 1

        elif dice[-1] < board[dice_loc[0]][dice_loc[1]]:    # 반시계 방향
            if direction == 1:
                roll(4)
                ans += score(dice_loc[0], dice_loc[1], visited)
                visited = [[False for _ in range(n)] for _ in range(n)]
                direction = 4
                
            else:
                roll(direction-1)
                ans += score(dice_loc[0], dice_loc[1], visited)
                visited = [[False for _ in range(n)] for _ in range(n)]
                direction -= 1
        
        else:   # 그대로
            roll(direction)
            ans += score(dice_loc[0], dice_loc[1], visited)
            visited = [[False for _ in range(n)] for _ in range(n)]
            
    print(ans)