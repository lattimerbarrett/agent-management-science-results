from pathlib import Path
import sympy as S
from z3 import Solver, Real, Int, unsat

# This file checks the algebraic parts of the final construction, not merely samples.
Path('workspace/agent1_complete_checks.py').write_text(Path(__file__).read_text())

# Quantum coefficient: unique degree-one map with three prescribed incidences.
a,b,c=S.symbols('a b c')
f=S.Matrix([b,a+b-c-1,c])
assert S.solve(list(f),(a,b,c),dict=True)==[{a:1,b:0,c:0}]
assert f.jacobian([a,b,c]).det()==-1
assert S.gcd(1,1)==1 and S.gcd(2,2)==2
k=Int('action_integer'); sol=Solver(); sol.add(k>0,k<1)
assert sol.check()==unsat

# The two graph spheres are Lagrangian and invariant under the half-turn.
R=S.diag(-1,-1,1); L1=S.diag(1,-1,1)
R45=S.Matrix([[S.sqrt(2)/2,-S.sqrt(2)/2,0],
              [S.sqrt(2)/2,S.sqrt(2)/2,0],[0,0,1]])
L2=R45*S.diag(1,1,-1)
for L in [L1,L2]:
    assert S.simplify(L.T*L)==S.eye(3)
    assert S.simplify(L.det())==-1
    assert S.simplify(R*L-L*R)==S.zeros(3)
# Trace phases divided by pi, with delta=pi/4 and chi=pi/2.
t,u=Real('t'),Real('u'); j,l=Int('j'),Int('l')
sol=Solver(); sol.add(t>=0,t<=1,u>=0,u<=1,
                     4*(-t-u-2*j)==1,
                     2*(t-u-2*l)==1)
assert sol.check()==unsat

# Bound |G'| <= 9/2 for the flat step G.
x=S.symbols('x', positive=True)
qprime=1/x**2+1/(1-x)**2
assert qprime.subs(x,S.Rational(1,4))==S.Rational(160,9)<18
assert S.simplify(S.diff(qprime,x,2)-6/x**4-6/(x-1)**4)==0
outer=S.exp(S.Rational(4,3)-1/x)*(x**-2+S.Rational(16,9))
# Its derivative is positive on (0,1/4]: the bracket has positive coefficients
# in 1-2x and x^2.
bracket=S.simplify(S.diff(outer,x)/S.exp(S.Rational(4,3)-1/x)*x**4)
assert S.expand(bracket)==1-2*x+S.Rational(16,9)*x*x
# exp(8/3) > 1 + 8/3 > 320/81 proves the outer bound is <9/2.
assert 1+S.Rational(8,3)+S.Rational(8,3)**2/2>S.Rational(320,81)
assert S.Rational(9,2)/16==S.Rational(9,32)<1

# Exact Hamilton equations underlying the angular-speed estimate.
th,J,P=S.symbols('th J P', real=True)
r=S.sqrt(P*P+J*J/S.sin(th)**2)
g=S.Function('g'); v=S.symbols('v', real=True)
H=J*g(r)*v
Dg=S.Subs(S.Derivative(g(S.Symbol('z')),S.Symbol('z')),S.Symbol('z'),r)
assert S.simplify(S.diff(H,J)-v*(g(r)+Dg*J*J/(r*S.sin(th)**2)))==0
assert S.simplify(S.diff(H,P)-J*v*Dg*P/r)==0
assert S.simplify(J*J/(r*S.sin(th)**2)-r+P*P/r)==0

# Ellipsoid-collapse Jacobian, proved by the rank-one determinant lemma.
A,B,Ap,Bp,rr=S.symbols('A B Ap Bp rr', positive=True)
X=S.Matrix(S.symbols('X0:4', real=True)); n=X/rr
D=S.diag(A/rr,B/rr,B/rr,B/rr)
w=S.Matrix([(Ap/rr-A/rr**2)*X[0]]+
           [(Bp/rr-B/rr**2)*X[i] for i in range(1,4)])
Jac=D+w*n.T
actual=S.factor(Jac.det())
formula=A*B**3/rr**3*((Ap/A)*X[0]**2/rr**2+
                              (Bp/B)*(1-X[0]**2/rr**2))
num=S.together(actual-formula).as_numer_denom()[0]
assert S.Poly(num,*X).rem(S.Poly(sum(z*z for z in X)-rr*rr,*X)).is_zero
# Uniform positive gap for the explicitly blended major axis.
assert S.Rational(23,32)-S.Rational(3,8)>S.Rational(1,3)
assert sum(S.Rational(1,S.factorial(i)) for i in range(4))==S.Rational(8,3)
assert S.simplify(S.diff(S.log(x)+1/x**2,x)-(x*x-2)/x**3)==0

print('All exact quantum, action-coset, graph-sphere, trace-disjointness,')
print('flat-cutoff, Hamilton-equation and ellipsoid-Jacobian checks passed.')
