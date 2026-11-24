from itertools import combinations
import sympy as sp

# Symbolic checks of all polynomial identities in the upper bound.
m, q, a = sp.symbols('m q a', integer=True)
i = sp.symbols('i', integer=True, positive=True)
assert sp.simplify(sp.summation(i, (i, 1, m)) + sp.summation(i, (i, 1, m-1)) - m**2) == 0
assert sp.expand(m + 2*(m-1) + 2*(m-2) + 2*(m-3)) == 7*m-12
assert sp.simplify(sp.summation(i+1, (i, 1, m)) + sp.summation(2*m+1-i, (i, m+1, 2*m)) - (m*m+2*m)) == 0
assert sp.expand((m+1) + 2*m + 2*(m-1) + 2*(m-2)) == 7*m-5
assert sp.expand(a*(a-1) - 2*(6*a-21) - (a-6)*(a-7)) == 0
assert sp.expand((m*(m-1) - (m*m-7*m+12))/2) == 3*m-6
assert sp.expand((m*(m+1) - (m*m-5*m+6))/2) == 3*m-3
assert sp.expand((3*m-6)-(6*m-21*q) + 3*(m-7*q+2)) == 0
assert sp.expand((3*m-3)-(6*(m+1)-21*q) + 3*(m-7*q+3)) == 0
# Independent finite checks of gap minimization, including exhaustive
# choices of all seven zero positions for small m.
for M in range(4, 13):
    we = [min(j, 2*M-j) for j in range(1, 2*M)]
    wo = [j+1 if j <= M else 2*M+1-j for j in range(1, 2*M+1)]
    assert sum(we)-sum(sorted(we)[-7:]) == M*M-7*M+12
    assert sum(wo)-sum(sorted(wo)[-7:]) == M*M-5*M+5
    assert {j+1 for j,x in enumerate(we) if x >= M-3} == set(range(M-3, M+4))
    if M <= 9:
        assert min(sum(we)-sum(we[j] for j in Z) for Z in combinations(range(len(we)), 7)) == M*M-7*M+12
        assert min(sum(wo)-sum(wo[j] for j in Z) for Z in combinations(range(len(wo)), 7)) == M*M-5*M+5
print('Symbolic identities and finite gap-minimization checks passed.')

def interval(lo, hi):
    return set(range(lo, hi+1))

# Neighbors in B, indexed from 1.
rows = [set(), set(), set(), {9}, {7,9}, {4,7,9}]
rows += [interval(21-i,18) for i in range(7,12)]
rows += [interval(10,18), {4,8}|interval(10,18), interval(8,18),
         {4,5,6,8}|interval(10,18), interval(6,18), interval(5,18),
         {3}|interval(5,18), {2,3}|interval(5,18)]
assert len(rows) == 19
ca = [0]*6 + [2]*5 + [1,2,1,2,1,1,1,1]
cb = [0]*18
cb[3] = 1
cb[6] = cb[8] = 2

adj = [set() for _ in range(37)]
colors = ca+cb

def edge(u,v):
    assert u != v
    adj[u].add(v)
    adj[v].add(u)

for u in range(19):
    for v in range(u+1,19):
        if ca[u] != ca[v]:
            edge(u,v)
for u,row in enumerate(rows):
    for j in row:
        edge(u,19+j-1)

def verify(Q):
    n = len(adj)
    assert n == 14*Q-5
    assert len(colors) == n and set(colors) == set(range(Q))
    for u in range(n):
        assert u not in adj[u]
        for v in adj[u]:
            assert u in adj[v]
            assert colors[u] != colors[v]
    degrees = [len(S) for S in adj]
    assert set(degrees) == set(range(n-7)) # 0,...,n-8
    assert n-len(set(degrees)) == 7
    return degrees

d = verify(3)
assert d[:19] == [13]*3 + list(range(14,30))
assert d[19:] == list(range(13)) + [13]*5
print('37-vertex base verified: 3 colors, degrees 0,...,29, deficiency 7.')

for Q in range(4,31):
    n = len(adj)
    old_degrees = [len(S) for S in adj]
    # New H: n,...,n+6; new L: n+7,...,n+13.
    adj.extend(set() for _ in range(14))
    colors.extend([Q-1]*7 + [0]*7)
    for h in range(7):
        for u in range(n):
            edge(n+h,u)
        # Bipartite staircase: H row degrees 0,...,6;
        # L column degrees 6,...,0.
        for ell in range(h):
            edge(n+h,n+7+ell)
    assert [len(adj[u]) for u in range(n)] == [x+7 for x in old_degrees]
    assert [len(adj[n+h]) for h in range(7)] == list(range(n,n+7))
    assert [len(adj[n+7+ell]) for ell in range(7)] == list(range(6,-1,-1))
    verify(Q)
print('All extension constructions for q=4,...,30 verified.')
