"""Exact rational certificate computation for P4 ranks(2,3,2).
Run from repository root: python workspace/agent1_case232_check.py
No modular result is used in this proof computation.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import sympy as s
from sympy.polys.matrices import DomainMatrix
from sympy.polys.domains import QQ
from sympy.polys.orderings import monomial_key
from itertools import product
from agent1_chern_eliminate import system

def check():
    es,vs,_=system((2,3,2))
    D=8
    mons=[m for m in product(range(D+1),repeat=len(vs)) if sum(m)<=D]
    mons.sort(key=monomial_key('grevlex'),reverse=True)
    inds={m:i for i,m in enumerate(mons)}
    rows=[]
    for e in es:
        p=s.Poly(e,*vs,domain=QQ)
        terms=p.rep.to_dict(); d=p.total_degree()
        for m in mons:
            if sum(m)+d>D: continue
            rows.append({inds[tuple(a+b for a,b in zip(k,m))]:c
                         for k,c in terms.items()})
    M=DomainMatrix.from_dod(dict(enumerate(rows)),(len(rows),len(mons)),QQ)
    R,piv=M.rref()
    low=[]
    for row in R.to_dod().values():
        if max(sum(mons[j]) for j in row)<=3:
            low.append(sum(s.sympify(c)*s.prod(v**a for v,a in zip(vs,mons[j]))
                           for j,c in row.items()))
    # Every low polynomial is an exact Q-linear combination of polynomial
    # multiples of the original equations, hence adding them preserves ideal.
    G=s.groebner(low+es,*vs,order='grevlex')
    a,u,b,v,w=vs
    expected=[u*u,u*v,v*v-w,u*w,v*w-v,w*w-w,a+3*u+(v-w)/2,b]
    assert list(G)==expected
    assert G.reduce(a*(a+v))[1]==0
    print('Macaulay shape:',M.shape,'rank:',len(piv))
    print('Exact Groebner basis:',list(G))
    print('bottom_c1 * top_c1 vanishes: verified')
    return list(G)

if __name__=='__main__': check()
