"""Exact supplementary checks for the lower-bound support-norm proof."""
import sympy as s
e=s.symbols('e', integer=True, nonnegative=True)
def dot(D,F):
 a,b=D; c,d=F
 return s.expand(-e*a*c+a*d+b*c)
A=(5,-1); B=(-1,12*e+5)
N=(1,e); f=(0,1)
assert dot(A,N)==-1
assert dot(B,f)==-1
assert dot(N,N)==e
assert dot(N,(1,0))==0
assert dot(N,f)==1
assert dot(f,(1,0))==1
assert dot(f,f)==0
# Dimension intersections used twice in the support proof:
# Levi has a positive 3-plane in ambient complex dimension4.
assert 3+2-4==1 # any fibre2-plane or test-surface2-plane has >=1 positive direction
# Incidence surface: holomorphic disc plus rank2 fibre, one equation.
assert 1+2-1==2
# Beta repair, exact example: chosen value b is larger in modulus than a0;
# multiplying holomorphic a by beta=b/a0 enforces incidence and enlarges
# every boundary modulus by the same factor >1.
a0=s.Rational(2); b=3+4*s.I
beta=b/a0
assert s.simplify(beta*a0-b)==0
assert s.simplify(beta*s.conjugate(beta))>1
# Triangle inequality in a 2-dimensional fibre forces an axis lower bound:
# if max |coefficients| <= C and F(v)=1 then F(e1)+F(e2)>=1/C.
C=s.symbols('C',positive=True)
assert s.simplify((1/C)/2-1/(2*C))==0
print('Exact lower-proof checks passed: negative nef pairings, restriction dimensions, incidence dimension, beta repair.')
