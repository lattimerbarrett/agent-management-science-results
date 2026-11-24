import sympy as s
from itertools import combinations,combinations_with_replacement
x=s.Matrix(s.symbols('x0:4'))
def skew(ij):
    A=s.zeros(4);i,j=ij;A[i,j]=1;A[j,i]=-1;return A
J=skew((0,1))+skew((2,3))
As=[skew(ij) for ij in combinations(range(4),2) if ij!=(2,3)]
qs=[]
for A,B in combinations(As,2):
    M=(J*x).row_join(A*x).row_join(B*x).extract([1,2,3],[0,1,2])
    q,r=s.div(s.expand(M.det()),x[0],*list(x));assert r==0
    qs.append(q)
mons=[x[i]*x[j] for i,j in combinations_with_replacement(range(4),2)]
C=s.Matrix([[s.Poly(q,*list(x)).coeff_monomial(m) for q in qs] for m in mons])
assert C.det()==2
print('Null-correlation wedge map determinant:',C.det())
