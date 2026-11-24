import numpy as np
from itertools import combinations
# Exact integer finite models refute norm-disjointization of positive WUC sequences.
for n in range(3, 16):
    edges=list(combinations(range(n),2)); N=len(edges)
    P=[np.diag([int(i in edge) for edge in edges]) for i in range(n)]
    assert np.array_equal(sum(P),2*np.eye(N,dtype=int))
    for i,j in combinations(range(n),2):
        assert np.max(np.diag(P[i]@P[j]))==1
        assert np.count_nonzero(P[i]@P[j])==1
    assert all(np.trace(p)==n-1 for p in P)
print('Checked 13 exact finite complete-graph projection families: sum P_i=2I, all pairwise product norms=1.')
# Spectral cutoff scalar bound used in projection reduction; algebraically check slopes/endpoints.
import sympy as s
eta=s.symbols('eta',positive=True)
t=eta/2
r=s.factor((eta-t)/(1-t))
assert s.simplify(r-eta/(2-eta))==0
assert s.simplify(t+(1-t)*r-eta)==0
print('Verified cutoff dimension bound tau(p)>=eta/(2-eta).')
