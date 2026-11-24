import sys
import pickle
import numpy as np
from pathlib import Path
from scipy.optimize import linprog
from agent4_flags6 import build

def solve7(a=.09,b=.48,maxiter=1000,tol=1e-7):
 G,B0,B1,M6=build()
 f=np.load('workspace/agent3_flags7.npz');L=f['L6'];M7=f['M']
 C=(B0*np.array([b]*120+[a]*120)[:,None]-B1)@L
 Ms=[np.einsum('ijk,kl->ijl',M,L) for M in M6]+[M7]
 from agent1_type4flags6 import build as build4
 import networkx as nx
 from itertools import combinations
 pairs=list(combinations(range(4),2));reps=[];seen=[]
 for typ in range(64):
  g=nx.Graph();g.add_nodes_from(range(4));g.add_edges_from(p for i,p in enumerate(pairs) if (typ>>i)&1)
  if not any(nx.is_isomorphic(g,h) for h in seen):reps.append(typ);seen.append(g)
 assert len(reps)==11
 addon=build4()
 Ms.extend(np.einsum('ijk,kl->ijl',addon[typ],L) for typ in reps)
 from agent3_type3flags7 import build as build3
 Ms.extend(build3())
 from agent1_type5flags7 import build as build5
 Ms.extend(build5())
 cache=Path('workspace/agent3_search7_state_v2.pkl')
 if cache.exists():
  state=pickle.loads(cache.read_bytes())
  if state['a']==a and state['b']==b:Aub=state['Aub'];start=state['it'];metadata=state['metadata']
  else:Aub=[-row for row in C];start=0;metadata=[]
 else:Aub=[-row for row in C];start=0;metadata=[]
 from agent4_books7 import build as books7
 if not any(mi==-1 for mi,v in metadata):
  B07,B17,patterns=books7();nf=B07.shape[0]//2
  C7=B07*np.array([b]*nf+[a]*nf)[:,None]-B17
  Aub.extend(-r for r in C7);metadata.extend((-1,i) for i in range(len(C7)))
 from agent3_highs import PersistentLP
 lp=PersistentLP(1044,Aub)
 lp.H.setOptionValue("solver","ipm")
 lp.H.changeColsCost(1044,np.arange(1044,dtype=np.int32),np.zeros(1044))
 lp.H.setOptionValue("run_crossover","off")
 for it in range(start,maxiter):
  ok,sol=lp.run()
  # remain in IPM withoutcrossover to obtain central feasible points
  if not ok:
   print('INFEASIBLE',it,flush=True)
   pickle.dump(dict(a=a,b=b,Aub=Aub,it=it,ray=lp.ray(),metadata=metadata),open('workspace/agent3_search7_infeasible.pkl','wb'))
   return False,None
  worst=0;newrows=[]
  for mi,M in enumerate(Ms):
   mat=np.einsum('ijk,k->ij',M,sol)
   ev,vec=np.linalg.eigh((mat+mat.T)/2)
   worst=min(worst,ev[0])
   # Add only the most negative direction from each block per iteration.
   if ev[0]<-tol:
    v=vec[:,0];coef=np.einsum('i,j,ijk->k',v,v,M);Aub.append(-coef);newrows.append(-coef);metadata.append((mi,v))
  if newrows:lp.add(newrows)
  if it%5==0:
   print('iteration',it,'min_eig',worst,'cuts',len(Aub),flush=True)
   cache.write_bytes(pickle.dumps(dict(a=a,b=b,Aub=Aub,it=it+1,metadata=metadata)))
  if worst>=-tol:
   print('NUMERIC FEASIBLE',it,worst,flush=True)
   np.savez('workspace/agent3_search7_solution.npz',a=a,b=b,densities=sol,worst=worst)
   return True,sol
 return None,sol

if __name__=='__main__':solve7()
