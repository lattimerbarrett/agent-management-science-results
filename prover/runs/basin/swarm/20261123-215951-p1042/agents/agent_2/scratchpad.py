from pathlib import Path
code='''"""Independent chain-level verification of the row-four reduction.
Uses no homology conclusions; compares every inclusion to raw simplicial chains.
"""
from itertools import combinations
from math import comb
import sys
sys.path.insert(0, "workspace")
from a3_fiber import fiber_complex

def boundary(t):
    return {t[:i]+t[i+1:]: (-1)**i for i in range(len(t))}

def add(out, c, x):
    for a,b in x.items():
        out[a]=out.get(a,0)+c*b
        if out[a]==0: del out[a]

def verify(m):
    gens,bd,sz=fiber_complex(m)
    ranks=[sum(k==j for k in sz) for j in range(5)]
    expected=[comb(m-1,4),3*m*comb(m-2,3),9*comb(m,2)*comb(m-3,2),24*(m-4)*comb(m,3),54*comb(m,4)]
    assert ranks==expected
    assert sum((-1)**j*ranks[j] for j in range(5))==(m**4+14*m**3-m*m+34*m+24)//24
    for b,(A,T) in enumerate(gens):
        columns={x for x,c in A}
        p=next(x for x in range(m) if x not in columns)
        original=boundary((p,)+T)
        for a in range(len(A)):
            A1=A[:a]+A[a+1:]
            columns1={x for x,c in A1}
            p1=next(x for x in range(m) if x not in columns1)
            reconstructed={}
            for i,sgn in bd[b].items():
                A2,T2=gens[i]
                if A2==A1:
                    add(reconstructed,sgn*(-1)**a,boundary((p1,)+T2))
            assert original==reconstructed
        twice={}
        for i,c in bd[b].items():add(twice,c,bd[i])
        assert not twice
    # For each monochrome triple, Q4 -> Q3 includes the boundaries
    # of every codimension-one face. Those containing the smallest
    # vertex are precisely the defining integral basis, hence span.
    n=m-3; r=m-5
    S=tuple(range(n));p=0
    defining={T for T in combinations(S[1:],r)}
    reached={tuple(x for x in S if x not in (p,j)) for j in S[1:]}
    assert defining==reached
    return len(gens), sum(map(len,bd))

if __name__=="__main__":
    for m in range(7,11):
        print(m,verify(m),flush=True)
'''
Path('workspace/a2_verify.py').write_text(code)
exec(compile(code,'workspace/a2_verify.py','exec'))