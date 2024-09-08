#include <iostream>
#include <vector>
#include <queue>
#include <cstring>

#define NORTH 0
#define EAST 1
#define SOUTH 2
#define WEST 3
#define MAX 75
#define MAX_K 1000
#define X first
#define Y second

using namespace std;

int R, C, K;
int grid[MAX][MAX];
int dr[4] = { -1, 0, 1, 0 };
int dc[4] = { 0, 1, 0, -1 };
int bot;
int dir[MAX_K];
bool isExit[MAX][MAX];

bool InRange(int r, int c) {
	return 1 <= r && r <= bot && 1 <= c && c <= C;
}

bool CanGoDown(int r, int c) {
	if (r >= bot - 1) return false;
	if (grid[r + 1][c - 1] != 0) return false;
	if (grid[r + 1][c] != 0) return false;
	if (grid[r + 1][c + 1] != 0) return false;
	if (grid[r + 2][c] != 0) return false;
	return true;
}

bool CanGoLeft(int r, int c) {
	if (!InRange(r, c - 2)) return false;
	if (!InRange(r + 2, c - 1)) return false;
	if (grid[r - 1][c - 1] != 0) return false;
	if (grid[r][c - 2] != 0) return false;
	if (grid[r + 1][c - 1] != 0) return false;
	if (grid[r + 1][c - 2] != 0) return false;
	if (grid[r + 2][c - 1] != 0) return false;
	return true;
}

bool CanGoRight(int r, int c) {
	if (!InRange(r, c + 2)) return false;
	if (!InRange(r + 2, c + 1)) return false;
	if (grid[r - 1][c + 1] != 0) return false;
	if (grid[r][c + 2] != 0) return false;
	if (grid[r + 1][c + 1] != 0) return false;
	if (grid[r + 1][c + 2] != 0) return false;
	if (grid[r + 2][c + 1] != 0) return false;
	return true;
}

bool TouchBot(int r) {
	return r + 1 == bot;
}

void GollemIsHere(int r, int c, int i) {
	grid[r][c] = i;
	grid[r - 1][c] = i;
	grid[r + 1][c] = i;
	grid[r][c - 1] = i;
	grid[r][c + 1] = i;
}

int bfs(int r, int c, int n) {
	queue<pair<int, int>> q;
	bool visited[MAX][MAX]; memset(visited, false, sizeof visited);
	vector<int> rows;

	q.push(make_pair(r, c));
	visited[r][c] = true;
	rows.push_back(r);
	while (!q.empty()) {
		auto cur = q.front(); q.pop();

		if (isExit[cur.X][cur.Y]) {
			for (int i = 0; i < 4; i++) {
				int nr = cur.X + dr[i];
				int nc = cur.Y + dc[i];

				if (!InRange(nr, nc)) continue;
				if (grid[nr][nc] == 0) continue;
				if (visited[nr][nc]) continue;

				q.push(make_pair(nr, nc));
				visited[nr][nc] = true;
				rows.push_back(nr);
			}
		}
		else {
			for (int i = 0; i < 4; i++) {
				int nr = cur.X + dr[i];
				int nc = cur.Y + dc[i];

				if (!InRange(nr, nc)) continue;
				if (grid[nr][nc] == 0) continue;
				if (grid[cur.X][cur.Y] != grid[nr][nc]) continue;
				if (visited[nr][nc]) continue;

				q.push(make_pair(nr, nc));
				visited[nr][nc] = true;
				rows.push_back(nr);
			}
		}
	}

	int ret = 0;
	for (int i = 0; i < (int)rows.size(); i++) {
		ret = max(ret, rows[i]);
	}
	return ret;
}

void reset() {
}

int Move(int r, int c, int n) {
	while (true) {
		if (CanGoDown(r, c)) {
			r++;
		}
		else if (CanGoLeft(r, c)) {
			r++;
			c--;
			dir[n] = (dir[n] - 1) % 4;
		}
		else if (CanGoRight(r, c)) {
			r++;
			c++;
			dir[n] = (dir[n] + 1) % 4;
		}
		else {
			if (r - 1 < 3) {
				memset(grid, 0, sizeof grid);
				memset(isExit, false, sizeof isExit);
				return 0;
			}
			GollemIsHere(r, c, n);
			isExit[r + dr[dir[n]]][c + dc[dir[n]]] = true;
			return bfs(r, c, n) - 3;
		}
	}
}

void print() {
	for (int r = 1; r <= bot; r++) {
		for (int c = 1; c <= C; c++) {
			cout << grid[r][c] << " ";
		}
		cout << endl;
	}
	cout << endl;
	for (int k = 0; k < K; k++) {
		cout << dir[k] << " ";
	}
	cout << endl;
	for (int r = 1; r <= bot; r++) {
		for (int c = 1; c <= C; c++) {
			cout << isExit[r][c] << " ";
		}
		cout << endl;
	}
}

int main() {
	cin >> R >> C >> K;
	bot = R + 3;

	int ans = 0;
	for (int gollem_num = 1; gollem_num <= K; gollem_num++) {
		int c, d;
		cin >> c >> d;
		dir[gollem_num] = d;

		int r = 2;
		ans += Move(r, c, gollem_num);

		// print();
	}
	cout << ans;

	return 0;
}