#include <iostream>
#include <cmath>

#define MAX_N 100
#define MAX_M 10000
#define MAX_H 10000

using namespace std;

int N, M, H, K;
int grid[MAX_N][MAX_N];
int dir[MAX_M];
struct Hider {
    int x, y, d;
} hiders[MAX_M];
struct Tree {
    int x, y;
} trees[MAX_H];
int treeGrid[MAX_N][MAX_N];
int ans;
struct Seeker {
    int x, y, d;
} seeker;
int dx[4] = {-1, 0, 1, 0};
int dy[4] = {0, 1, 0, -1};
bool isRed;
struct Center {
    int x, y;
} center;

void printGrid() {
    for (int i = 1; i <= N; i++) {
        for (int j = 1; j <= N; j++){ 
            cout << grid[i][j] << " ";
        }
        cout << endl;
    }
}

void printHider() {
    for (int i = 1; i <= M; i++) {
        Hider h = hiders[i];
        cout << h.x << " " << h.y << " " << h.d << endl;
    }
}

int distance(int x1, int y1, int x2, int y2) {
    return abs(x1-x2) + abs(y1-y2);
}

bool inRange(int x, int y) {
    return 1 <= x && x <= N && 1 <= y && y <= N;
}

bool isSeeker(int x, int y) {
    return seeker.x == x && seeker.y == y;
}

void move(int pid) {
    int x, y, d;
    x = hiders[pid].x;
    y = hiders[pid].y;
    d = hiders[pid].d;  // 1: (좌, 우), 2: (상, 하)

    int nx = x + dx[d];
    int ny = y + dy[d];

    if (!inRange(nx, ny)) {     // 격자를 벗어나는 경우
        int nd = (d + 2) % 4;

        hiders[pid].d = nd;
        int nnx = x + dx[nd];
        int nny = y + dy[nd];

        if (!isSeeker(nnx, nny)) {
            hiders[pid] = Hider{nnx, nny, nd};
            grid[x][y] = 0;
            grid[nnx][nny] = pid;
        }
    } else {                    // 격자를 벗어나지 않는 경우
        if (isSeeker(nx, ny)) return;
        grid[x][y] = 0;
        hiders[pid] = Hider{nx, ny, d};
        grid[nx][ny] = pid;
    }
}

void moveHider() {
    for (int i = 1; i <= M; i++) {
        if (distance(seeker.x, seeker.y, hiders[i].x, hiders[i].y) <= 3) {
            move(i);
        }
    }
    // cout << "===Hider===" << endl;
    // printHider();
}

void catchHider(int k) {
    int cnt = 0;
    for (int i = 0; i < 3; i++) {
        int x = seeker.x + dx[seeker.d] * i;
        int y = seeker.y + dy[seeker.d] * i;

        if (!inRange(x, y)) continue;
        if (treeGrid[x][y] == 1) continue;

        if (grid[x][y] != 0) cnt++;
    }
    ans += k * cnt;
}

void moveSeeker(int k) {
    int x = seeker.x;
    int y = seeker.y;
    int d = seeker.d;

    if (isRed) {    

        int nx = x + dx[d];
        int ny = y + dy[d];
        int nd = d;

        if (nx < center.x && ny == nx + 1) {
            nd = 1;
        } else if (nx < center.x && (nx + ny == center.x + center.y)) {
            nd = 2;
        } else if (nx > center.x && (nx == ny)) {
            nd = 3;
        } else if (nx > center.x && (nx + ny == center.x + center.y)) {
            nd = 0;
        } else if (nx == 1 && ny == 1) {
            nd = 2;
            isRed = false;
        }

        seeker = Seeker{nx, ny, nd};
        // cout << "===Seeker===" << endl;
        // cout << seeker.x << " " << seeker.y << " " << seeker.d << endl;

        catchHider(k);

    } else {

        int nx = x + dx[d];
        int ny = y + dy[d];
        int nd = d;

        if (nx < center.x && ny == nx + 1) {
            nd = 2;
        } else if (nx < center.x && (nx + ny == center.x + center.y)) {
            nd = 3;
        } else if (nx > center.x && (nx == ny)) {
            nd = 0;
        } else if (nx > center.x && (nx + ny == center.x + center.y)) {
            nd = 1;
        } else if (nx == center.x && ny == center.y) {
            nd = 0;
            isRed = true;
        }

        seeker = Seeker{nx, ny, nd};
        // cout << "===Seeker===" << endl;
        // cout << seeker.x << " " << seeker.y << " " << seeker.d << endl;

        catchHider(k);

    }
}

int main() {
    cin >> N >> M >> H >> K;

    seeker = Seeker{(N+1) / 2, (N+1) / 2, 0};
    center = Center{(N+1) / 2, (N+1) / 2};
    isRed = true;

    for (int i = 1; i <= M; i++) {
        int x, y, d;
        cin >> x >> y >> d;
        dir[i] = d;
        grid[x][y] = i;
        hiders[i] = Hider{x, y, d};
    }

    for (int i = 1; i <= H; i++) {
        int x, y;
        cin >> x >> y;
        treeGrid[x][y] = 1;
        trees[i] = Tree{x, y};
    }

    for (int k = 1; k <= K; k++) {
        // cout << k << "턴=====" << endl;
        moveHider();
        moveSeeker(k);
    }

    cout << ans;

    return 0;
}