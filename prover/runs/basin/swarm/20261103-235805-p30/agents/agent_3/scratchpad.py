import sympy as S
from itertools import combinations
from pathlib import Path
Path('workspace/agent3_independent.py').write_text(Path(__file__).read_text())
# Independent exact check of the complete n=4 bilinear construction.
m=2; n=4; t=S.symbols('t'); w=S.Poly((t-1)*(t-2),t)
# Coordinates are (Re z0, Re z1, Im z0, Im z1).
z=[S.Matrix([1,0]),S.Matrix([0,1]),S.Matrix([S.I,0]),S.Matrix([0,S.I])]
K=S.Matrix([[0,1],[-1,0]])
def bilinear(u,v):
    c=[u[0]*v[0],u[0]*v[1]+u[1]*v[0],u[1]*v[1]]
    rem=[S.expand(c[k]-w.nth(k)*c[2]) for k in range(2)]
    h=(S.conjugate(u).T*v)[0]
    hK=(S.conjugate(u).T*(S.I*K)*v)[0]
    return [S.re(h),S.re(hK)]+[f(c) for c in rem for f in (S.re,S.im)]
A=[S.zeros(n) for _ in range(6)]
for a in range(n):
 for b in range(n):
  val=bilinear(z[a],z[b])
  for k in range(6): A[k][a,b]=val[k]
assert A[0]==S.eye(n)
assert all(M==M.T for M in A)
PD=[A[0]]
for M in A[1:]:
 C=1+max(sum(abs(M[i,j]) for j in range(n)) for i in range(n))
 P=C*S.eye(n)+M
 assert all(P[i,i]>sum(abs(P[i,j]) for j in range(n) if j!=i) for i in range(n))
 PD.append(P)
print('Six exact symmetric matrices, first identity; shifted matrices strictly diagonally dominant PD:')
for M in PD: print(M.tolist())
# Every possible root factorization is checked for m=2,4,8.
for m in [2,4,8]:
 N=2*m-2; roots=[2**i for i in range(N)]; count=0
 for inds in combinations(range(N),m-1):
  I=set(inds); J=set(range(N))-I
  p=S.Poly(S.prod(t-roots[i] for i in I),t)
  q=S.Poly(S.prod(t-roots[i] for i in J),t)
  dot=sum(p.nth(k)*q.nth(k) for k in range(m))
  wedge=p.nth(m-2)*q.nth(m-1)-p.nth(m-1)*q.nth(m-2)
  assert dot>0 and wedge%2==1
  assert wedge==sum(roots[i] for i in J)-sum(roots[i] for i in I)
  count+=1
 print('m=',m,'all',count,'complementary factorizations have positive dot and odd nonzero skew product')
