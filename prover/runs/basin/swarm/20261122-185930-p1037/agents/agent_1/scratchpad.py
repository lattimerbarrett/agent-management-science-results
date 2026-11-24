# Python 3; exact integer/Laurent-polynomial arithmetic only.
import itertools as it
from functools import lru_cache

# A Laurent polynomial is a sorted tuple of (exponent, integer coefficient).
ZERO, ONE = (), ((0, 1),)
def mon(e, c=1): return ((e, c),) if c else ZERO
def add(a, b):
    d = dict(a)
    for e, c in b:
        d[e] = d.get(e, 0) + c
        if not d[e]: del d[e]
    return tuple(sorted(d.items()))
def neg(a): return tuple((e, -c) for e, c in a)
def shift(a, e, c=1): return tuple((f+e, c*d) for f, d in a) if c else ZERO
def mul(a, b):
    if not a or not b: return ZERO
    if len(a) == 1: return shift(b, *a[0])
    if len(b) == 1: return shift(a, *b[0])
    d = {}
    for e, c in a:
        for f, h in b: d[e+f] = d.get(e+f, 0) + c*h
    return tuple((e, c) for e, c in sorted(d.items()) if c)
def bar(a): return tuple((-e, c) for e, c in reversed(a))
def at1(a): return sum(c for e, c in a)
def put(d, k, v):
    z = add(d.get(k, ZERO), v)
    if z: d[k] = z
    elif k in d: del d[k]

def inv(p): return sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))
P4 = [(p, inv(p)) for p in it.permutations(range(4))]

# Normalize a word in matrix entries to row-major order, using exactly
# the four quantum-matrix relations in the question. Indices are 0-based.
@lru_cache(maxsize=200000)
def normal(w):
    for k in range(len(w)-1):
        x, y = w[k:k+2]
        if x > y:
            a, s = y; b, t = x
            v = w[:k] + (y, x) + w[k+2:]
            if a == b or s == t:
                return {z: shift(c, -1) for z, c in normal(v).items()}
            d = normal(v).copy()
            if s < t:
                v = w[:k] + ((a, t), (b, s)) + w[k+2:]
                for z, c in normal(v).items():
                    put(d, z, mul(c, ((-1, 1), (1, -1))))
            return d
    return {w: ONE}

@lru_cache(None)
def pair_polynomial(I, J):
    d = {}
    for p, l in P4:
        w = tuple((a, I[p[a]]) for a in range(4))
        for z, m in P4:
            v = w + tuple((a, J[z[a]]) for a in range(4))
            for v1, c in normal(v).items(): put(d, v1, shift(c, l+m, (-1)**(l+m)))
    return d

def standard(w):
    return all(all(a <= b for a, b in zip(I, J)) for I, J in zip(w, w[1:]))

# Obtain a two-minor straightening identity by exact polynomial elimination.
@lru_cache(None)
def small_rule(I, J):
    if standard((I, J)): return {(I, J): ONE}
    d, out = pair_polynomial(I, J).copy(), {}
    while d:
        w = min(d)
        rows = [[s for a, s in w if a == r] for r in range(4)]
        K, L = (tuple(row[j] for row in rows) for j in range(2))
        assert all(K[i] < K[i+1] and L[i] < L[i+1] for i in range(3))
        p = pair_polynomial(K, L)
        lead = p[w]
        assert len(lead) == 1 and abs(lead[0][1]) == 1
        c = shift(d[w], -lead[0][0], lead[0][1])
        put(out, (K, L), c)
        for v, h in p.items(): put(d, v, neg(mul(c, h)))
    return out

@lru_cache(None)
def rule(I, J):
    vals = sorted(set(I+J)); idx = {v: i for i, v in enumerate(vals)}
    A, B = tuple(idx[x] for x in I), tuple(idx[x] for x in J)
    return {tuple(tuple(vals[x] for x in C) for C in w): c
            for w, c in small_rule(A, B).items()}

@lru_cache(maxsize=200000)
def straighten(w):
    for k, (I, J) in enumerate(zip(w, w[1:])):
        if not standard((I, J)):
            d = {}
            for (K, L), c in rule(I, J).items():
                for v, h in straighten(w[:k]+(K, L)+w[k+2:]).items():
                    put(d, v, mul(c, h))
            return d
    return {w: ONE}

def key(T): return tuple(x for row in zip(*T) for x in row)
def prec(S, T):
    strict = False
    for h in range(1, 5):
        for r in range(10):
            s = sum(x <= r for I in S for x in I[:h])
            t = sum(x <= r for I in T for x in I[:h])
            if s > t: return False
            strict |= s < t
    return strict

