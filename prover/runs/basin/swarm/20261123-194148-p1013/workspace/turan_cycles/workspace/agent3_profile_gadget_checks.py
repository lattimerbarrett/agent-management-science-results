import itertools, math, z3
import numpy as np
from pathlib import Path

def dictatorship_check(r,m):
 V=list(itertools.product(range(r),repeat=m)); edges=[(i,j)for i,x in enumerate(V)for j,y in enumerate(V[:i])if all(a!=b for a,b in zip(x,y))]
 col=[z3.Int('d%d_%d_%d'%(r,m,i))for i in range(len(V))];s=z3.Solver()
 for c in col:s.add(c>=0,c<r)
 for i,j in edges:s.add(col[i]!=col[j])
 for a in range(r):s.add(col[V.index((a,)*m)]==a)
 for j in range(m):s.add(z3.Or([col[i]!=x[j]for i,x in enumerate(V)]))
 assert s.check()==z3.unsat,(r,m)
 A=np.zeros((len(V),len(V)),dtype=np.int64)
 for i,j in edges:A[i,j]=A[j,i]=1
 # Verify exact integer eigenbasis: tensor products of constant and centered alphabet vectors.
 basis=[np.ones(r,dtype=np.int64)]+[np.eye(r,dtype=np.int64)[i]-np.eye(r,dtype=np.int64)[r-1]for i in range(r-1)]
 vals=[];B=[]
 for ks in itertools.product(range(r),repeat=m):
  v=basis[ks[0]]
  for k in ks[1:]:v=np.kron(v,basis[k])
  t=sum(k!=0 for k in ks);lam=(-1)**t*(r-1)**(m-t)
  assert np.array_equal(A@v,lam*v)
  vals.append(lam);B.append(v)
 assert np.linalg.matrix_rank(np.array(B,dtype=float))==len(V)
 assert min(vals)==-(r-1)**(m-1)
 assert vals.count(min(vals))==m*(r-1)
 print('dictatorship/exact eigenbasis PASS',r,m,len(V),flush=True)

def anchors(r,Q,M,ntarget):
 # Complete (r-1)-partite anchor classes; all targetvertices adjacent every anchor.
 na=(r-1)*M;n=na+ntarget
 E=[(a,b)for a in range(na)for b in range(a)if a//M!=b//M]+[(a,b)for a in range(na)for b in range(na,n)]
 return n,E,list(range(na,n))

def bounded_coloring(n,E,r,Q):
 c=[z3.Int('c'+str(i))for i in range(n)];s=z3.Solver()
 for x in c:s.add(x>=0,x<r)
 for u in range(n):s.add(z3.PbLe([(c[u]==c[v],1)for a,b in E for v in ([b]if a==u else [a]if b==u else [])],Q))
 return s,c

def gadget_check(r,Q):
 M=r*Q+1;n,E,T=anchors(r,Q,M,M+1)
 s,c=bounded_coloring(n,E,r,Q);s.add(z3.Or([c[T[0]]!=c[t]for t in T[1:]]));assert s.check()==z3.unsat
 # Protected inequality: u=T0; M clones=T1..TM; endpointv adjacent allclones.
 v=n; EE=E+[(v,t)for t in T[1:]]
 s,c=bounded_coloring(n+1,EE,r,Q);s.add(c[v]==c[T[0]]);assert s.check()==z3.unsat
 print('anchor equality/protected inequality PASS',r,Q,M,flush=True)

if __name__=='__main__':
 for r,m in [(3,1),(3,2),(3,3),(4,2)]:dictatorship_check(r,m)
 for r,Q in [(3,0),(3,1),(3,2),(4,1)]:gadget_check(r,Q)
 print('ALL GADGET CHECKS PASSED')
