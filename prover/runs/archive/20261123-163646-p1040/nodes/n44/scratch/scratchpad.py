from sage.all import QQ, NumberField, polygen
from sympy import symbols, Poly, binomial, resultant
x=polygen(QQ)
for c in [4,8,16]:
 d=c//4
 K=NumberField(x**(2*d)-2*x**d+2,'pi'); pi=K.gen(); P=K.ideal(pi)
 assert P.is_prime() and P.norm()==2
 assert (1-pi**d)**2 == -1
 h=K.hilbert_symbol(1+pi,1+pi**(c-1),P)
 assert h == -1
 print('c=',c,'quadratic critical Hilbert symbol=',h)
z=symbols('z')
for p in [3,5,7,11,13,17,19]:
 f=sum(binomial(p,j)*z**(j-1) for j in range(1,p+1))
 N=int(resultant(f,1+z**(p-1),z))
 assert N%p==1 and N%(p*p)!=1
 print('p=',p,'critical norm mod p^2=',N%(p*p))
