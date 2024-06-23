dx = [0, 1, 0, -1, -1, -1, 1, 1]
dy = [-1, 0, 1, 0, -1, 1, -1, 1]


oppo = {
    0: 2,
    1: 3,
    2: 0,
    3: 1
}


def is_another_santa(r, c, p):
    for i in range(1, P+1):
        if i == p: continue

        if Sr[i] == r and Sc[i] == c:
            return i

    return 0

def distance(r1, c1, r2, c2):
    return (r1-r2)**2 + (c1-c2)**2


def get_target_santa():
    tmp = [(1e9, 1e9, 1e9)]    # (d, r, c, p)
    for p in range(1, P+1):
        if is_end[p]: continue
        tmp.append((distance(Sr[p], Sc[p], Rr, Rc), -Sr[p], -Sc[p], p))
    tmp.sort()
    return tmp[0][3]


def move_rudolph(p, dist, r, c, t):
    for i in range(8):
        if distance(Sr[p], Sc[p], Rr+dx[i], Rc+dy[i]) < dist:
            dist = distance(Sr[p], Sc[p], Rr+dx[i], Rc+dy[i])

            # 루돌프가 움직여 충돌
            if dist == 0:
                score[p] += C
                pause[p] = t+1

                Sr[p] += (dx[i] * C)
                Sc[p] += (dy[i] * C)
                if Sr[p] < 1 or Sr[p] > N or Sc[p] < 1 or Sc[p] > N:
                    is_end[p] = True

                another = is_another_santa(Sr[p], Sc[p], p)
                if another:
                    interaction(another, i)

            r, c = Rr+dx[i], Rc+dy[i]

    return r, c


def interaction(another, d):
    global Sr, Sc, is_end

    Sr[another] += dx[d]
    Sc[another] += dy[d]

    if Sr[another] < 1 or Sr[another] > N or Sc[another] < 1 or Sc[another] > N:
        is_end[another] = True

    other = is_another_santa(Sr[another], Sc[another], another)
    if other:
        interaction(other, d)


def move_santa(t):
    global is_end, Sr, Sc, score, pause

    for p in range(1, P+1):
        if is_end[p] or t <= pause[p]: continue

        d = distance(Rr, Rc, Sr[p], Sc[p])

        sr, sc = Sr[p], Sc[p]
        for i in range(4):
            nr = sr+dx[i]
            nc = sc+dy[i]

            if nr < 1 or nr > N or nc < 1 or nc > N: continue
            if is_another_santa(nr, nc, p): continue

            # 충돌
            if distance(Rr, Rc, nr, nc) == 0:
                score[p] += D
                pause[p] = t+1

                nnr = nr + dx[oppo[i]]*D
                nnc = nc + dy[oppo[i]]*D

                if nnr < 1 or nnr > N or nnc < 1 or nnc > N:
                    is_end[p] = True
                    Sr[p] = nnr
                    Sc[p] = nnc
                    break

                else:
                    Sr[p] = nnr
                    Sc[p] = nnc

                    another = is_another_santa(nnr, nnc, p)
                    if another:
                        interaction(another, oppo[i])


            elif distance(Rr, Rc, nr, nc) <= d:
                d = distance(Rr, Rc, nr, nc)

                Sr[p] = nr
                Sc[p] = nc


if __name__ == "__main__":
    N, M, P, C, D = map(int, input().split())
    Rr, Rc = map(int, input().split())
    Sr = [0 for _ in range(P+1)]
    Sc = [0 for _ in range(P+1)]
    for _ in range(P):
        p, sr, sc = map(int, input().split())
        Sr[p] = sr
        Sc[p] = sc

    pause = [-1 for _ in range(P+1)]
    score = [0 for _ in range(P+1)]
    is_end = [False for _ in range(P+1)]
    is_end[0] = True
    ans = 0
    for t in range(1, M+1):
        if all(is_end): break

        p = get_target_santa()

        dist = distance(Rr, Rc, Sr[p], Sc[p])
        Rr, Rc = move_rudolph(p, dist, Rr, Rc, t)

        move_santa(t)

        for p in range(1, P+1):
            if not is_end[p]:
                score[p] += 1

    print(*score[1:])