#include <iostream>
#include <deque>

#define MAKE_FACTORY 100
#define MOVE_ALL 200
#define CHANGE_FRONT 300
#define DIVIDE 400
#define GET_PRESENT_INFO 500
#define GET_BELT_INFO 600
#define MAX_N 100001
#define endl "\n"

using namespace std;

int q;
int n, m;
int m_src, m_dst;
deque<int> belt[MAX_N];
int p2b[MAX_N];

int MoveAll(int src, int dst) {
	while (!belt[src].empty()) {
		int p = belt[src].back(); belt[src].pop_back();
		p2b[p] = dst;
		belt[dst].push_front(p);
	}

	return belt[dst].size();
}

int ChangeFront(int src, int dst) {
	int s, d;

	if (!belt[src].empty() && !belt[dst].empty()) {
		s = belt[src].front(); belt[src].pop_front();
		d = belt[dst].front(); belt[dst].pop_front();
		p2b[s] = dst; p2b[d] = src;
		belt[src].push_front(d); belt[dst].push_front(s);
	}
	else if (belt[src].empty() && !belt[dst].empty()) {
		d = belt[dst].front(); belt[dst].pop_front();
		p2b[d] = src;
		belt[src].push_back(d);
	}
	else if (!belt[src].empty() && belt[dst].empty()) {
		s = belt[src].front(); belt[src].pop_front();
		p2b[s] = dst;
		belt[dst].push_back(s);
	}

	return belt[dst].size();
}

int Divide(int src, int dst) {
	int cnt = belt[src].size();

	if (cnt== 1) return belt[dst].size();

	for (int i = 0; i < cnt / 2; i++) {
		int p = belt[src].front(); belt[src].pop_front();
		p2b[p] = dst;
		belt[dst].push_front(p);
	}

	return belt[dst].size();
}

int GetPresentInfo(int p) {
	int a = -1;
	int b = -1;

	int belt_num = p2b[p];

	deque<int> curr_belt = belt[belt_num];

	if (curr_belt.size() == 1) {
		return -3;
	}

	for (int i = 0; i < curr_belt.size(); i++) {
		if (curr_belt[i] == p) {
			if (i == 0) {	// 맨 앞: 앞 선물이 없음
				b = curr_belt[i + 1];
			}
			else if (i == curr_belt.size() - 1) {	// 맨 뒤: 뒤 선물이 없음
				a = curr_belt[i - 1];
			}
			else {
				a = curr_belt[i - 1];
				b = curr_belt[i + 1];
			}
		}
	}

	return a + (2 * b);
}

int GetBeltInfo(int b_num) {
	if (belt[b_num].empty()) return -3;

	int a = belt[b_num].front();
	int b = belt[b_num][belt[b_num].size() - 1];
	int c = belt[b_num].size();

	return a + (2 * b) + (3 * c);
}

int main() {
	cin >> q;

	while (q--) {
		int op;
		cin >> op;

		switch (op)
		{
		case MAKE_FACTORY:
			cin >> n >> m;

			for (int present_num = 1; present_num <= m; present_num++) {
				int belt_num;
				cin >> belt_num;
				p2b[present_num] = belt_num;
				belt[belt_num].push_back(present_num);
			}

			break;
		case MOVE_ALL:
			cin >> m_src >> m_dst;

			cout << MoveAll(m_src, m_dst) << endl;

			break;
		case CHANGE_FRONT:
			cin >> m_src >> m_dst;

			cout << ChangeFront(m_src, m_dst) << endl;

			break;
		case DIVIDE:
			cin >> m_src >> m_dst;

			cout << Divide(m_src, m_dst) << endl;

			break;
		case GET_PRESENT_INFO:
			int p_num;
			cin >> p_num;
			
			cout << GetPresentInfo(p_num) << endl;

			break;
		case GET_BELT_INFO:
			int b_num;
			cin >> b_num;

			cout << GetBeltInfo(b_num) << endl;

			break;
		}
	}

	return 0;
}