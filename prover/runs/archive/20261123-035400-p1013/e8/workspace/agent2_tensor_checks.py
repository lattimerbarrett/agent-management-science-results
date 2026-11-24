"""Exact finite checks for the categorical-complete-graph color gadget."""
from itertools import product, combinations
from collections import Counter
import z3

def edges(r,m):
    V=list(product(range(r),repeat=m))
    E=[(i,j) for i,j in combinations(range(len(V)),2)
       if all(a!=b for a,b in zip(V[i],V[j]))]
    return V,E

def dictator_check(r,m):
    V,E=edges(r,m)
    x=[z3.Int('x_%d_%d_%d'%(r,m,i)) for i in range(len(V))]
    S=z3.Solver()
    S.add(*[z3.And(v>=0,v<r) for v in x])
    S.add(*[x[i]!=x[j] for i,j in E])
    # Fix the color permutation by constant vectors.
    for c in range(r): S.add(x[V.index((c,)*m)]==c)
    # Exclude all coordinate projections.
    S.add(*[z3.Or(*[x[i]!=V[i][j] for i in range(len(V))])
            for j in range(m)])
    status=S.check()
    assert status==z3.unsat,(r,m,status)
    # Check tensor spectrum and unique minimum level exactly.
    eigen=Counter()
    from math import comb
    for k in range(m+1):
        eigen[(-1)**k*(r-1)**(m-k)]+=comb(m,k)*(r-1)**k
    assert sum(eigen.values())==r**m
    assert min(eigen)==-(r-1)**(m-1)
    assert eigen[min(eigen)]==m*(r-1)
    return len(V),len(E)

if __name__=='__main__':
    for r,m in [(3,1),(3,2),(3,3),(3,4),(4,2),(4,3),(5,2)]:
        print(r,m,dictator_check(r,m),flush=True)
