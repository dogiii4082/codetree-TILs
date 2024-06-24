# import heapq
#
#
# def Dijkstra(st, en):
#     dist = [1e9 for _ in range(n)]
#
#     q = []
#     heapq.heappush(q, (0, st))
#     dist[st] = 0
#     while q:
#         curr_w, curr_v = heapq.heappop(q)
#
#         if dist[curr_v] != dist[curr_v]: continue
#
#         for cand_w, cand_u in graph[curr_v]:
#             if curr_w + cand_w <= dist[cand_u]:
#                 dist[cand_u] = curr_w + cand_w
#                 heapq.heappush(q, (curr_w+cand_w, cand_u))
#
#     return dist[en]
#
#
# if __name__ == "__main__":
#     Q = int(input())
#
#     graph = {}
#     travels = []
#     n, m = 0, 0
#     st = 0
#     poss = [True for _ in range(30001)]
#     q = []
#     for _ in range(Q):
#         tmp = list(map(int, input().split()))
#
#         op = tmp[0]
#         if op == 100:
#             n, m = tmp[1], tmp[2]
#             for i in range(3, len(tmp)-2, 3):
#                 v, u, w = tmp[i], tmp[i+1], tmp[i+2]
#                 if v in graph and (w, u) not in graph[v]:
#                     graph[v].append((w, u))
#                 elif v not in graph:
#                     graph[v] = [(w, u)]
#                 if u in graph and (w, v) not in graph[u]:
#                     graph[u].append((w, v))
#                 elif u not in graph:
#                     graph[u] = [(w, v)]
#
#         elif op == 200:
#             id, revenue, dest = tmp[1], tmp[2], tmp[3]
#             heapq.heappush(q, (-(revenue-Dijkstra(st, dest)), id, dest, revenue))
#
#         elif op == 300:
#             t = tmp[1]
#             poss[t] = False
#             q = [(benefit, id, dest, revenue) for benefit, id, dest, revenue in q if id != t]
#             heapq.heapify(q)
#
#         elif op == 400:
#             print(q)
#             while q:
#                 if q[0][0] > 0 or Dijkstra(st, dest) == 1e9 or not poss[id]:
#                     continue
#                 benefit, id, dest, revenue = heapq.heappop(q)
#                 print(id)
#                 break
#
#             else:
#                 print(-1)
#
#
#         elif op == 500:
#             s = tmp[1]
#             st = s
#
#             q_tmp = []
#             for _ in range(len(q)):
#                 benefit, id, dest, revenue = heapq.heappop(q)
#                 q_tmp.append((id, dest, revenue))
#             for id, dest, revenue in q_tmp:
#                 heapq.heappush(q, (-(revenue-Dijkstra(st, dest)), id, dest, revenue))

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
    travels = []
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
            # poss[t] = False
            q = [(benefit, id, dest, revenue) for benefit, id, dest, revenue in q if id != t]
            heapq.heapify(q)

        elif op == 400:
            temp_q = []
            found = False
            while q:
                benefit, id, dest, revenue = heapq.heappop(q)
                if benefit <= 0 and dijkstra(graph, start, dest) != float('inf'):
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