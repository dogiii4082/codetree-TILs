import sys
input = sys.stdin.readline

N, M = map(int, input().split())

board = list()
for _ in range(N):
    board.append(list(map(int, input().split())))
    
dx = [0, 0, -1, -1, -1, 0, 1, 1, 1]
dy = [0, 1, 1, 0, -1, -1, -1, 0, 1]
special_nutrition = [[N - 1, 0], [N - 2, 0], [N - 1, 1],  [N - 2, 1]]

def move_in_wrapping_grid(coord):
    if coord < 0:
        return coord + N
    if coord >= N:
        return coord % N
    return coord

def is_valid_coord(x, y):
    return 0 <= x < N and 0 <= y < N

def move_special_nutrient(dir, p):
    new_nutritions = []
    for i in range(len(special_nutrition)):
        special_nutrition[i][0] = move_in_wrapping_grid(special_nutrition[i][0] + dx[dir] * p)
        special_nutrition[i][1] = move_in_wrapping_grid(special_nutrition[i][1] + dy[dir] * p)

def apply_special_nutrient():
    for coord in special_nutrition:
        board[coord[0]][coord[1]] += 1
        
def grow_adjacent_rebros():
    indexes_count = []
    for i in range(len(special_nutrition)):
        add_cnt = 0
        for d in [2, 4, 6, 8]:
            if is_valid_coord(special_nutrition[i][0] + dx[d], special_nutrition[i][1] + dy[d]) and board[special_nutrition[i][0] + dx[d]][special_nutrition[i][1] + dy[d]] > 0:
                add_cnt += 1
        indexes_count.append([i, add_cnt])
    for ch in indexes_count:
        i = ch[0]
        add_cnt = ch[1]
        board[special_nutrition[i][0]][special_nutrition[i][1]] += add_cnt
        
def buy_special_nutrient_and_trim_rebros():
    new_nutritions = []
    for i in range(N):
        for j in range(N):
            if board[i][j] >= 2 and ([i, j] not in  special_nutrition):
                board[i][j] -= 2
                new_nutritions.append([i, j])
    return new_nutritions

def calculate_total_rebros():
    res = 0
    for i in range(N):
        for j in range(N):
            res += board[i][j]
    return res

if __name__ == "__main__":
    for _ in range(M):
        d, p = map(int, input().split())
        move_special_nutrient(d, p)
        apply_special_nutrient()
        grow_adjacent_rebros()
        special_nutrition = buy_special_nutrient_and_trim_rebros()
    print(calculate_total_rebros())