# Independently check that bar fixes a quantum 4-minor.
d, e = {}, {}
for p, l in P4:
    w = tuple((a, p[a]) for a in range(4))
    for v, c in normal(w).items(): put(d, v, shift(c, l, (-1)**l))
    for v, c in normal(w[::-1]).items(): put(e, v, shift(c, -l, (-1)**l))
assert d == e

# Expand the 5x5 hollow determinant, grouping identical graph monomials.
graph_coeff = {}
for p in it.permutations(range(5)):
    if any(i == p[i] for i in range(5)): continue
    g = tuple(sorted(tuple(sorted((i, p[i]))) for i in range(5)))
    graph_coeff[g] = graph_coeff.get(g, 0) + (-1)**inv(p)
assert len(graph_coeff) == 22
D, tabs = {}, set()
for g, c in graph_coeff.items():
    w = tuple(tuple(x for v in edge for x in (2*v, 2*v+1)) for edge in g)
    s = straighten(w); tabs.update(s)
    for T, a in s.items(): put(D, T, mon(0, c*at1(a)))
assert len(tabs) == 269 and len(D) == 130

# Close the finite set under bar. All these tableaux have beta=30.
bars, todo = {}, list(tabs)
while todo:
    T = todo.pop()
    assert standard(T) and len(T) == 5
    assert [sum(I.count(s) for I in T) for s in range(10)] == [2]*10
    bars[T] = {S: shift(c, 30) for S, c in straighten(T[::-1]).items()}
    for S in bars[T]:
        if S not in tabs: tabs.add(S); todo.append(S)
assert len(tabs) == 271

# Construct canonical elements in normalized-standard-monomial coordinates.
order = sorted(tabs, key=key, reverse=True)
B = {}
for i, T in enumerate(order):
    d = bars[T].copy(); put(d, T, mon(0, -1))
    b = {T: ONE}
    for S in reversed(order[:i]):
        if S not in d: continue
        c = d[S]
        assert c == neg(bar(c))
        a = tuple((e, h) for e, h in c if e < 0)
        for U, v in B[S].items():
            put(b, U, mul(a, v))
            put(d, U, neg(mul(c, v)))
    assert not d
    B[T] = b

# Verify every defining condition, including the actual dominance order.
for T, b in B.items():
    assert b[T] == ONE
    for S, c in b.items():
        if S != T: assert prec(S, T) and all(e < 0 for e, h in c)
    bb = {}
    for S, c in b.items():
        for U, v in bars[S].items(): put(bb, U, mul(bar(c), v))
    assert bb == b

# Normalize and decompose at q=1, with no conjectured coefficients supplied.
assert D[min(D, key=key)] == mon(0, 2)
f = {T: mon(0, at1(c)//2) for T, c in D.items()}
assert all(at1(c) % 2 == 0 for c in D.values())
answer = {}
for T in reversed(order):
    if T not in f: continue
    a = at1(f[T]); answer[T] = a
    for S, c in B[T].items(): put(f, S, mon(0, -a*at1(c)))
assert not f
answer = {tuple(tuple(x+1 for x in I) for I in T): a for T, a in answer.items()}
expected = {
 ((1,2,4,6),(1,2,4,8),(3,5,6,8),(3,7,9,10),(5,7,9,10)): 1,
 ((1,2,3,4),(1,2,5,6),(3,4,7,8),(5,6,9,10),(7,8,9,10)): 2}
assert answer == expected

# Reducedness certificate for the geometric equation.
def det(M):
    n = len(M)
    return sum((-1)**inv(p) * product(M[i][p[i]] for i in range(n))
               for p in it.permutations(range(n)))
def product(xs):
    z = 1
    for x in xs: z *= x
    return z
def example(t):
    A = [[1,1,1,2,1,-1,1,0,1,3], [0,2,1,0,2,1,3,-2,4,1],
         [t,1,0,3,0,2,0,1,0,-1], [0,2,0,-1,0,1,0,3,0,2]]
    G = [[0]*5 for _ in range(5)]
    for i in range(5):
        for j in range(i+1,5):
            cols = (2*i,2*i+1,2*j,2*j+1)
            G[i][j] = G[j][i] = det([[row[k] for k in cols] for row in A])
    if t == 0:
        assert any(det([[row[k] for k in cols] for row in A])
                   for cols in it.combinations(range(10),4))
    return det(G)
# This determinant has degree at most two in t, so three values suffice.
assert [example(t) for t in (-1,0,1)] == [0,0,-84000]
print('Verified: 22 graph monomials; 271 canonical certificates; D/2 = b(T1)+2b(T2).')
for T, a in sorted(answer.items(), key=lambda x: key(x[0])): print(a, T)
