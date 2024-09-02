#include <iostream>

#define MAX 100001
#define MAKE_FACTORY 100
#define MOVE_ALL 200
#define CHANGE_FRONT 300
#define DIVIDE 400
#define GET_GIFT_INFO 500
#define GET_BELT_INFO 600
#define endl "\n"

using namespace std;

int q;
int n, m;	// n: 벨트의 개수, m: 선물의 개수
int m_src, m_dst;
int a, b, c;

struct BELT {
	int front;
	int cnt;
	int back;
};

struct PRESENT {
	int prev;
	int num;
	int next;
};

BELT belt[MAX];
PRESENT present[MAX];

void printBelt() {
	for (int i = 1; i <= n; i++) {
		cout << "=====" << i << "번 벨트=====" << endl;
		cout << belt[i].front << " " << belt[i].cnt << " " << belt[i].back << endl;
	}
}

void printPresent() {
	for (int i = 1; i <= m; i++) {
		cout << "-----" << i << "번 선물-----" << endl;
		cout << present[i].prev << " " << present[i].num << " " << present[i].next << endl;
	}
}

void init() {
	for (int i = 1; i < MAX; i++) {
		belt[i] = BELT{ -1, 0, -1 };
		present[i] = PRESENT{ -1, 0, -1 };
	}
}

void MakeFactory(int b, int p) {
	if (belt[b].front == -1) {	// 벨트 비어있으면
		belt[b] = BELT{ p, 1, p };
		present[p] = PRESENT{ -1, p, -1 };
	}
	else {
		present[p].prev = belt[b].back;
		present[present[p].prev].next = p;
		present[p].num = p;
		belt[b].back = p;
		belt[b].cnt++;
	}
}

void MoveAll(int src, int dst) {
	int dst_back = belt[dst].cnt == 0 ? belt[src].back : belt[dst] .back;
	belt[dst].cnt += belt[src].cnt;
	present[belt[src].back].next = belt[dst].front;
	present[belt[dst].front].prev = belt[src].back;
	belt[dst].front = belt[src].front;
	belt[dst].back = dst_back;
	belt[src] = BELT{ -1, 0, -1 };
}

void ChangeFront(int src, int dst) {
	int src_front = belt[src].front;
	int dst_front = belt[dst].front;

	if (belt[src].cnt != 0 && belt[dst].cnt != 0) {	// 둘 다 비어있지 않으면
		belt[src] = BELT{ dst_front, belt[src].cnt, belt[src].back };
		belt[dst] = BELT{ src_front, belt[dst].cnt, belt[dst].back };

		present[src_front].next = present[belt[dst].front].next;
		present[dst_front].next = present[belt[src].front].next;
		return;
	}

	
	if (belt[src].cnt == 0 && belt[dst].cnt != 0) {
		belt[src] = BELT{ belt[dst].front, 1, belt[dst].front };
		belt[dst] = BELT{ present[belt[dst].front].next, belt[dst].cnt - 1, belt[dst].back };

		present[present[dst_front].next].prev = -1;
		present[dst_front] = PRESENT{ -1, dst_front, -1 };
	}
	else if (belt[src].cnt != 0 && belt[dst].cnt == 0) {
		belt[dst] = BELT{ belt[src].front, 1, belt[src].front };
		belt[src] = BELT{ present[belt[src].front].next, belt[src].cnt - 1, belt[src].back };

		present[present[src_front].next].prev = -1;
		present[src_front] = PRESENT{ -1, src_front, -1 };
	}
}

void Divide(int src, int  dst) {
	int cnt = belt[src].cnt;

	if (cnt == 1) return;

	for (int i = 0; i < cnt / 2; i++) {
		int src_front = belt[src].front;	// 3

		belt[src].front = present[src_front].next;
		belt[src].cnt--;

		present[src_front].next = belt[dst].front;
		present[src_front].prev = -1;
		present[belt[dst].front].prev = src_front;
		belt[dst].front = src_front;
		
		belt[dst].cnt++;

	}
}

int main() {
	ios::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);

	cin >> q;
	init();

	while (q--) {
		int cmd;
		cin >> cmd;

		switch (cmd)
		{
		case MAKE_FACTORY:
			cin >> n >> m;

			for (int present_num = 1; present_num <= m; present_num++) {
				int belt_num;
				cin >> belt_num;
				MakeFactory(belt_num, present_num);
			}

			break;

		case MOVE_ALL:
			cin >> m_src >> m_dst;

			MoveAll(m_src, m_dst);

			cout << belt[m_dst].cnt << endl;

			/*printBelt();
			printPresent();*/

			break;

		case CHANGE_FRONT:
			cin >> m_src >> m_dst;

			ChangeFront(m_src, m_dst);

			cout << belt[m_dst].cnt << endl;

			/*printBelt();
			printPresent();*/

			break;

		case DIVIDE:
			cin >> m_src >> m_dst;

			Divide(m_src, m_dst);

			cout << belt[m_dst].cnt << endl;

			/*printBelt();
			printPresent();*/

			break;
		case GET_GIFT_INFO:
			int p_num;
			cin >> p_num;

			a = present[p_num].prev;
			b = present[p_num].next;

			cout << a + (2 * b) << endl;

			break;
		case GET_BELT_INFO:
			int b_num;
			cin >> b_num;

			a = belt[b_num].front;
			b = belt[b_num].back;
			c = belt[b_num].cnt;

			cout << a + (2 * b) + (3 * c) << endl;

			break;

		default:
			break;
		}
	}

	return 0;
}