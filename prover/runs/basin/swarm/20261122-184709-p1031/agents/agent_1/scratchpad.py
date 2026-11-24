from math import comb
from fractions import Fraction

def vals(n,r,q):
    a=2*sum(comb(n-1,k) for k in range(r))
    s=2**q-1
    b=sum((-1)**(r-k)*comb(n,k)*s**k for k in range(r)) + sum(comb(n,k)*s**k for k in range(r,n+1))
    c=comb(n,r)*q**r
    return a,b,c

fail=[]
for n in range(2,32):
    for r in range(1,n):
        a,b,c=vals(n,r,2)
        if a*b<c*c:
            fail.append((n,r))
            print('failure',n,r,'A,B,C =',a,b,c,'C^2-AB =',c*c-a*b)
assert fail==[(31,21),(31,22)]
print('All',sum(n-1 for n in range(2,31)),'cases with n<31 pass.')
for n in range(2,32):
    rat,r=min((Fraction(a*b,c*c),r) for r in range(1,n) for a,b,c in [vals(n,r,2)])
    print(n,r,(1000*rat.numerator)//rat.denominator)
# Independently check evaluations from the original subset sum, grouping
# subsets by occupied classes and by their total cardinality.
for q in range(2,6):
    for n in range(2,9):
        for r in range(1,n):
            out=[]
            for x,y in [(2,0),(0,2),(1,1)]:
                p=[1]
                block=[0]+[comb(q,j) for j in range(1,q+1)]
                ans=(x-1)**r
                for k in range(1,n+1):
                    nxt=[0]*(len(p)+q)
                    for i,u in enumerate(p):
                        for j,v in enumerate(block):
                            nxt[i+j]+=u*v
                    p=nxt
                    rho=min(r,k)
                    ans+=comb(n,k)*sum(v*(x-1)**(r-rho)*(y-1)**(size-rho) for size,v in enumerate(p) if v)
                out.append(ans)
            assert tuple(out)==vals(n,r,q)
            # Check every coefficient of B expanded about s=1.
            coeff=[sum(((-1)**(r-j) if j<r else 1)*comb(n,j)*comb(j,k) for j in range(k,n+1)) for k in range(n+1)]
            assert all(v>=0 for v in coeff)
            assert coeff[r]==comb(n,r)*2**(n-r)
            assert vals(n,r,q)[1]>=comb(n,r)*2**(n-r)*(2**q-2)**r
            if q>=3:
                a,b,c=vals(n,r,q)
                assert a*b>=c*c
print('Independent finite evaluation and coefficient checks passed.')
