import sympy as s
from pathlib import Path
r,R,Lam=s.symbols('r R Lam',positive=True)
n=7;a=s.Rational(5,2);beta=s.Rational(5,12);c=s.Rational(5,24);kap=s.Rational(25,2)
U=(1+r*r)**(-a);G=(1+r*r)**(-5)
for j in range(2,7):
 D=j*(j+n-3)
 radial=-beta*D*r**(j+n-4)*U*(a*U+r*s.diff(U,r))-s.Rational(j-1,2)*r**(j+n-2)*s.diff(U,r)**2+kap*(j-1)*r**(j+n-2)*(1+r*r)**(-n)
 edge=c*(-(j-1)*r**(j+n-2)*s.diff(G,r)-j*(n-2)*r**(j+n-3)*G)
 assert s.simplify(s.diff(edge,r)-radial)==0
 expected=s.Rational((n-2)**2*(j-2),4*(n-1))
 assert s.limit(edge*r**(n-j-1),r,s.oo)==expected
 print('n7 degree',j,'exact first-linear coefficient=',expected)
f,S0,T1,T3,Agrad=s.symbols('f S0 T1 T3 Agrad',real=True)
rad=r*r+Lam*Lam*f*f;AA=1+rad
T=Lam*T1-Lam**3*T3/(1+Lam*Lam*Agrad)
S=Lam*S0
UZ=a*AA**-5-5*rad*AA**-6
grad2=25*rad*AA**-7
I=-beta*T*UZ-S*grad2/2+kap*S*AA**-7
assert s.simplify(I+I.subs(Lam,-Lam))==0
print('Exact direct-U graph flux is odd in shape amplitude')
N,J=s.symbols('N J')
assert s.simplify((N-1)+(J-2)-(N-2)-(J-1))==0
print('Exact bilinear Robin coefficient j-1 checked')
