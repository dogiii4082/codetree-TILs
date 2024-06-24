import heapq


def dijkstra(graph, start, end):
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    q = [(0, start)]

    while q:
        curr_w, curr_v = heapq.heappop(q)

        if curr_w > dist[curr_v]:
            continue

        for cand_w, cand_u in graph[curr_v]:
            new_dist = curr_w + cand_w
            if new_dist < dist[cand_u]:
                dist[cand_u] = new_dist
                heapq.heappush(q, (new_dist, cand_u))

    return dist[end]


if __name__ == "__main__":
    Q = int(input().strip())

    graph = {}
    n, m = 0, 0
    start = 0
    poss = [True] * 30001
    q = []

    for _ in range(Q):
        tmp = list(map(int, input().strip().split()))
        op = tmp[0]

        if op == 100:
            n, m = tmp[1], tmp[2]
            graph = {i: [] for i in range(n)}
            for i in range(3, len(tmp) - 2, 3):
                v, u, w = tmp[i], tmp[i + 1], tmp[i + 2]
                graph[v].append((w, u))
                graph[u].append((w, v))

        elif op == 200:
            id, revenue, dest = tmp[1], tmp[2], tmp[3]
            travel_cost = dijkstra(graph, start, dest)
            benefit = revenue - travel_cost
            heapq.heappush(q, (-(benefit), id, dest, revenue))

        elif op == 300:
            t = tmp[1]
            q = [(benefit, id, dest, revenue) for benefit, id, dest, revenue in q if id != t]
            heapq.heapify(q)

        elif op == 400:
            temp_q = []
            found = False
            while q:
                benefit, id, dest, revenue = heapq.heappop(q)
                if benefit <= 0 and benefit != float('inf'):
                    print(id)
                    found = True
                    break
                temp_q.append((benefit, id, dest, revenue))

            for item in temp_q:
                heapq.heappush(q, item)

            if not found:
                print(-1)

        elif op == 500:
            start = tmp[1]
            updated_q = []
            while q:
                benefit, id, dest, revenue = heapq.heappop(q)
                travel_cost = dijkstra(graph, start, dest)
                new_benefit = revenue - travel_cost
                updated_q.append((-(new_benefit), id, dest, revenue))
            for item in updated_q:
                heapq.heappush(q, item)