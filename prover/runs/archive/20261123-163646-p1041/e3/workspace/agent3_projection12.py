"""Exact projection bound reducing EVERY target word to a KTA-range12-var word.
No classification or exclusion is claimed by this file.

Additional m=14 max-pair<=7 branch (proved combinatorially):
Write p_a=number of unordered support pairs of difference a. If all p_a<=7,
for any2-plane K the total number of same-fiber pairs is sum(a inK minus zero)p_a<=21.
Parity projection therefore has weight>=w-42, because j mod2>=j-2*C(j,2).
If its support lay in a proper affine flatD of the12-dimensional quotient,
all support points outside pi^-1(D) occur in even fibers, whose total size
is <=w-wt(g)<=42. But nonzero RM(7,14) polynomial outside a proper affine
flat has weight>=64: choose a hyperplane containing thatflat but excluding
an outside1 point, and use minimumRM(7,13) weight64 onits complement.
Hence f is supported on pi^-1(D), a proper affine flat, impossible when
wt(f)==2 mod4: factoring its hyperplane indicator leaves RM(6,13), which
is doubly-even. Thus every such projection has FULLAFFINESPAN12.

Using only the KTA numerical exclusions below320, the chosenprojectionweights
are restricted to {288,296} forw322; {288,296,304} forw326;
{288,296,304,308} forw330; {296,304,308,312} forw334.
Further structural classification/lifting is still required.

Let S be a w-point set in F2^m,m>=14,w<=334. Choose uniformly a kernel K of
codimension12 and project support by parity onto F2^m/K. If a quotient fiber
contains j support points, its parity is at most j-2*C(j,2)+4*C(j,3).
Each pair coalesces with probability p2=(2^(m-12)-1)/(2^m-1), and each distinct
triple coalesces with p3=p2*(2^(m-12)-2)/(2^m-2).
Thus expected projected weight is at most E_m(w)=w-2*C(w,2)*p2+4*C(w,3)*p3.

This bound is decreasing with t=2^m for1<=w<=334. Put D=4096,
p=(t-D)/(D(t-1)), r=(t-2D)/(D(t-2)), q=p*r.
Then p'>0, r<=1/D, and
 p*r'/p'=2*(t-D)*(t-1)/(D*(t-2)^2)<=2/D.
The last inequality is (D-3)*t >=D-4. Hence q'/p'<=3/D.
Writing a=w(w-1), b=(2/3)w(w-1)(w-2), obtain
 E'/p' <= -a+3b/D = -a*(1-2*(w-2)/D)<0.
For w<=334 this is immediate. Therefore E_m(w)<=E_14(w).

If S supports f in RM(m-7,m), parity projection along K lies RM(5,12):
in coordinates adapted toK, summing over each kernel variable annihilates
monomials missing that variable, and removes it from the others. Every such
projected weight is divisible4: RM(5,12) is doubly-even since monomials have
weight divisible4 and any two monomials have even-weight intersection.
Consequently there exists a projection of weight at most
300,304,308,312 for original weights322,326,330,334 respectively.
All these are STRICTLY below the classical KTA threshold320.
"""
from fractions import Fraction
from math import comb

def expectation_bound(w,m):
 t=1<<m;s=1<<(m-12)
 p=Fraction(s-1,t-1)
 q=p*Fraction(s-2,t-2)
 return w-2*comb(w,2)*p+4*comb(w,3)*q

def verify():
 for j in range(335):
  assert (j&1)<=j-2*comb(j,2)+4*comb(j,3)
 expected={322:300,326:304,330:308,334:312}
 for w,bound in expected.items():
  e=expectation_bound(w,14)
  assert 4*(e.numerator//(4*e.denominator))==bound
  assert 2*(w-2)<4096
  for m in range(14,100):
   assert expectation_bound(w,m+1)<expectation_bound(w,m)
   assert expectation_bound(w,m)<bound+4
  print(w,'projection <=',bound,'; exact expectation upper bound',e,'=',float(e))
 # Check monotonicity algebra identity coefficient exactly.
 D=4096
 for t in [1<<m for m in range(14,100)]:
  assert (t-2)**2-(t-D)*(t-1)==(D-3)*t+4-D
  assert (D-3)*t+4-D>0
 print('All four universal12-dimensional projection bounds verified.')
if __name__=='__main__':verify()
