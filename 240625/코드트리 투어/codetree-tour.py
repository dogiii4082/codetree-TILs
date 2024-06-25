import heapq

def dijkstra(graph, start):
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

    return dist

if __name__ == "__main__":
    Q = int(input().strip())

    graph = {}
    n, m = 0, 0
    start = 0
    tickets = []
    distances = None

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
            distances = dijkstra(graph, start)

        elif op == 200:
            id, revenue, dest = tmp[1], tmp[2], tmp[3]
            travel_cost = distances[dest]
            benefit = revenue - travel_cost
            heapq.heappush(tickets, (-benefit, id, dest, revenue))

        elif op == 300:
            t = tmp[1]
            tickets = [ticket for ticket in tickets if ticket[1] != t]
            heapq.heapify(tickets)

        elif op == 400:
            if not tickets:
                print(-1)
            else:
                benefit, id, dest, revenue = heapq.heappop(tickets)
                if benefit <= 0:
                    print(id)
                else:
                    print(-1)
                    heapq.heappush(tickets, (benefit, id, dest, revenue))

        elif op == 500:
            new_start = tmp[1]
            if new_start != start:
                start = new_start
                distances = dijkstra(graph, start)
                new_tickets = []
                for _, id, dest, revenue in tickets:
                    travel_cost = distances[dest]
                    benefit = revenue - travel_cost
                    heapq.heappush(new_tickets, (-benefit, id, dest, revenue))
                tickets = new_tickets