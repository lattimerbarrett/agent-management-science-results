from itertools import combinations
from math import factorial, comb

def trim(p):
    p = list(p)
    while len(p)>1 and p[-1]==0: p.pop()
    return p

def add(p,q,sgn=1):
    r=[0]*max(len(p),len(q))
    for i,x in enumerate(p): r[i]+=x
    for i,x in enumerate(q): r[i]+=sgn*x
    return trim(r)

def mul(p,q):
    r=[0]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): r[i+j]+=x*y
    return trim(r)

def divrem(p,h):
    assert h[-1]==1
    r=trim(p); q=[0]*max(1,len(r)-len(h)+1)
    while len(r)>=len(h) and r!=[0]:
        t=len(r)-len(h); c=r[-1]; q[t]=c
        for i,a in enumerate(h): r[t+i]-=c*a
        r=trim(r)
    assert add(mul(q,h),r)==trim(p)
    return trim(q),r

def rootpoly(S):
    p=[1]
    for r in S: p=mul(p,[r,1])
    return p

def dot(x,y): return sum(a*b for a,b in zip(x,y))
def bil(x,C,y): return sum(x[i]*C[i][j]*y[j] for i in range(len(x)) for j in range(len(y)))
def zeros(n): return [[0]*n for _ in range(n)]

def check(s, all_factors=True):
    assert s>=3
    m=2**(s-1); k=m//2; j=2*m-2
    H=factorial(2*k-1); T=2*H*H+2
    K=zeros(k); e=0
    for a in range(k):
        for b in range(a+1,k):
            K[a][b]=T**e; K[b][a]=-T**e; e+=1
    h=rootpoly(range(1,2*k-1))
    assert len(h)==2*k-1
    assert T-1>H*H
    # Check the finite factorization certificate used in the proof.
    checked=0
    if all_factors:
        U=set(range(1,2*k-1))
        for S in combinations(sorted(U),k-1):
            a=rootpoly(S); b=rootpoly(sorted(U-set(S)))
            assert mul(a,b)==h
            assert max(a+b)<=H and min(a+b)>0
            assert dot(a,b)>0
            wedge=[a[r]*b[t]-a[t]*b[r] for r in range(k) for t in range(r+1,k)]
            assert any(wedge) and max(map(abs,wedge))<=H*H
            val=sum(c*T**e for e,c in enumerate(wedge))
            assert val==bil(a,K,b) and val!=0
            checked+=1
    # Construct all symmetric bilinear forms explicitly over the integers.
    I=zeros(m)
    for a in range(m): I[a][a]=1
    C2=zeros(m)
    for a in range(k):
        for b in range(k):
            C2[a][k+b]=-K[a][b]
            C2[k+a][b]=K[a][b]
    C=[I,C2]
    rem=[divrem([0]*e+[1],h)[1] for e in range(2*k-1)]
    for r in range(2*k-2):
        R=zeros(m); J=zeros(m)
        for a in range(k):
            for b in range(k):
                v=rem[a+b][r] if r<len(rem[a+b]) else 0
                R[a][b]=v; R[k+a][k+b]=-v
                J[a][k+b]=v; J[k+a][b]=v
        C.extend([R,J])
    assert len(C)==j
    assert all(A[a][b]==A[b][a] for A in C for a in range(m) for b in range(m))
    # Independently evaluate the polynomial formula on every pair of basis
    # vectors. Bilinearity makes these checks universal, not sampling.
    for a in range(m):
        for b in range(m):
            x=[int(t==a) for t in range(m)]; y=[int(t==b) for t in range(m)]
            xr,xi=x[:k],x[k:]; yr,yi=y[:k],y[k:]
            pr=add(mul(xr,yr),mul(xi,yi),-1)
            pi=add(mul(xr,yi),mul(xi,yr))
            rr=divrem(pr,h)[1]; ri=divrem(pi,h)[1]
            expected=[dot(x,y),bil(xi,K,yr)-bil(xr,K,yi)]
            for r in range(2*k-2):
                expected.extend([rr[r] if r<len(rr) else 0,ri[r] if r<len(ri) else 0])
            assert expected==[A[a][b] for A in C]
    # Shift by the identity to obtain positive definite covariance blocks.
    A=[I]
    for Q in C[1:]:
        R=1+max(sum(abs(v) for v in row) for row in Q)
        P=[[Q[a][b]+(R if a==b else 0) for b in range(m)] for a in range(m)]
        assert all(P[a][a]>sum(abs(P[a][b]) for b in range(m) if b!=a) for a in range(m))
        assert all(P[a][b]-R*I[a][b]==Q[a][b] for a in range(m) for b in range(m))
        A.append(P)
    assert len(A)==j
    # The upper-bound Euler-class coefficient, computed exactly.
    r=2*m-1; a=3*m-2; b=3*m-1
    assert a+b==3*r and a-r==m-1
    assert comb(r,m-1)%2==1
    # Dimensions of the Gaussian construction and the exact answer.
    d0=(j-1)+m
    assert d0==3*m-3 and b-1==d0+1
    print(f's={s}: j={j}; factor certificates={checked}; forms={len(C)}; counterexample dimension={d0}; upper dimension={b-1}',flush=True)
    return C,A

if __name__=='__main__':
    for s in (3,4,5): check(s)
