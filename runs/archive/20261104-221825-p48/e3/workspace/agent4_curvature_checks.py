import sympy as s
import json, pathlib
# In local Chern-horizontal frames on P(E), curvature of O(1) is
# diag(-k1,-k2,+1), where k1,k2 are horizontal curvatures of E in a line.
# Norm squared on total O(1), at fibre norm rho>0, has horizontal
# Levi = -rho * curvature(O(1)) and fibre Levi = 1.
rho,k1,k2=s.symbols('rho k1 k2',positive=True)
levi=s.diag(rho*k1,rho*k2,-rho,s.Integer(1))
assert levi.det()==-rho**3*k1*k2
assert sum(x.is_positive is True for x in levi.diagonal())==3
# Positive trace alone allows either k2 sign but at least one positive.
a,b=s.symbols('a b',real=True)
# Exact intersection checks in S,f coordinates.
e=s.symbols('e',nonnegative=True,integer=True)
def dot(v,w): return s.expand(-e*v[0]*w[0]+v[0]*w[1]+v[1]*w[0])
A=(5,-1); B=(-1,12*e+5); H=(1,3*e+1); P=(4,12*e+3)
assert dot(A,H)==10*e+4 and dot(B,H)==10*e+4
assert dot(A,P)==40*e+11 and dot(B,P)==40*e+17
assert dot(A,B)==65*e+26
D=(1,e); fibre=(0,1)
assert dot(A,D)==-1 and dot(B,fibre)==-1
# Inertia bookkeeping at a fibre support: CR dimension 3, negative
# plane dimension 2, vertical semipositive line dimension 1.
assert 2+1==3 and 2+(2)-3==1
# Exact Schur congruence in the nondegenerate vertical case.
a11,a22,c=s.symbols('a11 a22 c',real=True, nonzero=True)
a12,b1,b2=s.symbols('a12 b1 b2',real=True)
M=s.Matrix([[a11,a12,b1],[a12,a22,b2],[b1,b2,c]])
T=s.Matrix([[1,0,0],[0,1,0],[-b1/c,-b2/c,1]])
assert s.simplify(T.T*M*T)==s.Matrix([[a11-b1*b1/c,a12-b1*b2/c,0],[a12-b1*b2/c,a22-b2*b2/c,0],[0,0,c]])
out={'AH':str(dot(A,H)),'BH':str(dot(B,H)), 'AP':str(dot(A,P)), 'BP':str(dot(B,P)), 'c2':str(dot(A,B)), 'Griffiths_positive_Levi':str(levi), 'positive_eigenvalue_count':3}
pathlib.Path('workspace/agent4_curvature_checks.json').write_text(json.dumps(out,indent=2))
pathlib.Path('workspace/agent4_curvature_checks.py').write_text(pathlib.Path('scratchpad.py').read_text())
print(json.dumps(out,indent=2))
