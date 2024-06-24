import heapq


def Dijkstra(st, en):
    dist = [1e9 for _ in range(n)]

    q = []
    heapq.heappush(q, (0, st))
    dist[st] = 0
    while q:
        curr_w, curr_v = heapq.heappop(q)

        if dist[curr_v] != dist[curr_v]: continue

        for cand_w, cand_u in graph[curr_v]:
            if curr_w + cand_w <= dist[cand_u]:
                dist[cand_u] = curr_w + cand_w
                heapq.heappush(q, (curr_w+cand_w, cand_u))

    return dist[en]


if __name__ == "__main__":
    Q = int(input())

    graph = {}
    travels = []
    n, m = 0, 0
    st = 0
    poss = [True for _ in range(30001)]
    q = []
    for _ in range(Q):
        tmp = list(map(int, input().split()))

        op = tmp[0]
        if op == 100:
            n, m = tmp[1], tmp[2]
            for i in range(3, len(tmp)-2, 3):
                v, u, w = tmp[i], tmp[i+1], tmp[i+2]
                if v in graph and (w, u) not in graph[v]:
                    graph[v].append((w, u))
                elif v not in graph:
                    graph[v] = [(w, u)]
                if u in graph and (w, v) not in graph[u]:
                    graph[u].append((w, v))
                elif u not in graph:
                    graph[u] = [(w, v)]

        elif op == 200:
            id, revenue, dest = tmp[1], tmp[2], tmp[3]
            heapq.heappush(q, (-(revenue-Dijkstra(st, dest)), id, dest, revenue))

        elif op == 300:
            id = tmp[1]
            poss[id] = False

        elif op == 400:
            if q:
                benefit, id, dest, revenue = heapq.heappop(q)
                if benefit > 0 or Dijkstra(st, dest) == 1e9 or not poss[id]:
                    print(-1)
                else:
                    print(id)

            else:
                print(-1)


        elif op == 500:
            s = tmp[1]
            st = s
            q_tmp = []
            for _ in range(len(q)):
                benefit, id, dest, revenue = heapq.heappop(q)
                q_tmp.append((id, dest, revenue))
            for id, dest, revenue in q_tmp:
                heapq.heappush(q, (-(revenue-Dijkstra(st, dest)), id, dest, revenue))