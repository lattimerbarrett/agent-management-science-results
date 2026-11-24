import sympy as s
from itertools import product
n,k=s.symbols('n k', nonzero=True)
for ell in range(9):
    O=s.prod(n/k+j for j in range(ell))/s.factorial(ell)
    A=s.prod(n/k-1+j for j in range(ell))/s.factorial(ell)
    assert s.cancel((n+ell*k-k)*A-(n-k)*O)==0
# Check the complete rank claim for every zero/nonzero lower pattern,
# plus several coefficient values, for g<=16 (exact rational arithmetic).
cases=0
for g in range(2,17):
    r=(g+2)//3; kk=g-r; d=2*g-2
    gaps=list(range(1,2*g,2))
    assert 3*kk>=d and 4*kk>d and kk<d
    assert [h for h in gaps if h>2*kk]==[2*g-1-2*j for j in reversed(range(r))]
    for m in range(r):
        for lower in product((0,1,-2),repeat=m):
            b=list(lower)+( [3] )+[0]*(r-m-1)
            rows=[2*g-1-2*j for j in range(r)]
            # phi*x^a has pole q_a=2g-1-2j+2a.
            M=s.Matrix([[sum(b[j] for j in range(r) if 2*g-1-2*j+2*a==q)
                         for a in range(kk//2+1)] for q in rows])
            assert M.rank()==m+1
            assert all(M[:,a]==s.zeros(r,1) for a in range(m+1,kk//2+1))
            cases+=1
print('9 symbolic divergence identities; exact matrices checked:',cases)
