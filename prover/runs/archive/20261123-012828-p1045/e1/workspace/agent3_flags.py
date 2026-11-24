import numpy as np
import networkx as nx
from itertools import combinations
from scipy.optimize import linprog
from functools import lru_cache


def build():
 graphs=[g for g in nx.graph_atlas_g() if len(g)==5]
 n=len(graphs)
 B0=np.zeros((40,n));B1=np.zeros((40,n))
 Ms=[np.zeros((6,6,n)),np.zeros((4,4,n)),np.zeros((4,4,n)),np.zeros((2,2,n))]+[np.zeros((8,8,n)) for _ in range(8)]
 patterns=[(i,j,e) for i in range(4) for j in range(i,4) for e in range(2)]
 patidx={p:i for i,p in enumerate(patterns)}
 for gi,g in enumerate(graphs):
  E=lambda u,v:int(g.has_edge(u,v))
  def f(r,ys):
   y,z=ys
   return 2*(E(r,y)+E(r,z))+E(y,z)
  for r in range(5):
   rem=[v for v in range(5) if v!=r]
   for yz in combinations(rem,2):
    other=[v for v in rem if v not in yz]
    Ms[0][f(r,yz),f(r,other),gi]+=1/30
  for u in range(5):
   for v in range(5):
    if u==v:continue
    col=E(u,v)
    rem=[z for z in range(5) if z not in (u,v)]
    for x in rem:
     yz=[z for z in rem if z!=x];y,z=yz
     p1=2*E(u,y)+E(v,y);p2=2*E(u,z)+E(v,z)
     key=(min(p1,p2),max(p1,p2),E(y,z))
     idx=20*col+patidx[key]
     B0[idx,gi]+=1/60
     if E(u,x)==col and E(v,x)==col:
      B1[idx,gi]+=1/60
    for y in rem:
     for z in rem:
      if y==z:continue
      p1=2*E(u,y)+E(v,y);p2=2*E(u,z)+E(v,z)
      Ms[1+col][p1,p2,gi]+=1/120
  from itertools import permutations
  for roots in permutations(range(5),3):
   u,v,w=roots
   typ=4*E(u,v)+2*E(u,w)+E(v,w)
   yz=[z for z in range(5) if z not in roots]
   y,z=yz
   a1=4*E(u,y)+2*E(v,y)+E(w,y)
   a2=4*E(u,z)+2*E(v,z)+E(w,z)
   Ms[4+typ][a1,a2,gi]+=1/60
  for uv in combinations(range(5),2):
   rem=[z for z in range(5) if z not in uv]
   for yz in combinations(rem,2):
    Ms[3][E(*uv),E(*yz),gi]+=1/30
 return graphs,B0,B1,Ms


def solve(a,b,maxiter=500,tol=1e-9,verbose=True):
 graphs,B0,B1,Ms=build()
 cap=np.array([b]*20+[a]*20)
 # book matrices must have cap*base - extension nonnegative
 C=B0*cap[:,None]-B1
 Aub=[-x for x in C];bub=[0.]*len(C)
 for iteration in range(maxiter):
  sol=linprog(np.zeros(len(graphs)),A_ub=np.array(Aub),b_ub=bub,A_eq=[np.ones(len(graphs))],b_eq=[1.],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
  if not sol.success:
   if verbose:print('INFEASIBLE',iteration,sol.message,flush=True)
   return False,iteration,sol
  worst=0
  for M in Ms:
   mat=np.einsum('ijk,k->ij',M,sol.x)
   ev,vec=np.linalg.eigh((mat+mat.T)/2)
   worst=min(worst,ev[0])
   for j,e in enumerate(ev):
    if e < -tol:
     v=vec[:,j]
     coef=np.einsum('i,j,ijk->k',v,v,M)
     Aub.append(-coef);bub.append(0.)
  if verbose and iteration%10==0:print('iteration',iteration,'min_eig',worst,'cuts',len(Aub),flush=True)
  if worst>=-tol:
   if verbose:print('FEASIBLE',iteration,'worst',worst,flush=True)
   return True,iteration,sol
 return None,maxiter,sol

if __name__=='__main__':
 import sys
 a=float(sys.argv[1]) if len(sys.argv)>1 else .09
 b=float(sys.argv[2]) if len(sys.argv)>2 else .486
 solve(a,b)
