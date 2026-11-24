from sage.all import matrix,ZZ,SimplicialComplex
from itertools import combinations,product
from math import comb,factorial
import time

def indices(m):
 U=(1<<m)-1
 rows=[];cols=[]
 for A in range(1<<m):
  if A.bit_count()<3:continue
  rest=U^A;B=rest
  while True:
   if m-A.bit_count()-B.bit_count()>=3:rows.append((A,B))
   if not B:break
   B=(B-1)&rest
 for e in range(3):
  for Es in combinations(range(m),e):
   E=sum(1<<j for j in Es);rest=U^E;D=rest
   while True:
    C=rest^D
    if D.bit_count()<=m-5 and C.bit_count()>=3:cols.append((C,D))
    if not D:break
    D=(D-1)&rest
 return rows,cols

def result(m):
 rows,cols=indices(m)
 P=matrix(ZZ,len(rows),len(cols),lambda i,j:int((rows[i][0]&~cols[j][0])==0 and (rows[i][1]&~cols[j][1])==0))
 ds=P.elementary_divisors()
 rk=sum(d!=0 for d in ds)
 Q=sum(comb(m,a)*comb(m-a,b) for a in range(3,m-5) for b in range(3,m-a-2))
 a=len(rows)-rk-Q
 E=(m**4+14*m**3-m**2+34*m+24)//24
 tors=[int(d) for d in ds if d>1]
 return a,a+E,tors

if __name__=='__main__':
 for m in [7,8]:
  t=time.time();a,b,tors=result(m)
  print(m,'sphere counts',a,b,'torsion orders',tors,'time',time.time()-t,flush=True)
  caps=[2,2,2,m-5]
  facets=[tuple(4*j+x for j,x in enumerate(w)) for w in product(range(4),repeat=m) if all(w.count(i)<=caps[i] for i in range(4))]
  K=SimplicialComplex(facets)
  H=K.homology(algorithm='no_chomp')
  print('independent simplicial homology',H,flush=True)
  assert list(H[m-3].invariants()).count(0)==a
  assert list(H[m-2].invariants()).count(0)==b
  assert sorted(int(x) for x in H[m-3].invariants() if x>1)==tors
  assert all(len(g.invariants())==0 for k,g in H.items() if k not in (m-3,m-2))
  # Check Euler formula directly, enumerating face counts by their four row sizes.
  ec=0
  for sizes in product(*[range(c+1) for c in caps]):
   k=sum(sizes)
   if k<=m:
    nf=factorial(m)//factorial(m-k)
    for s in sizes:nf//=factorial(s)
    ec+=(-1)**k*nf
  assert -ec==(-1)**(m-2)*(b-a)
 print('All assertions passed.')
