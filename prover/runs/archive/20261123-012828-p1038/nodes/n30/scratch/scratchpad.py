import sympy as s
from itertools import combinations
# The universal Pfaffian minor-summation identity that can assemble positive
# principal Pfaffians.  J_ij=1 for i<j and D_ii=(-1)^i*t_i.
def pf(A):
 n=A.rows
 if n==0:return s.Integer(1)
 return s.expand(sum((-1)**(j+1)*A[0,j]*pf(A.extract([k for k in range(n) if k not in [0,j]],[k for k in range(n) if k not in [0,j]])) for j in range(1,n)))
for n in [2,4,6]:
 K=s.zeros(n);J=s.zeros(n)
 ts=s.symbols('t:'+str(n));D=s.diag(*[(-1)**i*ts[i] for i in range(n)])
 for i in range(n):
  for j in range(i+1,n):
   K[i,j]=s.Symbol('k%d%d'%(i,j));K[j,i]=-K[i,j];J[i,j]=1;J[j,i]=-1
 rhs=0
 for k in range(0,n+1,2):
  for I in combinations(range(n),k):rhs+=pf(K.extract(I,I))*s.prod(ts[i] for i in I)
 assert s.expand(pf(J-D*K*D)-rhs)==0
 print('positive Pfaffian minor-sum identity verified, order',n)
# Lowest nontrivial reduced determinant (one axial insertion, m=1).
x,y,c,T=s.symbols('x y c T')
P=[(1-x*T)*(1-y*T),(1-c*T)*(T+x),(T+c)*(T+y)]
Delta=s.det(s.Matrix([[s.expand(p).coeff(T,k) for k in range(3)] for p in P]))
base=(1+c*c)*(1+x*x)*(1+y*y)
assert s.factor(Delta-base)==(y-c)*(x-y)*(1+c*x)
print('one-insertion expansion:',s.factor(Delta-base))
print('Full determinant-to-Pfaffian identification has NOT been computed here.')