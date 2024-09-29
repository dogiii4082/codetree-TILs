import java.util.*;

class Pair {
    int x, y;

    public Pair(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public String toString() {
        return "(" + x + "," + y + ")";
    }
}

public class Main {
    private static final int MAX_N = 20;
    private static final int MAX_M = 5;

    private static int n, m, k;

    private static final int[] dx = {-1, 1, 0, 0};
    private static final int[] dy = {0, 0, -1, 1};

    public static int[][] grid = new int[MAX_N][MAX_N];
    private static ArrayList<Pair>[] teams = new ArrayList[MAX_M];

    public static int ans;

    public static void main(String[] args) {
        Input();


        for (int r = 0; r < k; r++) {
//            System.out.println(r);
//            for (int i = 0; i < n; i++) {
//                for (int j = 0; j < n; j++) {
//                    System.out.print(grid[i][j] + " ");
//                }
//                System.out.println();
//            }
//
        //    for (int i = 0; i < m; i++) {
        //        System.out.println(teams[i]);
        //    }
//            System.out.println(ans);
            move();
//            for (int i = 0; i < n; i++) {
//                for (int j = 0; j < n; j++) {
//                    System.out.print(grid[i][j] + " ");
//                }
//                System.out.println();
//            }

            Pair hit = throwBall(r);
//            System.out.println(hit);
//            System.out.println();

            if (hit.x == -1 && hit.y == -1) continue;

            int idx = 0;
            int tIdx = -1;
            for (int i = 0; i < m; i++) {
                ArrayList<Pair> curTeam = teams[i];

                for (int j = 0; j < curTeam.size(); j++) {
                    if (curTeam.get(j).x == hit.x && curTeam.get(j).y == hit.y) {
                        idx = j;
                        tIdx = i;
                        break;
                    }
                }
            }
            ans += (idx + 1) * (idx + 1);
            if (tIdx != -1) reverse(tIdx);


        }
        System.out.println(ans);
    }

    private static void reverse(int idx) {
        ArrayList<Pair> team = teams[idx];
        Collections.reverse(team);
        teams[idx] = team;

        for (int i = 0; i < teams[idx].size(); i++) {
            if (i == 0) grid[teams[idx].get(i).x][teams[idx].get(i).y] = 1;
            else if (i == teams[idx].size() - 1) grid[teams[idx].get(i).x][teams[idx].get(i).y] = 3;
            else grid[teams[idx].get(i).x][teams[idx].get(i).y] = 2;
        }
    }

    private static void move() {
        for (int i = 0; i < m; i++) {
            ArrayList<Pair> curTeam = teams[i];
            grid[curTeam.get(curTeam.size()-1).x][curTeam.get(curTeam.size()-1).y] = 4;
            ArrayList<Pair> nxtTeam = new ArrayList<Pair>();
            for (int j = 0; j < curTeam.size() - 1; j++) {
                if (j == 0) {
                    Pair head = curTeam.get(0);

                    for (int d = 0; d < 4; d++) {
                        int nx = head.x + dx[d];
                        int ny = head.y + dy[d];

                        if (!inRange(nx, ny)) continue;

                        if (grid[nx][ny] == 4) {
                            nxtTeam.add(new Pair(nx, ny));
                            grid[nx][ny] = 1;
                        }
                    }
                }
                nxtTeam.add(curTeam.get(j));
            }
            teams[i] = nxtTeam;
        }

        for (int i = 0; i < m; i++) {
            ArrayList<Pair> curTeam = teams[i];

            for (int j = 1; j < curTeam.size(); j++) {
                if (j == curTeam.size() - 1) {
                    grid[curTeam.get(j).x][curTeam.get(j).y] = 3;
                } else {
                    grid[curTeam.get(j).x][curTeam.get(j).y] = 2;
                }
            }
        }
    }

    private static Pair throwBall(int r) {
        r %= 4*n;

        if (r / n == 0) {
            for (int i = 0; i < n; i++) {
                if (1 <= grid[r][i] && grid[r][i] <= 3) {
                    return new Pair(r, i);
                }
            }
        } else if (r / n == 1) {
            for (int i = n-1; i >= 0; i--) {
                if (1 <= grid[i][r % n] && grid[i][r % n] <= 3) {
                    return new Pair(i, r % n);
                }
            }
        } else if (r / n == 2) {
            for (int i = n-1; i >= 0; i--) {
                if (1 <= grid[3*n-r-1][i] && grid[3*n-r-1][i] <= 3) {
                    return new Pair(3*n-r-1, i);
                }
            }
        } else {
            for (int i = 0; i < n; i++) {
                if (1 <= grid[i][4*n-r-1] && grid[i][4*n-r-1] <= 3) {
                    return new Pair(i, 4*n-r-1);
                }
            }
        }

        return new Pair(-1, -1);
    }

    private static boolean inRange(int x, int y) {
        return 0 <= x && x < n && 0 <= y && y < n;
    }

    private static void getTeam(Pair p, boolean[][] visited, List<Pair> team, int t) {
        visited[p.x][p.y] = true;
        team.add(new Pair(p.x, p.y));

        if (grid[p.x][p.y] == 3) {  // 목적지인가?
            teams[t].addAll(team);
            return;
        }

        for (int i = 0; i < 4; i++) {
            int nx = p.x + dx[i];
            int ny = p.y + dy[i];

            if (!inRange(nx, ny)) continue;
            if (visited[nx][ny]) continue;
            if (grid[nx][ny] == 0 || grid[nx][ny] == 4) continue;
            if (team.size() == 1 && grid[nx][ny] == 3) continue;

            getTeam(new Pair(nx, ny), visited, team, t);
        }
    }

    private static void Input() {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();
        m = sc.nextInt();
        k = sc.nextInt();
        for (int x = 0; x < n; x++)
            for (int y = 0; y < n; y++)
                grid[x][y] = sc.nextInt();

        for (int i = 0; i < m; i++) teams[i] = new ArrayList<>();

        int t = 0;
        for (int x = 0; x < n; x++) {
            for (int y = 0; y < n; y++) {
                if (grid[x][y] == 1 && t < m) {
                    boolean[][] visited = new boolean[n][n];
                    List<Pair> team = new ArrayList<>();
                    getTeam(new Pair(x, y), visited, team, t);
                    if (!team.isEmpty()) t++;
                }
            }
        }
    }
}