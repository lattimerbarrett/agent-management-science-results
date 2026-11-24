"""Exact parameter arithmetic and wedge gap for the theta/regular-subdivision pair."""
from fractions import Fraction as F
from math import comb

def pair(k):
 D=2*(k-1)**2
 v=D*(k-1)+2;e=D*k
 W=D*(D-1)+D*(k-1)
 # Regular core on 4k vertices of degree 2k-2, paths length k-1.
 core_v=4*k;core_e=core_v*(2*k-2)//2
 vp=core_v+core_e*(k-2);ep=core_e*(k-1)
 Wp=core_v*comb(2*k-2,2)+core_e*(k-2)
 assert vp==2*v and ep==2*e
 A=k*k-3*k+3
 assert F(e,v)==F((k-1)**2,A)
 gap=F(W,v)-F(Wp,vp)
 assert gap==F(2*(k-1)*(k-2)**2,A)
 return F(e,v),gap

for k in range(3,100):pair(k)
for r in range(3,30):
 for k in range(r+3,r+30):
  rho,gap=pair(k)
  assert gap>r-1
print('Exact arithmetic, equal density and wedge-gap formulas verified for all k=3..99.')
print('For r=3..29, every tested k>=r+3 has gap>r-1.')
for k in [3,5,11,21,51]:print('k=',k,'rho, wedge-density gap=',pair(k))
