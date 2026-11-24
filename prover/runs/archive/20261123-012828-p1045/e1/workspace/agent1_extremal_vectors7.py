import networkx as nx
import numpy as np
from itertools import product,combinations
from math import factorial
from pathlib import Path
import pickle

def build():
 fn=Path('workspace/agent1_extremal_vectors7.npz')
 if fn.exists():return dict(np.load(fn))
 gs=[g for g in nx.graph_atlas_g() if len(g)==7]
 ass=[(0,)+a for a in product(range(3),repeat=6)]
 cross=[sum(a[i]!=a[j] for i,j in combinations(range(7),2)) for a in ass]
 rn=[];tn=[]
 for gi,g in enumerate(gs):
  aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(g,g).isomorphisms_iter())
  mult=factorial(7)//aut;e=g.number_of_edges();edges=list(g.edges())
  rnum=mult*13**e*12**(21-e);tnum=0
  for a,c in zip(ass,cross):
   if all(a[i]!=a[j] for i,j in edges):tnum+=3*13**e*12**(c-e)*25**(21-c)
  rn.append(rnum);tn.append(mult*tnum)
  if gi%200==0:print('vectors',gi,flush=True)
 assert sum(rn)==25**21
 assert sum(tn)==3**7*25**21
 out=dict(random=np.array([x/25**21 for x in rn]),tripartite=np.array([x/(3**7*25**21) for x in tn]),p=np.array(13/25))
 np.savez(fn,**out)
 Path('workspace/agent1_extremal_vectors7_exact.pkl').write_bytes(pickle.dumps(dict(random_num=rn,random_den=25**21,tripartite_num=tn,tripartite_den=3**7*25**21)))
 return out
if __name__=='__main__':
 out=build()
 from agent4_books7 import build as books
 B0,B1,_=books();a=(13/25)**2/3;b=(1+2*(12/25)**2)/3
 for name in ['random','tripartite']:
  x=out[name]
  aa=(13/25)**2 if name=='random' else a
  bb=(12/25)**2 if name=='random' else b
  d=(B0*np.r_[np.full(996,bb),np.full(996,aa)][:,None]-B1)@x
  print(name,'book min',d.min(),'red maxabs',abs(d[996:]).max(),flush=True)
  assert d.min()>-1e-12
