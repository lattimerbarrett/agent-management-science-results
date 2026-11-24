import numpy as np
import sympy as sp
from functools import lru_cache

p=sp.symbols('p',positive=True);q=p/(p-1)
F=1+1/(p*(p-1));v=1/(p-1)
assert sp.simplify((1+1/(q*(q-1)))/(p-1)-F)==0
assert sp.simplify(v/q-1/p)==0
assert sp.simplify((v/p)*q+v*(1-v)-v)==0
assert sp.simplify(v/p+(1-v)/p-1/p)==0
print('All symbolic exponent/duality identities passed.')

def params(p,Q):
 v=1/(p-1);return Q**-1,Q**-v,2-Q**-1,2-Q**-v,Q**(v/p)

def leaves(p,Q,L):
 t,s,r,z,k=params(p,Q);out=[]
 def rec(lo,hi,a,c,h,d,top):
  if d==0:
   out.append((lo,hi,a,c,h,top));return
  step=(hi-lo)/4
  for j in range(4):
   good=j in (1,2);sig=1 if j<2 else -1
   aa=a*(r if good else t);cc=c*(z if good else s);hh=h+sig*k/c
   ll=lo+j*step;rr=ll+step;tt=j if top<0 else top
   if good:rec(ll,rr,aa,cc,hh,d-1,tt)
   else:out.append((ll,rr,aa,cc,hh,tt))
 rec(0.,1.,1.,1.,0.,L,-1)
 return np.array(out)

def phi(x):
 y=np.zeros_like(x);m=x!=0;y[m]=x[m]*np.log(np.abs(x[m]));return y

def calculations(p,Q,L):
 t,s,r,z,k=params(p,Q);q=p/(p-1)
 D=leaves(p,Q,L);lo,hi,a,c,h,top=D.T;ell=hi-lo;mu=ell*a
 assert abs(np.sum(ell*a)-1)<2e-12
 assert abs(np.sum(ell*c)-1)<2e-12
 assert max(abs(h))<=3*k+1e-12
 def geom(x):return sum(x**j for j in range(L))
 ratios=[r**(1-q)/2,r/(2*z**p),z**q/(2*r**(q-1))]
 closed=[t**(1-q)/2*geom(ratios[0])+ratios[0]**L,
         t*s**(-p)/2*geom(ratios[1])+ratios[1]**L,
         t/2*(s/t)**q*geom(ratios[2])+ratios[2]**L]
 actual=[np.sum(mu*a**(-q)),np.sum(mu*c**(-p)),np.sum(mu*(c/a)**q)]
 assert np.allclose(actual,closed,rtol=3e-11,atol=3e-11)
 K=(phi(hi[:,None]-lo[None,:])-phi(lo[:,None]-lo[None,:])
    -phi(hi[:,None]-hi[None,:])+phi(lo[:,None]-hi[None,:]))/np.pi
 # Exact double integral of 1/(pi*(x-y)) between distinct terminal cells.
 np.fill_diagonal(K,0.)
 term=a[:,None]*c[None,:]*(h[:,None]-h[None,:])*K
 B=np.sum(term);C=np.sum(term*(top[:,None]!=top[None,:]))
 # Compute the ORIGINAL mixed operator-norm root characteristic, not a substitute.
 A=a**(1/p);DD=A/c
 xx=A[:,None]/A[None,:];yy=DD[:,None]/DD[None,:]
 bb=A[:,None]/DD[None,:]*(h[:,None]-h[None,:])
 fro=xx*xx+yy*yy+bb*bb;det=xx*yy
 norm=np.sqrt((fro+np.sqrt(np.maximum(0,fro*fro-4*det*det)))/2)
 characteristic=np.sum(ell*((norm**q)@ell)**(p-1))
 return B,C,characteristic

for pp in [2.,2.2,3.,5.]:
 for Q in [max(20.,2.**(pp-1)),100.]:
  prev=0.;t,s,r,z,k=params(pp,Q)
  for L in range(1,8):
   B,C,A=calculations(pp,Q,L)
   assert abs(B-C-r/2*prev)<2e-9*max(1,abs(B))
   prev=B
  print(f'p={pp:g}, Q={Q:g}: exact-cell B_7={B:.9g}, cross/k={C/k:.9g}, original root Ap={A:.9g}')

for m in [2,4,6,8]:
 x=np.array([.5]);H=np.array([0.])
 for j in range(m):
  x=np.concatenate([.25+x/4,.5+x/4]);H=np.concatenate([1+H/2,-1+H/2])
 mask=((x[:,None]<.5)&(x[None,:]>.5))|((x[:,None]>.5)&(x[None,:]<.5))
 den=x[:,None]-x[None,:];den=np.where(mask,den,1.)
 C=np.mean(np.where(mask,(H[:,None]-H[None,:])/den,0.))/np.pi
 assert C<=-2/np.pi+1e-12
 print(f'Cantor cross approximation m={m}: {C:.12f}')
print('All geometric-series, exact Hilbert-cell recurrence and strict cross-sign checks passed.')
open('workspace/agent1_complete_lower_checks.py','w').write(open('scratchpad.py').read())
