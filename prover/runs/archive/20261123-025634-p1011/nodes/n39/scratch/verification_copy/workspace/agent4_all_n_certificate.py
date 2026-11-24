"""Exact certificate: the degree-three radial shape scale matrix is indefinite in every integer n>=19. This is NOT a nonlinear existence proof."""
import sympy as s, sys
sys.path.insert(0,'workspace')
from agent4_exact_sums import matrix
n,t,y=s.symbols('n t y')
def atan(q,N=60):
 a=sum((-1)**j*s.Rational(1,q)**(2*j+1)/s.Integer(2*j+1) for j in range(N))
 b=a+(-1)**N*s.Rational(1,q)**(2*N+1)/s.Integer(2*N+1)
 return min(a,b),max(a,b)
a,b=atan(5);c,d=atan(239);pl,pu=16*a-4*d,16*b-4*c
assert pl>3
# Machin formula follows tan(4 atan(1/5)-atan(1/239))=1 and the angle is in (0,pi/2).
def bounds(expr):
 lo=hi=s.Integer(0)
 for (p,),c in s.Poly(s.expand(expr),s.pi).terms():
  if c>=0:lo+=c*pl**p;hi+=c*pu**p
  else:lo+=c*pu**p;hi+=c*pl**p
 return lo,hi
for N in range(19,40):
 Q=matrix(N);M=s.Matrix(4,4,lambda i,j:(i+j+1)*Q[i,j])
 found=False
 for size in (2,3,4):
  numerator,denominator=s.fraction(s.factor(M[:size,:size].det()))
  dl,du=bounds(denominator);assert dl>0
  lo,hi=bounds(numerator)
  if hi<0:
   print('CERTIFIED indefinite',N,'negative principal minor of size',size)
   found=True;break
 assert found
# All n>=40. gamma Cauchy Schwarz gives 0<t<2/(pi*n)<2/(3*n).
P=s.sympify(open('workspace/agent4_M01_P.txt').read())
Qsymbol=s.sympify(open('workspace/agent4_symbolic_Q.txt').read())
Dsymbol=3*Qsymbol[0,0]*Qsymbol[1,1]-4*Qsymbol[0,1]**2
positive_den=(n-8)*(n-6)**2*(n-4)**2*(n-1)**2
assert s.cancel(Dsymbol+4*P/positive_den)==0
A=s.Poly(P,t).coeff_monomial(t**2)
def signs_after40(expr):
 return [s.sign(c) for c in s.Poly(s.expand(s.cancel(expr).subs(n,y+40)),y).all_coeffs()]
assert all(z==1 for z in signs_after40(A))
assert all(z==-1 for z in signs_after40(s.diff(P,t).subs(t,s.Rational(2,3)/n)))
assert all(z==1 for z in signs_after40(P.subs(t,s.Rational(2,3)/n)))
# So P decreases over [0,2/(3n)] and its value at the right endpoint is positive.
print('CERTIFIED indefinite for ALL n>=40 by negative 2x2 minor and positive-coefficient polynomial checks.')
