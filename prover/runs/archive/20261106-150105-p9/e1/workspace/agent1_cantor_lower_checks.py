"""Checks for monotone-Cantor sharp lower bound. No numerical test substitutes
for the tube estimate or Hilbert-transform argument in the accompanying proof.
"""
import math
import numpy as np
import sympy as s
from scipy.special import roots_jacobi, beta as beta_function
p=s.symbols('p',positive=True)
x,y=s.symbols('x y',real=True)
q=p/(p-1)
L=s.log(4)-x/p-y/q
d=s.log(2)/L
alpha=1-d+x/L
beta=1-d+y/L
assert s.simplify(alpha/p+beta/q-d)==0
assert s.simplify((1-d-alpha)*L+x)==0
assert s.simplify((1-d-beta)*L+y)==0
assert s.simplify((1+1/(p-1)-1/p)-(1+1/(p*(p-1))))==0
a,b=s.symbols('a b',positive=True)
assert s.simplify((1/(1-a)+1/(1-b)-1)/(1-a*b)-1/((1-a)*(1-b)))==0
print('5 symbolic parameter / Hardy identities verified')

# Exact finite Hardy factorization and long-block lower bound.
for aa,bb in [(.8,.9),(.95,.7),(.93,.97)]:
    N=80
    lo=np.fromfunction(lambda i,j:np.where(i>=j,aa**np.maximum(i-j,0),0),(N,N))
    up=np.fromfunction(lambda i,j:np.where(j>=i,bb**np.maximum(j-i,0),0),(N,N))
    mat=lo@up
    explicit=np.empty((N,N))
    for n in range(N):
      for m in range(N):
        explicit[n,m]=sum(aa**(n-k)*bb**(m-k) for k in range(min(n,m)+1))
    assert np.max(np.abs(mat-explicit))<1e-12
    pairing=np.sum(mat)/N
    pairing_formula=sum((1-aa**j)*(1-bb**j) for j in range(1,N+1))/(N*(1-aa)*(1-bb))
    assert abs(pairing-pairing_formula)<1e-10
    for n in [0,20,79]:
      rowsum=(1-aa**(n+1))/((1-aa)*(1-bb))
      tail=bb**(N-n)/(1-bb)*sum((aa*bb)**j for j in range(n+1))
      assert abs(np.sum(mat[n])-(rowsum-tail))<1e-10
print('finite Hardy factorizations and exact row sums verified')

# Actual commutator kernel quadrature, distinct from the geometric bound.
def gaps(r,n):
    out=[]
    for j in range(2**n):
      left=0.; tv=0.
      for k in range(n):
        bit=(j>>(n-1-k))&1
        left+=bit*(1-r)*r**k
        tv+=bit*2.**(-k-1)
      out.append((left+r**(n+1),left+(1-r)*r**n,tv+2.**(-n-1)))
    return out

def level_quadrature(r,n,exponent,Q=12):
    z,w=roots_jacobi(Q,-exponent,-exponent)
    w=w/w.sum()
    pts=[]; ts=[]; ws=[]
    for l,h,t in gaps(r,n):
      pts.extend((l+h)/2+(h-l)*z/2)
      ts.extend([t]*Q)
      ws.extend(w/(2**n))
    return np.array(pts),np.array(ts),np.array(ws)

pp=3.; qq=pp/(pp-1); rhoA=.96; rhoB=.92
r=.25*rhoA**(1/pp)*rhoB**(1/qq)
LL=math.log(1/r); dd=math.log(2)/LL
al=1-dd+math.log(rhoA)/LL
be=1-dd+math.log(rhoB)/LL
assert abs(al/pp+be/qq-dd)<1e-14
GA=(1-2*r)**(1-al)*beta_function(1-al,1-al)
GB=(1-2*r)**(1-be)*beta_function(1-be,1-be)
for n in range(6):
    assert abs(2**n*r**((1-al)*n)*GA-GA*rhoA**n)<1e-12
    assert abs(2**n*r**((1-be)*n)*GB-GB*rhoB**n)<1e-12
min_ratio=float('inf')
for n in range(2,6):
  xx,tt,ww=level_quadrature(r,n,al)
  for m in range(2,6):
    yy,uu,vv=level_quadrature(r,m,be)
    dx=xx[:,None]-yy[None,:]
    dt=tt[:,None]-uu[None,:]
    kernel=np.divide(dt,dx,out=np.zeros_like(dx),where=np.abs(dx)>1e-15)
    assert np.min(kernel)>-1e-11
    averaged=float(ww@kernel@vv)
    lower=sum((1/(4*r))**k for k in range(min(n,m)-1))/16
    assert averaged+1e-10>=lower
    min_ratio=min(min_ratio,averaged/lower)
print('16 actual Cantor commutator block quadratures exceed geometric lower; min ratio',min_ratio)

# Prefix-pair enumeration verifies disjointness and the factor 1/16.
for n,m in [(3,4),(5,5),(6,4)]:
    used=set()
    for k in range(min(n,m)-1):
      selected=[]
      for i in range(2**n):
        for j in range(2**m):
          wi=i>>(n-k) if k else 0
          wj=j>>(m-k) if k else 0
          if wi!=wj: continue
          ni=(i>>(n-k-2))&3
          mj=(j>>(m-k-2))&3
          if (ni,mj) in [(0,3),(3,0)]: selected.append((i,j))
      assert len(selected)==2**(n+m-k-3)
      assert not used.intersection(selected)
      used.update(selected)
print('prefix counts/disjointness verified for 3 finite tree pairs')

# Target-balanced families: no huge tree needs to be enumerated.
for pp,K in [(1.5,32.),(3.,1024.),(5.,1048576.)]:
    qq=pp/(pp-1)
    eA=1/K; eB=K**(-1/(pp-1))
    ra=1-eA; rb=1-eB
    rr=.25*ra**(1/pp)*rb**(1/qq)
    LL=math.log(1/rr); dd=math.log(2)/LL
    al=1-dd+math.log(ra)/LL; be=1-dd+math.log(rb)/LL
    assert 0<al<1-dd and 0<be<1-dd
    assert abs(al/pp+be/qq-dd)<1e-12
    aa=ra**(1/pp); bb=rb**(1/qq)
    characteristic_proxy=max(1/eA,eB**(-(pp-1)),K**-1/eA/eB**(pp-1))
    assert abs(characteristic_proxy/K-1)<1e-10
    norm_proxy=K**(-1/pp)/((1-aa)*(1-bb))
    exponent=1+1/(pp-1)-1/pp
    print('p,K,r,exponents, norm proxy / K^target:', pp,K,rr,(al,be),norm_proxy/K**exponent)
