from sage.all import GF
from itertools import combinations
from collections import Counter
from math import comb


def make(q):
    K = GF(q*q, 'z')
    els = [K.zero(), K.one()] + [x for x in K if x not in (0, 1)]
    n = q*q
    ix = {a: i for i, a in enumerate(els)}

    add = [[ix[a+b] for b in els] for a in els]
    mul = [[ix[a*b] for b in els] for a in els]
    sub = [[ix[a-b] for b in els] for a in els]
    inv = [0] + [ix[1/a] for a in els[1:]]
    fq = [i for i, a in enumerate(els) if a**q == a]

    # Infinity is represented by n.
    circles = set()

    # Finite norm circles.
    for a in els:
        for r in els:
            if r and r**q == r:
                circles.add(tuple(
                    i for i, z in enumerate(els)
                    if (z-a)**(q+1) == r
                ))

    # Circles containing infinity.
    for a in range(n):
        for b in range(1, n):
            circles.add(tuple(sorted(
                [n] + [add[a][mul[b][s]] for s in fq]
            )))

    C = sorted(circles)
    assert len(C) == q*(q*q+1)

    # Check the complete 3-design, including intersection <= 2.
    triples = set()
    for c in C:
        assert len(c) == q+1
        for tri in combinations(c, 3):
            assert tri not in triples
            triples.add(tri)
    assert len(triples) == comb(n+1, 3)

    M = [sum(1 << p for p in c) for c in C]
    T = [
        sum(1 << a for a, c in enumerate(C) if p in c)
        for p in range(n+1)
    ]

    gen = K.multiplicative_generator()
    lg = {ix[gen**i]: i % (q+1) for i in range(n-1)}

    # ds[C][p] is the scalar-coset shift s_{C,p}.
    ds = []
    for c in C:
        if n in c:
            a, b = c[:2]
            u = (1, a)
            v = (0, sub[b][a])
        else:
            a, b, d = c[:3]
            lam = mul[sub[d][a]][inv[sub[b][d]]]
            u = (1, a)
            v = (lam, mul[lam][b])

        shifts = {}
        for s in fq + [n]:
            if s == n:
                x, y = v
            else:
                x = add[u[0]][mul[s][v[0]]]
                y = add[u[1]][mul[s][v[1]]]
            p = mul[y][inv[x]] if x else n
            shifts[p] = lg[x if x else y]

        assert sorted(shifts) == list(c)
        ds.append(shifts)

    return q, C, M, T, ds, (add, mul, sub, inv, fq)


def hemi(D, sol):
    q, C, M, T, ds, tables = D
    m = q+1
    graph = [[] for _ in range(len(sol)*m)]

    for i, a in enumerate(sol):
        for j in range(i):
            b = sol[j]
            for p in set(C[a]) & set(C[b]):
                delta = (ds[a][p] - ds[b][p]) % m
                for x in range(m):
                    y = (x + delta) % m
                    u, v = i*m+x, j*m+y
                    graph[u].append(v)
                    graph[v].append(u)

    colour = {}
    for v in range(len(graph)):
        if v in colour:
            continue
        colour[v] = 0
        stack = [v]
        while stack:
            x = stack.pop()
            for y in graph[x]:
                if y in colour:
                    if colour[y] == colour[x]:
                        return False
                else:
                    colour[y] = 1-colour[x]
                    stack.append(y)

    # Independently check the half-size consequence of the lemma.
    assert all(
        sum(colour[i*m+j] for j in range(m)) == m//2
        for i in range(len(sol))
    )
    return True


def affine_group(D):
    q, C, M, T, ds, tables = D
    add, mul, sub, inv, fq = tables
    n = q*q
    p = 3 if q == 9 else q
    degree = 4 if q == 9 else 2
    lookup = {c: i for i, c in enumerate(C)}

    def power(x, k):
        y = 1
        while k:
            if k & 1:
                y = mul[y][x]
            x = mul[x][x]
            k //= 2
        return y

    ans = []
    for j in range(degree):
        fr = [power(x, p**j) for x in range(n)]
        for a in fq[1:]:
            for b in fq:
                P = [add[mul[a][fr[x]]][b] for x in range(n)] + [n]
                perm = [
                    lookup[tuple(sorted(P[x] for x in c))]
                    for c in C
                ]
                ans.append((P, perm))
    return ans


