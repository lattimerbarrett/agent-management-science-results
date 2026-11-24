import mpmath as mp
import numpy as np
from numpy.polynomial import Polynomial as Poly
mp.mp.dps=90
lam0=[mp.mpf(i) for i in range(1,7)]
def W(x):return mp.fprod(x-i for i in lam0)
delta=mp.mpf(225)/128
rr=np.sort((Poly.fromroots(np.arange(1.,7.))+float(delta)).roots())
roots=[mp.findroot(lambda x:W(x)+delta,(mp.mpf(float(r))-.001,mp.mpf(float(r))+.001)) for r in rr]
proots=roots[::2]
def p(x):return mp.fprod((x-a)/(-a) for a in proots)
t=[1,1,2,2,1,1]
w=[mp.mpf(ti)/abs(p(x)) for ti,x in zip(t,lam0)];sw=sum(w);w=[a/sw for a in w]
lam=lam0+[mp.mpf('3.5')]
# centered coordinates avoid conditioning, but preserve monic polynomial map.
x=[(a-mp.mpf('3.5'))/5 for a in lam]
def step(v):
 prev=[mp.mpf(0)]*7;pol=[mp.mpf(1)]*7;b=mp.mpf(0)
 for j in range(3):
  nn=sum(wi*pi*pi for wi,pi in zip(v,pol))
  a=sum(wi*xi*pi*pi for wi,xi,pi in zip(v,x,pol))/nn
  new=[(xi-a)*pi-b*pr for xi,pi,pr in zip(x,pol,prev)]
  b=sum(wi*pi*pi for wi,pi in zip(v,new))/nn
  prev,pol=pol,new
 v=[wi*pi*pi for wi,pi in zip(v,pol)];total=sum(v)
 return [a/total for a in v]
def displacement(eps):
 v=[a*(1-eps) for a in w]+[eps]
 nxt=step(step(v))
 return [a-b for a,b in zip(nxt,v)]
eps=mp.mpf('1e-25');d1=displacement(eps);d2=displacement(eps/2)
A=[(4*b-a)/eps for a,b in zip(d1,d2)]
B=[2*(a-2*b)/eps**2 for a,b in zip(d1,d2)]
print('exact core orthogonality errors:',*[mp.nstr(sum(wi*p(xi)*xi**j for wi,xi in zip(w,lam0)),5) for j in range(3)])
print('linear coefficient A in F(v(e))-v(e)=e A+e^2 B+O(e^3):')
print([mp.nstr(a,16) for a in A])
print('quadratic coefficient B:')
print([mp.nstr(a,16) for a in B])
print('transverse update: e_next=e +',mp.nstr(B[-1],16),'*e^2+O(e^3)')
# Kernel formula for monic orthogonal polynomial perturbation.
print('pure transverse path expansion computed; iterative tangential motion cannot be inferred by freezing these coefficients.')
