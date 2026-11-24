from math import gcd
from heapq import heappush, heappop
from itertools import combinations
from fractions import Fraction
from functools import lru_cache

def ceildiv(a,b):
    return -((-a)//b)

def answer(m,n):
    assert m>0 and n>0 and gcd(m,n)==1
    d=m*m+n*(2*m+1)
    M=m+n-1
    c1=n*(2*m+1)*M-d+1
    c2=(m-1)*(d-m-1)
    sig=ceildiv(c1+c2,d)
    delta=ceildiv((n-2)*m*m-(3*m+2)*n+2,d)
    assert sig-M==delta
    return delta,sig,M,c1,c2

def reduce_pair(m,n,u,v):
    # b_(u,v) = x0^p x4^q b_(U,V), with b of degree max(u,v).
    p=q=0
    while True:
        old=max(u,v)
        if u-v>m:
            u,v=u-m-1,v+m
            p+=old-max(u,v)
        elif v-u>m:
            u,v=u+m+1,v-m
            p+=old-max(u,v)
        elif old>=m+n:
            if u>=v:
                u,v=u-m-n,v-n
            else:
                u,v=u-n+1,v-m-n
            q+=n
            p+=old-max(u,v)-n
        else:
            return u,v,p,q
        assert min(u,v,p,q)>=0

def apery(gens,d):
    # Independent shortest-path computation of the Apéry set modulo d.
    dist=[None]*d
    dist[0]=0
    heap=[(0,0)]
    while heap:
        x,r=heappop(heap)
        if dist[r]!=x: continue
        for a in gens:
            y=x+a; s=y%d
            if dist[s] is None or y<dist[s]:
                dist[s]=y
                heappush(heap,(y,s))
    assert all(x is not None for x in dist)
    return dist

def qrank(A):
    if not A or not A[0]: return 0
    A=[[Fraction(x) for x in row] for row in A]
    r=0
    for c in range(len(A[0])):
        pivot=next((i for i in range(r,len(A)) if A[i][c]),None)
        if pivot is None: continue
        A[r],A[pivot]=A[pivot],A[r]
        z=A[r][c]
        A[r]=[x/z for x in A[r]]
        for i in range(r+1,len(A)):
            z=A[i][c]
            if z: A[i]=[x-z*y for x,y in zip(A[i],A[r])]
        r+=1
        if r==len(A): break
    return r

@lru_cache(None)
def koszul_homology(code):
    # code records which of the 32 subsets of five generators occur.
    V=[[s for s in range(32) if (code>>s)&1 and s.bit_count()==i]
       for i in range(6)]
    ranks=[0]*7
    for i in range(1,6):
        rows={s:j for j,s in enumerate(V[i-1])}
        mat=[[0]*len(V[i]) for _ in V[i-1]]
        for j,s in enumerate(V[i]):
            for k,b in enumerate(b for b in range(5) if (s>>b)&1):
                face=s^(1<<b)
                assert face in rows
                mat[rows[face]][j]=(-1)**k
        ranks[i]=qrank(mat)
    hom=tuple(len(V[i])-ranks[i]-ranks[i+1] for i in range(6))
    assert min(hom)>=0
    return hom

def direct_betti(A,sumsets,J):
    subset_size=[s.bit_count() for s in range(32)]
    subset_sum=[sum(A[i] for i in range(5) if (s>>i)&1) for s in range(32)]
    betti={}
    for j in range(J+1):
        for x in sumsets[j]:
            code=0
            for s in range(32):
                i=subset_size[s]
                if i<=j and x-subset_sum[s] in sumsets[j-i]:
                    code|=1<<s
            for i,b in enumerate(koszul_homology(code)):
                if b: betti[i,j]=betti.get((i,j),0)+b
    return betti

def check(m,n,with_betti=False):
    delta,sigma,M,c1,c2=answer(m,n)
    d=m*m+n*(2*m+1)
    A=[0,n*m,n*(m+1),n*(2*m+1),d]
    D=[(u,v) for u in range(M+1) for v in range(M+1) if abs(u-v)<=m]
    assert len(D)==d
    ab={}
    for u,v in D:
        alpha=n*(m*u+(m+1)*v)
        beta=max(u,v)*d-alpha
        assert alpha%d not in ab
        ab[alpha%d]=(alpha,beta,max(u,v))
    assert len(ab)==d and max(e for a,b,e in ab.values())==M
    for u in range(2*(m+n)+2):
        for v in range(2*(m+n)+2):
            U,V,p,q=reduce_pair(m,n,u,v)
            assert (U,V) in D
            assert max(u,v)==p+q+max(U,V)
            assert n*(m*u+(m+1)*v)==q*d+n*(m*U+(m+1)*V)
    ap1=apery(A,d)
    ap2=apery([d-a for a in A],d)
    for r,(alpha,beta,e) in ab.items():
        assert ap1[r]==alpha
        assert ap2[(-r)%d]==beta
    assert max(ap1)-d+1==c1
    assert max(ap2)-d+1==c2
    assert (sigma==0 or (sigma-1)*d<c1+c2) and sigma*d>=c1+c2
    J=max(sigma+1,M+5 if with_betti else M+2)
    S=[{0}]
    for h in range(1,J+1):
        S.append({x+a for x in S[-1] for a in A})
    for h in range(J+1):
        saturated={x for x in range(h*d+1)
                   if x>=ap1[x%d] and h*d-x>=ap2[(h*d-x)%d]}
        assert S[h]==saturated
        assert len(S[h])==sum(h-e+1 for a,b,e in ab.values() if e<=h)
    if with_betti:
        B=direct_betti(A,S,M+5)
        assert max(j-i for i,j in B)==M
        # Euler characteristic of the graded free resolution.
        for h in range(M+6):
            from math import comb
            predicted=sum((-1)**i*b*comb(h-j+4,4)
                          for (i,j),b in B.items() if j<=h)
            assert predicted==len(S[h])
        return B

if __name__=='__main__':
    count=0
    for m in range(1,11):
        for n in range(1,11):
            if gcd(m,n)==1:
                check(m,n)
                count+=1
    print('Direct Apéry, reduction, sumset and Hilbert-function checks:',count,'pairs')
    pairs=[(1,1),(1,3),(2,1),(2,3),(3,2),(3,4),(4,3),(5,2),(5,7),(8,11)]
    for m,n in pairs:
        B=check(m,n,True)
        print((m,n),'(delta,sigma,reg,c1,c2) =',answer(m,n),
              'Betti =',sorted(B.items()))
    print('All checks passed; distinct Koszul complexes:',koszul_homology.cache_info().currsize)
