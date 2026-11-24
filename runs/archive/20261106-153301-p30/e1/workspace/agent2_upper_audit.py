"""Independent computational audit of the upper-bound mod-2 zero count.
No external process/network used. All combinatorial assertions are exact.
"""
from math import comb
from itertools import combinations
import sympy as sp
from pathlib import Path


def lucas2(n,k):
    return int(k >= 0 and (k & ~n) == 0)


def check_arithmetic(max_s=15):
    out=[]
    for s in range(3,max_s+1):
        m=1<<(s-1); j=2*m-2; d=3*m-2; a=d-2; b=d
        assert a+b==3*j
        assert a-j==m-2 and b-j==m
        # Lucas proves this for arbitrary s; independently compute exact binomial.
        c=comb(j,m-2)
        assert c%2==lucas2(j,m-2)==1
        # Complete binary expansion gives all odd positions of (1+t)^j.
        assert j == sum(1<<r for r in range(1,s))
        assert m-2 == sum(1<<r for r in range(1,s-1))
        # In the cohomology quotient the indicated surviving monomial has degree 3j.
        assert j+(m-2)==a and j+(j-(m-2))==b
        out.append((s,j,d,c%2))
    return out


def reference_section_audit(s=3):
    """Explicit reference section on RP^a x RP^b.
    Basic rows use t=1..j, mixed rows t=j+1..2j.
    Any r rows in r columns are a Vandermonde matrix; determinant product
    of pairwise differences proves every required rank symbolically.
    For s=3 enumerate all zeros, build exact rational kernels, and check
    the nonzero other factor in every mixed product.
    """
    m=1<<(s-1); j=2*m-2; a=3*m-4; b=3*m-2
    def row(t,dim): return [sp.Integer(t)**k for k in range(dim+1)]
    basic=list(range(1,j+1)); mixed=list(range(j+1,2*j+1))
    count=0
    for S_tuple in combinations(range(j),a-j):
        S=set(S_tuple)
        first=basic+[mixed[r] for r in range(j) if r in S]
        second=basic+[mixed[r] for r in range(j) if r not in S]
        A=sp.Matrix([row(t,a) for t in first])
        B=sp.Matrix([row(t,b) for t in second])
        u=A.nullspace();v=B.nullspace()
        assert len(u)==len(v)==1
        u=u[0];v=v[0]
        # Full row rank gives transverse linear systems. For product equations
        # every vanishing factor is multiplied by a nonzero factor.
        assert A.rank()==a and B.rank()==b
        for r,t in enumerate(mixed):
            lu=(sp.Matrix([row(t,a)])*u)[0]
            mv=(sp.Matrix([row(t,b)])*v)[0]
            assert lu*mv==0
            assert (lu==0)==(r in S)
            assert (mv==0)==(r not in S)
        count+=1
    assert count==comb(j,a-j) and count%2==1
    return {'s':s,'j':j,'a':a,'b':b,'reference_zeros':count,'all_transverse':True}

if __name__=='__main__':
    Path('workspace/agent2_upper_audit.py').write_text(Path(__file__).read_text())
    print('Exact binomial checks (s,j,d,parity):')
    print(check_arithmetic())
    print('Explicit projective reference-section audit:')
    print(reference_section_audit())
