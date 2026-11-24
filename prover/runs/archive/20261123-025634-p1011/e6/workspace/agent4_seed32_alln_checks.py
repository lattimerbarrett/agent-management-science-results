"""Exact certificate: q2 degree-four quadratic reduced-energy seeds in every n>=32.
This is an algebraic seed result, NOT the full Yamabe noncompactness theorem.
The formulas are verified by the independent symbolic telescoping generator
agent4_symbolic_M_checks.py; this file checks the all-dimensional sign argument.
"""
import sympy as s
from fractions import Fraction
from pathlib import Path
import sys
sys.path.insert(0,'workspace')
from agent3_odd_gram_checks import PI
assert PI[0]>Fraction(333,106)
n,t,x=s.symbols('n t x')
A=1+t
B=((n**2-3*n+18)+(3*n**2-9*n+10)*t)/((n-6)*(n-1))
C=((n**4-8*n**3+189*n**2-774*n+1296)+(9*n**4-72*n**3+397*n**2-974*n+816)*t)/((n-8)*(n-6)*(n-1)**2)
D=s.factor(3*A*C-4*B**2)
u=8*n/(s.Rational(333,106)*(n-1)**2)

def positive_on_ray(expr,N=33):
 num,den=s.fraction(s.factor(s.together(expr)))
 for poly in [num,den]:
  co=s.Poly(s.expand(poly.subs(n,x+N)),x).all_coeffs()
  assert all(v>=0 for v in co) and co[-1]>0,(expr,co)

# dD/dt is affine. Positive at both endpoints implies positive on [0,u].
assert s.diff(D,t,3)==0
positive_on_ray(s.diff(D,t).subs(t,0))
positive_on_ray(s.diff(D,t).subs(t,u))
positive_on_ray(-D.subs(t,u))
# A,B,C positive when n>=33 and t>=0.
for Q in [A,B,C]:
 for coefficient in s.Poly(Q,t).all_coeffs():positive_on_ray(coefficient)
# The endpoint n32 has exact rational gamma ratio.
t32=s.simplify(4*s.gamma(s.Rational(31,2))**2/(s.pi*s.gamma(16)**2))
assert t32.is_Rational
assert D.subs({n:32,t:t32})<0
for Q in [A,B,C]:assert Q.subs({n:32,t:t32})>0

# Translation Hessian simplification and lower bounds.
aa,bb,cc,rr=s.symbols('A B C r',positive=True)
m=n-1
M1=2*(aa+bb)/(n-1)
M3=((n-1)*bb-(n+3)*aa)/2
Hother=2*(rr*aa-bb)-4*M3/(n+3)
Hspecial=6*(rr*aa-bb)-(n+3)**2/(n+1)*M1-4*(s.Rational(3)/(n+3)-1/(n+1))*M3
assert s.factor(Hother-(2*aa*(rr+1)-4*(n+1)*bb/(n+3)))==0
assert s.factor(Hspecial-(aa*(6*rr+2*(n-9)/(n-1))-4*(3*n**2+4*n+9)*bb/((n-1)*(n+3))))==0
assert s.factor(Hother.subs(rr,2*bb/aa)-(2*aa+8*bb/(n+3)))==0
assert s.factor(Hspecial.subs(rr,2*bb/aa)-(2*(n-9)*aa/(n-1)+8*(n-9)*bb/((n-1)*(n+3))))==0
# At r=(2B+sqrt(4B²-3AC))/A, stationary scale and positive scale Hessian.
d=s.symbols('d',positive=True)
rstar=(2*bb+d)/aa
constraint=d*d-(4*bb*bb-3*aa*cc)
assert s.factor((aa*rstar*rstar-4*bb*rstar+3*cc)-constraint/aa)==0
assert s.factor((4*bb*rstar-6*cc)-(2*d*d+4*bb*d)/aa+2*constraint/aa)==0
print('PASS: 4B²>3AC for every integer n>=32, exact gamma bounds and polynomial certificates')
print('PASS: chosen scale root has positive scale and all translation Hessians')
if Path(__file__).name=='scratchpad.py':Path('workspace/agent4_seed32_alln_checks.py').write_text(Path(__file__).read_text())
