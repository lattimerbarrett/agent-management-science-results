import sympy as S
import numpy as np
import mpmath as m
p=S.symbols('p', positive=True); q=p/(p-1)
assert S.simplify(1/p+1/q+q/p**2-(1+1/(p-1)-1/p))==0
e=S.symbols('e', positive=True)
a=(p-1)*(1-e)
assert S.simplify(p*(-1+e)+a-(-1+e))==0
r=S.symbols('r'); z=S.symbols('z')
assert S.simplify(1+(z-1)*r/(1-z*r)-(1-r)/(1-z*r))==0
rng=np.random.default_rng(412)
for k in range(350):
 def pd():
  Z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
  return Z.conj().T@Z+np.eye(2)
 U,V,A,B=pd(),pd(),pd(),pd()
 op=lambda T:np.linalg.norm(T,2)
 v=rng.normal(size=2)+1j*rng.normal(size=2)
 assert op(U@np.linalg.inv(V))+1e-10>=np.linalg.norm(U@v)/np.linalg.norm(V@v)
 assert np.isclose(op(A@B),op(B@A))
 assert np.isclose(op(np.linalg.inv(A)@U),op(U@np.linalg.inv(A)))
 assert op(A@np.linalg.inv(U))<=op(A@B)*op(np.linalg.inv(B)@np.linalg.inv(U))+1e-9
 f=rng.normal(size=2)+1j*rng.normal(size=2)
 g=rng.normal(size=2)+1j*rng.normal(size=2)
 assert np.allclose(np.vdot(np.linalg.inv(V)@f,U@g),np.vdot(A@np.linalg.inv(V)@f,np.linalg.inv(A)@U@g))
for theta in np.linspace(1e-8,1,10001):
 d=theta/16; rho=1-theta
 assert 4**d<=1+theta/4+1e-14
 assert 1-4**d*rho>=3*theta/4-1e-14
 assert (4/3)*2**d<2
m.mp.dps=60
for pp in [m.mpf('1.1'),m.mpf('1.5'),m.mpf('2.1'),m.mpf(3),m.mpf(7)]:
 for ee in [m.mpf(1)/4,m.mpf(1)/8,m.mpf(1)/16]:
  delta=m.exp(-4/ee)
  for j in range(11):
   t=m.exp(-(1+m.mpf(j)/10)/ee)
   assert m.log((t+m.mpf('.5'))/(t+delta))>=1/(2*ee)
  alpha=(pp-1)*(1-ee)
  for aa,bb in [(0,1),(.2,1),(-1,1),(-.2,1),(-3,-1)]:
   aa,bb=m.mpf(aa),m.mpf(bb)
   def integ_power(c):
    if aa<0<bb:return ((-aa)**(c+1)+bb**(c+1))/(c+1)
    lo,hi=sorted([abs(aa),abs(bb)])
    return (hi**(c+1)-lo**(c+1))/(c+1)
   L=bb-aa
   ap=integ_power(alpha)/L*(integ_power(-alpha/(pp-1))/L)**(pp-1)
   assert ap<=(2/ee)**(pp-1)*(1+m.mpf('1e-50'))
print('Passed: 3 exact identities; 1750 matrix checks; 30003 RH checks; 240 power-weight/kernel checks.')
