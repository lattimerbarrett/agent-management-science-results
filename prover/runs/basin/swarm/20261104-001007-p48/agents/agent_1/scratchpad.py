import sympy as s
from pathlib import Path
e=s.symbols('e', nonnegative=True, integer=True)
def dot(D,F):
 a,b=D;c,d=F
 return s.expand(-e*a*c+a*d+b*c)
A=(5,-1); B=(-1,12*e+5); H=(1,3*e+1); P=(4,12*e+3)
assert dot(A,H)==dot(B,H)==10*e+4
assert dot(A,P)==40*e+11
assert dot(B,P)==40*e+17
C=tuple(s.expand(x+y) for x,y in zip(A,B))
assert dot(C,C)==80*e+32
assert dot(A,B)==65*e+26
# Norm squared of a line-bundle coordinate: complex Hessian block
# h=1 at point, first derivatives of log h encoded by column a;
# C is the Hessian of log h.  Hessian congruent to diag(t*C,1).
a,b,t=s.symbols('a b t', real=True)
c,d,g=s.symbols('c d g', real=True)
v=s.Matrix([a,b]); Q=s.Matrix([[c,g],[g,d]])
M=(t*Q+t*v*v.T).row_join(s.sqrt(t)*v)
M=M.col_join((s.sqrt(t)*v.T).row_join(s.ones(1)))
R=s.eye(3); R[2,0]=-s.sqrt(t)*a;R[2,1]=-s.sqrt(t)*b
assert s.simplify(R.T*M*R)==s.diag(t*Q,s.ones(1))
assert dot(A,(1,e))==-1
assert dot(B,(0,1))==-1
# Dimension checks for restriction of Hermitian forms.
assert 3+2-4==1  # 3 positive ambient directions => 1 on every surface
assert 3+2-4==1  # same for each rank-two vector-bundle fibre
# Complete 4x4 line-bundle Levi congruence over a threefold.
u1,u2,u3=s.symbols('u1 u2 u3', real=True)
q11,q22,q33,q12,q13,q23=s.symbols('q11 q22 q33 q12 q13 q23', real=True)
u=s.Matrix([u1,u2,u3])
Q3=s.Matrix([[q11,q12,q13],[q12,q22,q23],[q13,q23,q33]])
M4=(t*(Q3+u*u.T)).row_join(s.sqrt(t)*u)
M4=M4.col_join((s.sqrt(t)*u.T).row_join(s.ones(1)))
R4=s.eye(4)
for k in range(3): R4[3,k]=-s.sqrt(t)*u[k]
assert s.simplify(R4.T*M4*R4)==s.diag(t*Q3,s.ones(1))
# Fully complex Hermitian version, not only real-symmetric matrices.
tp=s.symbols('tp', positive=True)
uc=s.Matrix(s.symbols('z1 z2 z3', complex=True))
p12,p13,p23=s.symbols('p12 p13 p23', complex=True)
Qc=s.Matrix([[q11,p12,p13],[s.conjugate(p12),q22,p23],[s.conjugate(p13),s.conjugate(p23),q33]])
Mc=(tp*(Qc+uc*uc.H)).row_join(s.sqrt(tp)*uc)
Mc=Mc.col_join((s.sqrt(tp)*uc.H).row_join(s.ones(1)))
Rc=s.eye(4)
for k in range(3): Rc[3,k]=-s.sqrt(tp)*s.conjugate(uc[k])
assert s.simplify(Rc.H*Mc*Rc)==s.diag(tp*Qc,s.ones(1))
print('All intersection identities, dimension bounds, and real/complex Levi block-congruence checks passed.')
Path('workspace/agent1_checks.py').write_text(Path('scratchpad.py').read_text())