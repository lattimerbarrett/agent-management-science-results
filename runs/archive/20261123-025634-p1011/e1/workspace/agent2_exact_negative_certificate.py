from fractions import Fraction as Q
from math import factorial
from pathlib import Path
K=300
c=[Q(1),-Q(461,1000),Q(7,125),-Q(693,500000)]
d=[1,3,5,7]

def P(k):
 return [Q(1),Q(k*k+21*k+11,9),Q(k**4+42*k**3+467*k*k+546*k+264,144),Q(k**6+63*k**5+1372*k**4+11319*k**3+22855*k*k+26166*k+10296,3024)]
E=Q(0); O=Q(0)
ws=[Q(8400,factorial(10)**2), Q(40572*4**22*factorial(11)**2,factorial(22)**2)]
for k in range(K):
 p=P(k); q=sum(ci*pi for ci,pi in zip(c,p)); dq=sum(ci*di*pi for ci,di,pi in zip(c,d,p))
 term=2*ws[k%2]*q*dq
 if k%2:Eodd=None; O+=term
 else:E+=term
 ws[k%2]*=Q((2*k+25)*(k+3)**2,(2*k+21)*(k+20)**2)
# Exact alternating-series intervals and Machin's formula.
def atan_inv_bounds(q,N=80):
 S=sum((Q(1,(2*j+1)*q**(2*j+1)) if j%2==0 else -Q(1,(2*j+1)*q**(2*j+1))) for j in range(N))
 nextterm=Q(1,(2*N+1)*q**(2*N+1))
 return (S,S+nextterm) if N%2==0 else (S-nextterm,S)
aL,aU=atan_inv_bounds(5); bL,bU=atan_inv_bounds(239)
pL,pU=16*aL-4*bU,16*aU-4*bL
assert pU>pL>3

def interval_product_scalar(v,l,u):return (v*l,v*u) if v>=0 else (v*u,v*l)
EL,EU=interval_product_scalar(E,pL,pU)
OL,OU=interval_product_scalar(O,1/pU,1/pL)
SL,SU=EL+OL,EU+OU
# Tail: each P_j/k^(2j) is bounded by positive-coefficient polynomial at 1/K.
R=[Q(1),Q(1,9)*(1+Q(21,K)+Q(11,K*K)),Q(1,144)*(1+Q(42,K)+Q(467,K**2)+Q(546,K**3)+Q(264,K**4)),Q(1,3024)*(1+Q(63,K)+Q(1372,K**2)+Q(11319,K**3)+Q(22855,K**4)+Q(26166,K**5)+Q(10296,K**6))]
M=sum(abs(c[j])*R[j]/K**(6-2*j) for j in range(4))
N=sum(abs(c[j])*d[j]*R[j]/K**(6-2*j) for j in range(4))
# Gautschi: [Gamma(y)/Gamma(y+1/2)]^2 <= (y+1/2)/y^2.
# Split denominator Gamma(y+10.5) into Gamma(y+.5)*10 factors >=y.
# w(k) <= W*k^(-16).
W=(2+Q(21,K))*(1+Q(1,K))**2*(1+Q(20,K))**2*2**21*(1+Q(1,K+1))
T=2*W*M*N/(3*(K-1)**3)
assert SU+T<0
print('Exact rational certificate, K=',K)
print('finite sum interval:',float(SL),float(SU))
print('absolute infinite-tail bound:',float(T))
print('rigorous infinite-sum upper bound:',float(SU+T))
print('All sign decisions were exact Fraction comparisons, not floating tests.')
Path('workspace/agent2_exact_negative_certificate.py').write_text(Path(__file__).read_text())
