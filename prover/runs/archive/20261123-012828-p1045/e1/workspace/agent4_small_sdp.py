import numpy as np
from scipy.optimize import linprog
from itertools import combinations_with_replacement

def solve(a,r,k=3,tol=1e-9,ret=False):
 s=1-r;ps=list(combinations_with_replacement(range(k),2));n=2+2*k+2*len(ps);c=0;one=n-1
 muB=list(range(1,k+1));muR=list(range(k+1,2*k+1));gb={p:1+2*k+j for j,p in enumerate(ps)};gr={p:1+2*k+len(ps)+j for j,p in enumerate(ps)}
 def id(g,i,j):return g[tuple(sorted((i,j)))]
 mats=[]
 for mass,mu,gg in [(s,muB,gb),(r,muR,gr)]:
  M=np.zeros((k+1,k+1,n));M[0,0,one]=mass
  for i in range(k):
   M[0,i+1,mu[i]]=M[i+1,0,mu[i]]=1
   for j in range(k):M[i+1,j+1,id(gg,i,j)]=1
  mats.append(M)
 C=np.zeros((k,k,n))
 for i in range(k):
  for j in range(k):C[i,j,id(gb,i,j)]=-1
  C[i,i,id(gb,i,i)]+=k-1
 mats.append(C)
 rows=[]
 def add(d):
  v=np.zeros(n)
  for i,x in d.items():v[i]+=x
  rows.append(v)
 for i in range(k):
  add({gb[i,i]:1,gr[i,i]:1,muB[i]:-2,muR[i]:-2,c:1})
  add({gb[i,i]:1,muB[i]:-1});add({gr[i,i]:1,muR[i]:-1})
  if i:add({gr[0,0]:1,gr[i,i]:-1})
 for i in range(k):
  for j in range(i+1,k):add({gb[i,j]:1,gr[i,j]:1,one:-a})
 add({gr[0,0]:1,one:-r*(a-r)/s})
 bounds=[(0,1)]+[(0,s)]*k+[(0,r)]*k+[(0,s)]*len(ps)+[(0,r)]*len(ps)+[(1,1)]
 obj=np.zeros(n);obj[c]=-1
 for it in range(1000):
  opt=linprog(obj,A_ub=rows,b_ub=np.zeros(len(rows)),bounds=bounds,method='highs')
  if not opt.success:return None
  x=opt.x;worst=0
  for M in mats:
   H=np.einsum('ijk,k->ij',M,x);ev,V=np.linalg.eigh(H);worst=min(worst,min(ev))
   for j,e in enumerate(ev):
    if e < -tol:
     v=-np.einsum('i,j,ijk->k',V[:,j],V[:,j],M);v/=max(abs(v));rows.append(v)
  if worst>=-tol:
   if ret:return opt.x,gb,gr,muB,muR,it,worst
   return opt.x[c],it,worst
 return opt.x[c],it,worst
if __name__=='__main__':
 a=.09
 for r in [.0001,.001,.01,.03,.067,.08,.089]:print(r,solve(a,r),flush=True)
