"""Exact symbolic/rational certificate for r=2 rival-cycle inequality, all m>=100.
See agent4_r2_proof.md for combinatorial derivation and factorial tail bound.
"""
import sympy as s, math, os, shutil
m,t,q=s.symbols('m t q', integer=True,positive=True)
ff=s.functions.combinatorial.factorials.FallingFactorial
cs=[0]*5
weight_sum=0
for u in range(4):
 for v in range(3):
  w=(math.comb(3,u) if v==0 else 0)-(math.comb(2,u)*math.comb(2,v) if u<=2 else 0)
  if not w or u+v==0:continue
  weight_sum+=abs(w)*2**(u+v-1)
  j0=max(u-1,v,0);delta=abs(1-u+v)
  pol=s.expand(s.cancel(ff(q,u)*ff(q,v)/q)).subs(q,m-j0-t).expand()
  a=1-2*u;b=-2*v
  fac=(m+1 if a==1 else 1/ff(m,-a))*(1/ff(m,-b))
  deg=s.degree(pol,t)
  reconstructed=0
  for ell in range(deg+1):
   dif=sum((-1)**(ell-i)*math.comb(ell,i)*pol.subs(t,i) for i in range(ell+1))/math.factorial(ell)
   reconstructed+=dif*ff(t,ell)
   cs[delta+ell]+=w*2**(u+v-1)*fac*dif
  assert s.expand(reconstructed-pol)==0
assert weight_sum<1000
cs=[s.factor(c) for c in cs]
for i,c in enumerate(cs):print('I'+str(i),'coefficient',c)
lo=[sum(s.Rational(1,math.factorial(k)*math.factorial(k+j)) for k in range(20)) for j in range(5)]
hi=[lo[j]+s.Rational(1,math.factorial(20)*math.factorial(20+j))/(1-s.Rational(1,21*(21+j))) for j in range(5)]
M=100;x=s.symbols('x',nonnegative=True)
for i,c in enumerate(cs):
 num,den=s.fraction(c)
 coeff=s.Poly(s.expand(num.subs(m,x+M)),x).all_coeffs()
 assert all(a>=0 for a in coeff) if i in [0,4] else all(a<=0 for a in coeff)
 assert all(a>=0 for a in s.Poly(s.expand(den.subs(m,x+M)),x).all_coeffs())
low=s.factor(sum(c*(lo[i] if i in [0,4] else hi[i]) for i,c in enumerate(cs))-s.Rational(4,5)/m)
num,den=s.fraction(low)
assert all(a>=0 for a in s.Poly(s.expand(num.subs(m,x+M)),x).all_coeffs())
assert all(a>=0 for a in s.Poly(s.expand(den.subs(m,x+M)),x).all_coeffs())
print('Infinite Bessel extension difference/m!^2 >=4/(5m) for ALL m>=100.')
# Tail <=2000(m+3)^3/(m-4)!^2 <1/(100m).
assert 200000*100*103**3<math.factorial(96)**2
# The scaled bound decreases: ratio at m>=100 is at most16/(m-3)^2<1.
assert s.Rational(16,97**2)<1
print('Factorial extension error <1/(100m) for ALL m>=100; exact cycle difference positive.')
# Independently check the finite contraction formula against join-polynomial counts.
import sys
sys.path.insert(0,'workspace')
from agent1_cycles import cycles_join_r2,mul,power
for mm in [8,10,20,50]:
 total=0
 for u in range(4):
  for v in range(3):
   w=(math.comb(3,u) if v==0 else 0)-(math.comb(2,u)*math.comb(2,v) if u<=2 else 0)
   if not w or u+v==0:continue
   for qq in range(max(u,v,1),min(mm+1-u,mm-v)+1):
    total+=w*2**(u+v-1)*math.comb(mm+1-2*u,qq-u)*math.comb(mm-2*v,qq-v)*math.factorial(qq)*math.factorial(qq-1)
 def qm(n,a):return mul(power([1,4,1],a),power([1,1],n-2*a))
 exact=cycles_join_r2(qm(mm+1,3),qm(mm,0),mm+1,mm)-cycles_join_r2(qm(mm+1,2),qm(mm,2),mm+1,mm)
 assert total==exact
print('Four independent finite contraction/join-polynomial checks passed.')
for mm in range(13,100):
 def qm(n,a):return mul(power([1,4,1],a),power([1,1],n-2*a))
 assert cycles_join_r2(qm(mm+1,3),qm(mm,0),mm+1,mm)>cycles_join_r2(qm(mm+1,2),qm(mm,2),mm+1,mm)
print('All remaining 87 cases m=13..99 checked; conclusion holds for every odd n>=27.')

