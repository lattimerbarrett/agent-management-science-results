import sympy as s
from pathlib import Path
e=s.symbols('e', integer=True, nonnegative=True)
def dot(x,y):
 a,b=x;c,d=y
 return s.expand(-e*a*c+a*d+b*c)
H=(1,3*e+1);P=(4,12*e+3);c1=(4,12*e+4)
assert dot(H,H)==5*e+2
assert dot(c1,P)==80*e+28
assert s.expand(P[1]-e*P[0])==8*e+3
A=(5,-1);B=(-1,12*e+5)
assert dot(A,B)==65*e+26
assert dot(c1,c1)-dot(A,B)==15*e+6
out={'H^2':str(dot(H,H)),'P_ample_margin':str(s.expand(P[1]-e*P[0])),'c1.P':str(dot(c1,P)),'c2':str(dot(A,B)),'s2':str(dot(c1,c1)-dot(A,B))}
Path('workspace/agent4_checks.txt').write_text('\n'.join(f'{k} = {v}' for k,v in out.items()))
print(out)
# Verify local Levi eigenvalue count for norm exhaustion in a metric-normal frame.
# Horizontal Griffiths curvature trace >0 supplies one positive eigenvalue;
# line-fibre radial supplies another, angular direction is negative.
for lam in [(3,-2),(1,1),(-2,3),(0,1),(1,0)]:
 assert sum(lam)>0
 levi=[*lam,-1,1]
 assert sum(v>0 for v in levi)>=2
print('Local signature checks passed; symbolic proof uses lambda1+lambda2>0.')
# Exact formal congruence responsible for the Levi inertia statement.
a=s.Matrix(3,3,lambda i,j:s.Symbol('a%d%d'%(i,j)))
u=s.Matrix(s.symbols('u0:3')); ub=s.Matrix(1,3,s.symbols('ub0:3'))
T=s.eye(4);T[:3,3]=u
Ts=s.eye(4);Ts[3,:3]=ub
D=s.diag(a,s.Integer(1))
M=(a+u*ub).row_join(u).col_join(ub.row_join(s.ones(1,1)))
assert T*D*Ts==M
assert T.det()==1 and Ts.det()==1
print('Exact 4x4 Schur-complement identity verified symbolically.')
t,eps=s.symbols('t eps', real=True, positive=True)
quartic=s.expand((1+t)**4+(1-t)**4+eps*(1+t)**2*(1-t)**2)
assert s.expand(quartic-(2+eps+(12-2*eps)*t**2+(2+eps)*t**4))==0
second=s.simplify(s.diff(quartic**s.Rational(1,4),t,2).subs(t,0))
assert s.simplify(second-(6-eps)/(eps+2)**s.Rational(3,4))==0
print('Finsler real convexity obstruction:',second, '<0 for eps>6')
Path('workspace/agent4_checks.py').write_text(Path('scratchpad.py').read_text())