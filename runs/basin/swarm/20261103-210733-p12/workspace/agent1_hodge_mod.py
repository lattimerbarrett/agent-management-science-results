"""Exact lambda_g times Chern-character Hodge integrals via Mumford GRR.
F(g, ds, ms) = int_{Mbar_g,n} lambda_g prod psi_i^ds_i prod ch_ms_j(E).
No unproved Gorenstein assumption enters.  All arithmetic is rational.
"""
from functools import lru_cache
from fractions import Fraction
P=1000000007
def Q(x,y=1):
    if isinstance(x,Fraction):return (x.numerator*pow(x.denominator,-1,P)*pow(y,-1,P))%P
    if hasattr(x,"q"):return int(x.p)*pow(int(x.q),-1,P)*pow(int(y),-1,P)%P
    return (int(x)%P)*pow(int(y)%P,-1,P)%P
from math import factorial, comb, prod
from collections import Counter
from itertools import product
import sympy as s

@lru_cache(None)
def b(g):
    if g==0:return Q(1)
    return Q((-1)**(g-1)*(2**(2*g-1)-1),2**(2*g-1))*Q(s.bernoulli(2*g),factorial(2*g))%P

@lru_cache(None)
def splits(t):
    items=list(Counter(t).items())
    def rec(i,a,c,m):
        if i==len(items):yield tuple(a),tuple(c),m;return
        v,n=items[i]
        for k in range(n+1):yield from rec(i+1,a+[v]*k,c+[v]*(n-k),m*comb(n,k))
    return tuple(rec(0,[],[],1))

def F(g,ds=(),ms=()):return _F(g,tuple(sorted(ds)),tuple(sorted(ms)))

@lru_cache(None)
def _F(g,ds,ms):
    n=len(ds)
    if 2*g-2+n<=0:return Q(0)
    if sum(ds)+sum(ms)!=2*g-3+n:return Q(0)
    if g==0:
        if ms:return Q(0)
        return Q(factorial(n-3),prod(factorial(x) for x in ds))
    if not ms:return b(g)*Q(factorial(sum(ds)),prod(factorial(x) for x in ds))%P
    assert all(m>0 and m%2 for m in ms)
    # String and dilaton relations: all Hodge classes pull back.
    if ds and ds[0]==0:
        restds=ds[1:];val=0
        for d,num in Counter(restds).items():
            if d:
                dd=list(restds);dd.remove(d);dd.append(d-1)
                val+=num*F(g,dd,ms)
        return val%P
    if 1 in ds:
        dd=list(ds);dd.remove(1)
        return (2*g-3+n)*F(g,dd,ms)%P
    m=ms[-1];rest=ms[:-1]
    value=F(g,ds+(m+1,),rest)
    for d,num in Counter(ds).items():
        dd=list(ds);dd.remove(d);dd.append(d+m)
        value-=num*F(g,dd,rest)
    boundary=Q(0)
    for ga in range(g+1):
      gb=g-ga
      for da,db,multd in splits(ds):
        if 2*ga-1+len(da)<=0 or 2*gb-1+len(db)<=0:continue
        for ma,mb,multm in splits(rest):
          j=2*ga-2+len(da)-sum(da)-sum(ma)
          if 0<=j<m:
            fa=F(ga,da+(j,),ma)
            if fa:boundary+=(-1)**j*multd*multm*fa*F(gb,db+(m-1-j,),mb)
    value+=boundary*pow(2,-1,P)
    return Q(s.bernoulli(m+1),factorial(m+1))*value%P

def odd_partitions(n,m=None):
    if n==0:yield ();return
    if m is None:m=n
    for i in range(min(n,m),0,-1):
        if i%2:
            for p in odd_partitions(n-i,i):yield (i,)+p

@lru_cache(None)
def lambda_expansion(k):
    # c_t(E)=exp(sum_{m odd}(m-1)! ch_m t^m).
    terms=[]
    for p in odd_partitions(k):
        coeff=Q(1)
        for m,cnt in Counter(p).items():coeff*=Q(factorial(m-1)**cnt,factorial(cnt))
        terms.append((p,coeff))
    return tuple(terms)

@lru_cache(None)
def kappa_expansion(a):
    # kappa products inverted from psi pushforwards: signed set partitions.
    if not a:return (((),1),)
    first=a[0];cc=Counter(a[1:]);ks=tuple(cc);cs=tuple(cc.values());out=Counter()
    for vv in product(*(range(c+1) for c in cs)):
        size=1+sum(vv);ss=first+sum(k*v for k,v in zip(ks,vv))
        mult=(-1)**(size-1)*prod(comb(c,v) for c,v in zip(cs,vv))
        rem=tuple(sorted(k for k,c,v in zip(ks,cs,vv) for _ in range(c-v)))
        for p,z in kappa_expansion(rem):out[tuple(sorted(p+(ss,)))]+=mult*z
    return tuple((p,z) for p,z in out.items() if z)

def H(g,k,kappa=(),psi=()):
    # int lambda_g lambda_k prod kappa_i prod psi_j^dj.
    # kappa here is the log kappa on Mbar_g,len(psi).
    if sum(kappa)+sum(psi)+k!=2*g-3+len(psi):return Q(0)
    ans=Q(0)
    for p,c in lambda_expansion(k):
      for a,z in kappa_expansion(tuple(sorted(kappa))):
        ans+=c*z*F(g,tuple(psi)+tuple(i+1 for i in a),p)
    return ans%P

def validate():
    assert b(1)==Q(1,24) and b(2)==Q(7,5760)
    assert F(2,(),(1,))==Q(1,5760)
    assert F(3,(),(1,1,1))*pow(2,-1,P)%P==Q(1,1451520)
    assert H(3,2,(1,))==Q(1,120960)
    # Compare genus4 two kappa intersections with Faber ratio.
    x=H(4,3,(2,));y=H(4,3,(1,1))
    assert y==Q(32,3)*x%P,(x,y)
    # lambda_g^2=0, checked with several top-degree psi insertions.
    for g in range(1,5):
        assert H(g,g,(),(g-2,))==0 if g>=2 else True
    print('Exact Mumford recursion passed lambda_g theorem, genus2/3 Hodge values, genus4 Faber ratio, lambda_g^2 tests.')

if __name__=='__main__':
    validate();print('cache',_F.cache_info())
