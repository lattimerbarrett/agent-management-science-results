import runpy
import numpy as np
from fractions import Fraction

s = runpy.run_path('agents/agent_1/scratchpad.py', run_name='__main__')
adj, weights = s['example']()
A = np.zeros((len(adj), len(adj)), dtype=np.int64)
for v, ns in enumerate(adj):
    A[v, list(ns)] = 1
A2 = A @ A
A3 = A2 @ A
print('Independent adjacency-matrix check: trace A^3 =', np.trace(A3), '; trace A^5 =', np.trace(A3 @ A2))
assert np.trace(A3) == 0
assert np.trace(A3 @ A2) == 0
assert Fraction(sum(weights[j] for j in adj[0]),sum(weights)) > 0