def enumerate_nests(D):
    q, C, M, T, ds, tables = D
    fq = tables[-1]
    B = len(C)
    root = C.index(tuple(sorted(fq + [q*q])))
    initial_group = affine_group(D)
    maskid = {m: i for i, m in enumerate(M)}
    out = []

    def rec(sol, U, O, A, G):
        k = len(sol)
        if not O:
            out.append(tuple(sorted(sol)))
            return

        r = q-k
        if r <= 0:
            return
        if any((M[a] & O).bit_count() > 2*r for a in sol):
            return

        if r == 1:
            a = maskid.get(O)
            if a is not None and ((A >> a) & 1):
                out.append(tuple(sorted(sol + [a])))
            return

        lower = q+1-2*(r-1)
        if lower >= 4:
            oldA, A = A, 0
            while oldA:
                v = oldA & -oldA
                oldA -= v
                a = v.bit_length()-1
                if (M[a] & O).bit_count() >= lower:
                    A |= v

        # Choose an open point with the fewest available circles.
        best, best_count, chosen_p = None, B+1, None
        bits = O
        while bits:
            v = bits & -bits
            bits -= v
            p = v.bit_length()-1
            candidates = A & T[p]
            count = candidates.bit_count()
            if not count:
                return
            if count < best_count:
                best, best_count, chosen_p = candidates, count, p

        # The initial group fixes infinity, so choose it at the root.
        if k == 1:
            chosen_p = q*q
            best = A & T[chosen_p]
        if not best:
            return

        if len(G) > 1:
            G = [g for g in G if g[0][chosen_p] == chosen_p]
        symmetry = len(G) > 1

        while best:
            v = best & -best
            a = v.bit_length()-1
            m = M[a]

            if symmetry:
                orbit = sum(1 << b for b in {g[1][a] for g in G})
            else:
                orbit = v

            best &= ~orbit

            # In this branch retain other members of the orbit.
            nextA = A & ~v

            # Later sibling branches exclude the whole orbit.
            A &= ~orbit

            nextO = O ^ m
            if (m & nextO).bit_count() > 2*(r-1):
                continue

            newly_saturated = m & O
            while newly_saturated:
                w = newly_saturated & -newly_saturated
                newly_saturated -= w
                nextA &= ~T[w.bit_length()-1]

            nextG = (
                [g for g in G if g[1][a] == a]
                if symmetry else G
            )
            rec(sol + [a], U | m, nextO, nextA, nextG)

    rec(
        [root], M[root], M[root],
        ((1 << B)-1) ^ (1 << root),
        initial_group
    )
    return out


def root_group(D):
    q, C, M, T, ds, tables = D
    add, mul, sub, inv, fq = tables
    n = q*q
    lookup = {c: i for i, c in enumerate(C)}
    aff = affine_group(D)
    G = [g[1] for g in aff]

    # PGL(2,q) is the union of its affine subgroup and the maps
    # affine o (x -> 1/(x-c)), c in F_q.
    for c in fq:
        P = [
            inv[sub[x][c]] if x != c else n
            for x in range(n)
        ] + [0]
        ip = [
            lookup[tuple(sorted(P[x] for x in circle))]
            for circle in C
        ]
        G += [
            [g[1][ip[a]] for a in range(len(C))]
            for g in aff
        ]

    assert len(G) == q*(q*q-1)*(4 if q == 9 else 2)
    return G


def bad_classes(D, sols):
    q, C, M, T, ds, tables = D
    add, mul, sub, inv, fq = tables
    n = q*q
    G = root_group(D)

    def canon(s):
        return min(tuple(sorted(g[a] for a in s)) for g in G)

    rooted = {canon(s) for s in sols}
    rooted_counts = Counter(map(len, rooted))
    lookup = {c: i for i, c in enumerate(C)}
    rebasing = {}

    def change_root(s, r):
        if r not in rebasing:
            a, b, c = C[r][:3]  # These are finite.
            f = mul[sub[c][a]][inv[sub[c][b]]]
            # f*(x-b)/(x-a) sends (a,b,c) to (infinity,0,1).
            P = [
                mul[mul[sub[x][b]][inv[sub[x][a]]]][f]
                if x != a else n
                for x in range(n)
            ] + [f]
            rebasing[r] = [
                lookup[tuple(sorted(P[x] for x in circle))]
                for circle in C
            ]
        g = rebasing[r]
        return tuple(sorted(g[a] for a in s))

    ans = []
    while rooted:
        s = min(rooted)
        orbit = {canon(change_root(s, r)) for r in s}
        rooted.difference_update(orbit)
        ans.append(min(orbit))

    rooting_counts = [
        (len(s), len({canon(change_root(s, r)) for r in s}))
        for s in ans
    ]
    return ans, rooted_counts, rooting_counts


def check_nests(D, out):
    q, C, M, T, ds, tables = D
    assert len(out) == len(set(out))

    for s in out:
        assert 1 <= len(s) <= q
        counts = Counter(p for a in s for p in C[a])
        assert set(counts.values()) == {2}

        seen = {s[0]}
        while True:
            new = seen | {
                b for b in s
                if any(M[b] & M[a] for a in seen)
            }
            if new == seen:
                break
            seen = new
        assert len(seen) == len(s)


if __name__ == '__main__':
    coefficients = {}

    for q in (5, 7, 9, 11):
        D = make(q)
        out = enumerate_nests(D)
        check_nests(D, out)

        bad = [s for s in out if not hemi(D, s)]
        if bad:
            representatives, rooted, rootings = bad_classes(D, bad)
        else:
            representatives, rooted, rootings = [], Counter(), []

        print("q =", q, flush=True)
        print(" search:", sorted(Counter(map(len, out)).items()), flush=True)
        print(" bad:", sorted(Counter(map(len, bad)).items()), flush=True)
        print(" rooted bad:", sorted(rooted.items()), flush=True)
        print(" bad classes:",
              sorted(Counter(map(len, representatives)).items()), flush=True)
        print(" rooting orbit counts:", sorted(rootings), flush=True)

        for t, number in Counter(map(len, representatives)).items():
            coefficients[q, t] = number

    print("Nonzero coefficients:", sorted(coefficients.items()))
