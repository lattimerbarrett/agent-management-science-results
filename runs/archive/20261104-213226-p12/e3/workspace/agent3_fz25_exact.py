from sympy import Rational
import json, math, itertools
P = 1000000007
N = 12
g = 25

def parts(n, lo=1):
    if n == 0:
        yield ()
    for i in range(lo, n + 1):
        for t in parts(n - i, i):
            yield ((i,) + t)

def mul(a, b):
    c = [0] * (N + 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b[:N + 1 - i]):
            c[i + j] = c[i + j] + x * y
    return c
A = [math.factorial(6 * n) // math.factorial(3 * n) // math.factorial(2 * n) for n in range(N + 1)]
B = [A[n] * (6 * n + 1) * Rational(1, 6 * n - 1) for n in range(N + 1)]
Ai = [1] + [0] * N
for n in range(1, N + 1):
    Ai[n] = -sum((A[i] * Ai[n - i] for i in range(1, n + 1)))
D = mul(B, Ai)
Ds = [[1] + [0] * N]
for i in range(10):
    Ds.append(mul(Ds[-1], D))
LA = [0] * (N + 1)
for n in range(1, N + 1):
    LA[n] = sum((i * A[i] * Ai[n - i] for i in range(1, n + 1))) * Rational(1, n)
sigmas = [s for n in range(11) for s in parts(n) if all((x % 3 != 2 for x in s))]
sigmas.sort(key=lambda s: (len(s), s))
from collections import Counter
cs = {s: Counter(s) for s in sigmas}
E = {(): {(): 1}}
for n in range(1, N + 1):
    for k in range(1, n + 1):
        c = -k * LA[k] * Rational(1, n)
        for mon, v in list(E[()].items()):
            if sum(mon) == n - k:
                out = tuple(sorted(mon + (k,)))
                E[()][out] = E[()].get(out, 0) + v * c

def H(s):
    shift = sum((x // 3 for x in s))
    power = sum((x % 3 == 1 for x in s))
    c = (-1) ** (len(s) + 1) * math.factorial(len(s) - 1)
    for v in cs[s].values():
        c = c * Rational(1, math.factorial(v))
    return [0] * shift + [c * x for x in Ds[power][:N + 1 - shift]]
Hs = {s: H(s) for s in sigmas if s}
for s in sigmas:
    if not s:
        continue
    j = s[0]
    den = Rational(1, cs[s][j])
    out = {}
    for t in sigmas:
        if not t or j not in cs[t] or any((cs[t][v] > cs[s][v] for v in cs[t])):
            continue
        u = tuple(sorted((cs[s] - cs[t]).elements()))
        w = -cs[t][j] * den
        for mon, v in E[u].items():
            for n, c in enumerate(Hs[t][:N + 1 - sum(mon)]):
                if not c:
                    continue
                dest = tuple(sorted(mon + (n,))) if n else mon
                factor = 1 if n else 48
                out[dest] = out.get(dest, 0) + w * v * c * factor
    E[s] = out
basis = list(parts(12))
idx = {s: i for i, s in enumerate(basis)}
rows = []
labels = []
for r in range(1, 13):
    for s in sigmas:
        if 3 * r <= 24 + sum(s) or (25 - r - sum(s) - 1) % 2:
            continue
        for m in parts(12 - r):
            row = [0] * len(basis)
            for k, v in E[s].items():
                if sum(k) == r:
                    row[idx[tuple(sorted(k + m))]] = v
            rows.append(row)
            labels.append((r, s, m))
M = [r[:] for r in rows]
rank = 0
piv = []
for j in range(77):
    i = next((i for i in range(rank, len(M)) if M[i][j]), None)
    if i is None:
        continue
    M[rank], M[i] = (M[i], M[rank])
    inv = Rational(1, M[rank][j])
    M[rank] = [x * inv for x in M[rank]]
    for k in range(rank + 1, len(M)):
        a = M[k][j]
        if a:
            M[k] = [x - a * y for x, y in zip(M[k], M[rank])]
    piv.append(j)
    rank += 1
print('rows', len(rows), 'rank', rank, 'dimension', 77 - rank)

