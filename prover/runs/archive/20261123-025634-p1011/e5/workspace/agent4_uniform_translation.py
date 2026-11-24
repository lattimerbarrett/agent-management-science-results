import sympy as S
from pathlib import Path
n,A,B,C,z=S.symbols('n A B C z',positive=True)
m=n-1
M1=(n-1)*(A+B)/2
G3=S.factor(M1-(n+1)*A)
G1=S.factor(4*M1/(n-1)**2)
trans=S.factor(B+2*G3/(m+4))
support=S.factor(6*B+(m+4)**2/(m+2)*G1+S.Rational(8)*(m+1)/((m+2)*(m+4))*G3)
assert S.factor(trans-(2*(n+1)*B/(n+3)-A))==0
assert S.factor(support-12*B+2*(n-9)/(n-1)*(A+4*B/(n+3)))==0
# At the first scale root z=A/(2B+sqrt(4B²-3AC)), hence 0<z<A/(2B).
# For n>9, A,B>0, trans<2B and support<12B.
assert S.factor(2*B-trans-A-4*B/(n+3))==0
assert S.factor(12*B-support-2*(n-9)*(A*(n+3)+4*B)/((n-1)*(n+3)))==0
print('Verified all uniform degree1 translation-Hessian identities exactly.')
print('transverse coefficient:',trans)
print('supported coefficient:',support)
