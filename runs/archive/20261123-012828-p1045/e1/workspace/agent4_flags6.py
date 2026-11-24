import numpy as np
import networkx as nx
from itertools import combinations, permutations
from scipy.optimize import linprog
from pathlib import Path
import pickle

def build():
 cache=Path('workspace/agent4_flags6.pkl')
 if cache.exists():return pickle.loads(cache.read_bytes())
 graphs=[g for g in nx.graph_atlas_g() if len(g)==6];n=len(graphs)
 edges3=list(combinations(range(3),2)); perms3=list(permutations(range(3)))
 def canon(code):
  bits=[(code>>i)&1 for i in range(9)]; vals=[]
  for pm in perms3:
   ar=[bits[pm[i]] for i in range(3)]+[bits[3+pm[i]] for i in range(3)]
   ar += [bits[6+edges3.index(tuple(sorted((pm[i],pm[j]))))] for i,j in edges3]
   vals.append(sum(x<<i for i,x in enumerate(ar)))
  return min(vals)
 cc=[canon(i) for i in range(512)]; cs=sorted(set(cc)); ci={x:i for i,x in enumerate(cs)}
 C0=np.zeros((240,n)); C1=np.zeros((240,n))
 patterns=[(i,j,e) for i in range(4) for j in range(i,4) for e in range(2)];pi={x:i for i,x in enumerate(patterns)}
 Ms=[np.zeros((6,6,n)),np.zeros((4,4,n)),np.zeros((4,4,n)),np.zeros((4,4,n)),np.zeros((20,20,n)),np.zeros((20,20,n))]
 Ms += [np.zeros((8,8,n)) for _ in range(8)]
 for gi,g in enumerate(graphs):
  E=lambda u,v:int(g.has_edge(u,v))
  def oneflag(r,yz):
   y,z=yz;return 2*(E(r,y)+E(r,z))+E(y,z)
  def twoflag(u,v,yz):
   y,z=yz;a=2*E(u,y)+E(v,y);b=2*E(u,z)+E(v,z)
   return pi[min(a,b),max(a,b),E(y,z)]
  for r in range(6):
   rem=[i for i in range(6) if i!=r]
   for yz in combinations(rem,2):
    others=[i for i in rem if i not in yz]
    for st in combinations(others,2):Ms[0][oneflag(r,yz),oneflag(r,st),gi]+=1/180
  for u,v in permutations(range(6),2):
   col=E(u,v);rem=[i for i in range(6) if i not in (u,v)]
   for x in rem:
    yz=[i for i in rem if i!=x]
    ar=[E(u,y) for y in yz]+[E(v,y) for y in yz]+[E(yz[i],yz[j]) for i,j in edges3]
    idx=120*col+ci[cc[sum(x<<i for i,x in enumerate(ar))]]
    C0[idx,gi]+=1/120
    if E(u,x)==col and E(v,x)==col:C1[idx,gi]+=1/120
   for y,z in permutations(rem,2):
    a=2*E(u,y)+E(v,y);b=2*E(u,z)+E(v,z)
    Ms[1+col][a,b,gi]+=1/360
   for yz in combinations(rem,2):
    st=[i for i in rem if i not in yz]
    Ms[4+col][twoflag(u,v,yz),twoflag(u,v,st),gi]+=1/180
  for abc in combinations(range(6),3):
   xyz=[i for i in range(6) if i not in abc]
   a=sum(E(i,j) for i,j in combinations(abc,2));b=sum(E(i,j) for i,j in combinations(xyz,2))
   Ms[3][a,b,gi]+=1/20
  for u,v,w in permutations(range(6),3):
   typ=4*E(u,v)+2*E(u,w)+E(v,w);rem=[i for i in range(6) if i not in (u,v,w)]
   for y,z in permutations(rem,2):
    a=4*E(u,y)+2*E(v,y)+E(w,y);b=4*E(u,z)+2*E(v,z)+E(w,z)
    Ms[6+typ][a,b,gi]+=1/720
 out=(graphs,C0,C1,Ms);cache.write_bytes(pickle.dumps(out));return out

def solve(a,b,maxiter=1000,tol=1e-8):
 gs,C0,C1,Ms=build();cap=np.array([b]*120+[a]*120);C=C0*cap[:,None]-C1
 Aub=[-r for r in C];bub=[0.]*len(C)
 for it in range(maxiter):
  sol=linprog(np.zeros(len(gs)),A_ub=np.array(Aub),b_ub=bub,A_eq=[np.ones(len(gs))],b_eq=[1.],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
  if not sol.success:
   print('INFEASIBLE',it,sol.message,flush=True);return False,sol
  worst=0
  for M in Ms:
   mat=np.einsum('ijk,k->ij',M,sol.x);ev,vec=np.linalg.eigh((mat+mat.T)/2);worst=min(worst,ev[0])
   for j,e in enumerate(ev):
    if e < -tol:
     coef=np.einsum('i,j,ijk->k',vec[:,j],vec[:,j],M);Aub.append(-coef);bub.append(0.)
  if it%10==0:print('iteration',it,'eig',worst,'cuts',len(Aub),flush=True)
  if worst>=-tol:
   print('FEASIBLE',it,'eig',worst,flush=True)
   np.savez('workspace/agent4_flags6_solution.npz',a=a,b=b,densities=sol.x)
   return True,sol
 print('MAXITER',worst,flush=True);return None,sol
if __name__=='__main__':
 import sys
 solve(float(sys.argv[1]) if len(sys.argv)>1 else .09,float(sys.argv[2]) if len(sys.argv)>2 else .48)
