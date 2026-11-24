import sympy as s
from pathlib import Path
e=s.symbols('e', nonnegative=True, integer=True)
def dot(D,F):
 a,b=D;c,d=F
 return s.expand(-e*a*c+a*d+b*c)
A=(5,-1); B=(-1,12*e+5); H=(1,3*e+1); P=(4,12*e+3); C=(4,12*e+4); K=(-2,-e-2)
c2=dot(A,B); c12=dot(C,C)
assert s.expand(c2-(65*e+26))==0
assert s.expand(c12-(80*e+32))==0
assert dot(A,H)==dot(B,H)==10*e+4
assert dot(A,P)==40*e+11
assert dot(B,P)==40*e+17
assert s.expand(4*c2-c12)==180*e+72
assert s.expand(c12-c2)==15*e+6
assert s.expand(c2-c12/4)==45*e+18
print('c1² =',c12,'; c2 =',c2,'; discriminant =',s.expand(4*c2-c12))
print('tautological volume =',s.expand(c12-c2))
print('slopes:',dot(A,P),dot(B,P),dot(C,P)/2)
print('Euler E =',s.expand(2+(c12-dot(C,K))/2-c2))
print('sectional genus tautological =',s.expand(1+dot((C[0]+K[0],C[1]+K[1]),C)/2))
