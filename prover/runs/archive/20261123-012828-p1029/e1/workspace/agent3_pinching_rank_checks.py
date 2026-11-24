import sympy as s
from pathlib import Path
import random
random.seed(301)
def support(P):
    cs=P.columnspace()
    if not cs: return s.zeros(P.rows)
    B=s.Matrix.hstack(*cs)
    return B*(B.T*B).inv()*B.T
count=0
for n in range(2,8):
 for r in range(1,n):
  for k in range(1,n):
   # rational orthogonal Householder change of basis
   v=s.Matrix([random.randrange(1,9) for _ in range(n)])
   Q=s.eye(n)-2*v*v.T/(v.T*v)[0]
   p=Q*s.diag(*([1]*r+[0]*(n-r)))*Q.T
   e=s.diag(*([1]*k+[0]*(n-k)))
   f=s.eye(n)-e
   D=e*p*e+f*p*f
   z=support(D)
   assert (z-p)*p==s.zeros(n)
   # meet dimensions from rank of complementary compression maps
   meet_pe=r-(f*p).rank()
   meet_pf=r-(e*p).rank()
   assert z.rank()-r==r-meet_pe-meet_pf
   assert D.rank()==(e*p*e).rank()+(f*p*f).rank()
   count+=1
print('Exact rational pinching-rank identities checked:',count)
