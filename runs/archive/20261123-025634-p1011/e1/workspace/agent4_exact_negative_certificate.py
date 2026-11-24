"""Exact rational certificate for a failed auxiliary weighted-Hessian lemma.
NOT a counterexample to the original compactness theorem.
"""
from fractions import Fraction as F
from math import factorial

def atan_bounds(q,terms):
    a=sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(terms)),F(0))
    nxt=F((-1)**terms,(2*terms+1)*q**(2*terms+1))
    return min(a,a+nxt),max(a,a+nxt)
a,b=atan_bounds(5,60);c,d=atan_bounds(239,20)
pi_lo,pi_hi=16*a-4*d,16*b-4*c
assert F(314159,100000)<pi_lo<pi_hi<F(314160,100000)

def polys(k):
    return [F(1),F(k*k+21*k+11,9),F(k**4+42*k**3+467*k*k+546*k+264,144),F(k**6+63*k**5+1372*k**4+11319*k**3+22855*k*k+26166*k+10296,3024)]
c=[F(1),F(-461,1000),F(7,125),F(-693,500000)]
D=[1,3,5,7]
K=200
weights=[F(8400,factorial(10)**2),F(23*4*441)*(F(4**11*factorial(11),factorial(22)))**2]
sums=[F(0),F(0)]
for k in range(K):
    parity=k%2
    ps=polys(k)
    v=sum((cc*p for cc,p in zip(c,ps)),F(0))
    dv=sum((dd*cc*p for dd,cc,p in zip(D,c,ps)),F(0))
    sums[parity]+=2*weights[parity]*v*dv
    weights[parity]*=F((2*k+25)*(k+3)**2,(2*k+21)*(k+20)**2)

def mul_interval(a,lo,hi):return (a*lo,a*hi) if a>=0 else(a*hi,a*lo)
e0,e1=mul_interval(sums[0],pi_lo,pi_hi)
o0,o1=mul_interval(sums[1],1/pi_hi,1/pi_lo)
finite_lo,finite_hi=e0+o0,e1+o1
# For k>=K, gamma log-convexity gives ratio² <=2^21/k^21.
# Thus w(k)<=Cw*k^(-16). Positive polynomial coefficients imply
# P_j(k)<=P_j(K)*(k/K)^6. Sum k^(-4) <=1/[3(K-1)^3].
ps=polys(K)
S=sum((abs(cc)*p for cc,p in zip(c,ps)),F(0))
T=sum((dd*abs(cc)*p for dd,cc,p in zip(D,c,ps)),F(0))
Cw=2**21*(2+F(21,K))*(1+F(1,K))**2*(1+F(20,K))**2
tail=2*S*T*Cw/F(K**12*3*(K-1)**3)
assert finite_hi+tail<0
print('Exact rational finite sum enclosure:',float(finite_lo),float(finite_hi))
print('Rigorous absolute tail bound:',float(tail))
print('Rigorous total upper bound:',float(finite_hi+tail))
print('CERTIFIED: this auxiliary weighted shape Hessian has a negative direction.')
