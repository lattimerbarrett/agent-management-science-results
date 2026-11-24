from sage.all import ZZ, QQ, matrix, vector, gcd, PolynomialRing, factorial, prod
from itertools import combinations, product
from math import comb

def local(q,b):
    C=[[] for a in range(q+1)]
    for a in range(q+1):
        for J in combinations(range(q),a):
            for R in product(range(3),repeat=a):
                if all(R.count(r)<=b[r] for r in range(3)):
                    C[a].append(tuple(zip(J,R)))
    ids=[{f:i for i,f in enumerate(L)} for L in C]
    D={}
    for a in range(1,q+1):
        D[a]=matrix(ZZ,len(C[a-1]),len(C[a]))
        for j,f in enumerate(C[a]):
            for i in range(a):
                D[a][ids[a-1][f[:i]+f[i+1:]],j]=(-1)**i
    ranks=[0]
    for a in range(1,q+1):
        S=D[a].smith_form(transformation=False)
        nz=[abs(S[i,i]) for i in range(min(S.dimensions())) if S[i,i]]
        assert all(x==1 for x in nz)
        ranks.append(len(nz))
        if a>=2: assert D[a-1]*D[a]==0
    H=tuple(len(C[a])-ranks[a]-(ranks[a+1] if a<q else 0) for a in range(q+1))
    return C,D,H,ranks[1:]

expected=[(4,(2,2,2),(0,0,0,1,2)),(3,(1,2,2),(0,0,0,2)),
          (2,(0,2,2),(0,0,1)),(2,(1,1,2),(0,0,2)),
          (1,(0,1,2),(0,1)),(1,(1,1,1),(0,2))]
for q,b,H in expected:
    C,D,h,r=local(q,b)
    assert h==H
    print(q,b,'ranks',r,'homology ranks',h)

C,D,_,_=local(4,(2,2,2))
cyclic={(0,1),(1,2),(2,0)}
def cweight(R):
    cnt=[R.count(r) for r in range(3)]
    return 0 if 2 not in cnt else (1 if (cnt.index(2),cnt.index(1)) in cyclic else -1)
phi=vector(ZZ,[(-1)**next(j for j in range(4) if j not in [u for u,r in f])*cweight([r for u,r in f]) for f in C[3]])
assert phi*D[4]==0
K=D[3].right_kernel_matrix()
assert gcd(list(phi*K.transpose()))==6
print('primitive local functional: gcd = 6')

# Each identity coefficient in the uniform pair-decomposition is checked.
for R in product(range(3),repeat=3):
    if R.count(0)>1 or any(R.count(r)>2 for r in (1,2)):continue
    rhs=0
    for i,j in combinations(range(3),2):
        rs=sorted((R[i],R[j]))
        rhs+=int(rs==[1,1])-int(rs==[2,2])+int(rs==[0,2])-int(rs==[0,1])
    assert cweight(list(R))==rhs

# Explicit universal relation cycles, expanded as squarefree polynomials.
from collections import defaultdict
def mul(A,B):
    out=defaultdict(int)
    for a,u in A.items():
        for b,v in B.items():
            if len({j for j,r in a+b})==len(a+b):out[tuple(sorted(a+b))]+=u*v
    return {a:u for a,u in out.items() if u}
def diff(r,s,j):return {((j,r),):1,((j,s),):-1}
def derivative(z):
    out=defaultdict(int)
    for A,c in z.items():
        for k,(j,r) in enumerate(A):out[j,A[:k]+A[k+1:]]+=c
    return {a:u for a,u in out.items() if u}
def times_x(w,n):
    return {(j,A):c for A,c in w.items() for j in range(n) if j not in [i for i,r in A]}
for n in range(6,11):
    h={((j,2),):1 for j in range(n)}
    E={((i,2),(j,2)):1 for i,j in combinations(range(n),2)}
    u=diff(0,1,0);v=diff(1,2,1)
    for z,w,mark,scale in [(mul(u,E),mul(u,h),{0},2),(mul(mul(u,v),h),mul(u,v),{0,1},-3)]:
        assert all(sum(r==0 for j,r in A)<=1 and all(sum(r==s for j,r in A)<=2 for s in (1,2)) for A in z)
        assert derivative(z)==times_x(w,n)
        f=defaultdict(int)
        for A,c in z.items():f[tuple(j for j,r in A)]+=c*cweight([r for j,r in A])
        for T in combinations(range(n),3):assert f[T]==scale*int(mark<=set(T))
        for S in combinations(range(n),4):
            val=sum(f[T] for T in combinations(S,3))
            assert val==(6 if len(mark)==1 else -6)*int(mark<=set(S))
print('explicit auxiliary cycles and connecting coefficients checked')

# Independent finite checks of the simultaneous incidence diagonalization.
for n in range(6,10):
    F=list(combinations(range(n),4))
    ballot=[A for j in range(min(4,n-4)+1) for A in combinations(range(1,n+1),j) if all(a>=2*(i+1) for i,a in enumerate(A))]
    U=matrix(ZZ,[[int(set(a-1 for a in A)<=set(S)) for S in F] for A in ballot])
    assert abs(U.det())==1
    rows=[A for j in (1,2) for A in combinations(range(n),j)]
    N=matrix(ZZ,[[int(set(A)<=set(S)) for A in rows] for S in F])
    T=N.smith_form(transformation=False)
    nz=[abs(T[i,i]) for i in range(min(T.dimensions())) if T[i,i]]
    assert nz.count(1)==comb(n,2)-1 and nz.count(2)==1 and len(nz)==comb(n,2)
print('incidence lattices checked n=6,7,8,9')

P=PolynomialRing(QQ,'m');m=P.gen()
def binpol(z,k):return prod(z-i for i in range(k))/factorial(k)
a=m*(m-1)*(m-2)*(m-7)/24
r=[binpol(m,k)*[1,3,9,24,54][k]*binpol(m-k-1,4-k) for k in range(5)]
b=a+sum((-1)**k*r[k] for k in range(5))
assert b==(m**4+2*m**3+11*m**2+10*m+12)/12
print('Euler polynomial:',b)
from pathlib import Path
Path('workspace/agent1_certificate.py').write_text(Path(__file__).read_text())
