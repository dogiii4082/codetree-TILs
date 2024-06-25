import heapq


def floyd_warshall(graph, n):
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        for w, j in graph[i]:
            dist[i][j] = min(dist[i][j], w)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist


if __name__ == "__main__":
    Q = int(input())

    graph = {}
    n, m = 0, 0
    start = 0
    tickets = []
    distances = None

    for _ in range(Q):
        tmp = list(map(int, input().split()))
        op = tmp[0]

        if op == 100:
            n, m = tmp[1], tmp[2]
            graph = {i: [] for i in range(n)}
            for i in range(3, len(tmp) - 2, 3):
                v, u, w = tmp[i], tmp[i + 1], tmp[i + 2]
                graph[v].append((w, u))
                graph[u].append((w, v))
            distances = floyd_warshall(graph, n)

        elif op == 200:
            id, revenue, dest = tmp[1], tmp[2], tmp[3]
            travel_cost = distances[start][dest]
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
            start = tmp[1]
            new_tickets = []
            for _, id, dest, revenue in tickets:
                travel_cost = distances[start][dest]
                benefit = revenue - travel_cost
                heapq.heappush(new_tickets, (-benefit, id, dest, revenue))
            tickets = new_tickets