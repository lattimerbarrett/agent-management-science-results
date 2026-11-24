import sympy as s
import numpy as np
from pathlib import Path
k=s.symbols('k');n=21;a=s.Rational(n+1,2);aa=s.Rational(n+2,2)
Ps=[]
for j in range(5):
 p=sum(s.binomial(j,h)*(-1)**(j-h)*s.rf(k+1,h)*s.rf(k+2*a-h+1,h)/(s.factorial(h)*s.rf(a-h,h)) for h in range(j+1))
 Ps.append(s.Poly(s.expand(p),k))
def telescoping(P):
 R=s.Poly((k+aa)*P.as_expr(),k); S=0
 for r in range(P.degree(),-1,-1):
  c=R.coeff_monomial(k**(r+1))/(2*(n-r-4))
  S+=c*k**r
  T=(k+n-1)**2*k**r-(k+3)**2*(k+2)**r
  R-=s.Poly(c*T,k)
 assert R.is_zero
 V0=s.gamma(s.Rational(3,2))**2/s.gamma(s.Rational(n+1,2))**2
 V1=s.gamma(2)**2/s.gamma(s.Rational(n+2,2))**2
 return s.expand((n-1)**2*S.subs(k,0)*V0+n**2*S.subs(k,1)*V1)
G=s.zeros(5)
for i in range(5):
 for j in range(i,5):
  G[i,j]=G[j,i]=telescoping(Ps[i]*Ps[j])
D=s.Matrix(5,5,lambda i,j:(2+2*i+2*j)*G[i,j])
v=s.Matrix([1,-s.Rational(3,5),s.Rational(1,10),-s.Rational(1,200),s.Rational(1,30000)])
val=s.simplify((v.T*D*v)[0]);print('rational negative v',list(v));print('exact D quadratic',val);print('numeric',val.evalf())
print('G normalized',np.array(G.evalf(),dtype=float)/float(G[0,0]))
Path('workspace/agent2_gram21_exact_sympy.txt').write_text(str({'G':G,'D':D,'v':v,'vDv':val}))
