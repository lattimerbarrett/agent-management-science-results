import networkx as nx
import itertools as it
import numpy as np
from z3 import Solver,Int,Or,sat,unsat
from pathlib import Path

def tensor(r,m):
 vs=list(it.product(range(r),repeat=m));G=nx.Graph();G.add_nodes_from(vs)
 G.add_edges_from((a,b) for a,b in it.combinations(vs,2) if all(x!=y for x,y in zip(a,b)))
 return G

def colorable(G,q,deleted=()):
 vs=set(G)-set(deleted);x={v:Int('x'+str(i)) for i,v in enumerate(vs)};s=Solver()
 s.add(*[Or(*[x[v]==c for c in range(q)]) for v in vs])
 s.add(*[x[a]!=x[b] for a,b in G.edges() if a in vs and b in vs])
 return s.check()==sat

def realize(r,Fs):
 k=len(Fs);ports=[(i,v) for i,F in enumerate(Fs) for v in F]
 proper=[]
 for F in Fs:
  col=nx.coloring.greedy_color(F,strategy='largest_first');assert max(col.values())<r;proper.append(col)
 rows=[]
 for i in range(k):rows.append({p:0 if p[0]==i else proper[p[0]][p[1]] for p in ports})
 D=tensor(r,k);G=nx.relabel_nodes(D,lambda v:('hard',v));hard=set(G)
 for p in ports:
  h=('hard',tuple(row[p] for row in rows));P=('port',p);G.add_node(P)
  aux=[('aux',p,j) for j in range(r-1)];G.add_nodes_from(aux);hard.update(aux)
  G.add_edges_from(it.combinations(aux,2));G.add_edges_from((a,h) for a in aux);G.add_edges_from((a,P) for a in aux)
 for i,F in enumerate(Fs):G.add_edges_from((('port',(i,a)),('port',(i,b))) for a,b in F.edges())
 # Embeddings into complete r-partite graph with exactly selected soft F inside one part.
 for j,row in enumerate(rows):
  c={('hard',v):v[j] for v in D}
  for p in ports:
   c[('port',p)]=row[p]
   choices=iter(a for a in range(r) if a!=row[p])
   for i in range(r-1):c[('aux',p,i)]=next(choices)
  mono={(a,b) for a,b in G.edges() if c[a]==c[b]}
  assert len(mono)==Fs[j].number_of_edges()
  assert all(a[0]==b[0]=='port' and a[1][0]==b[1][0]==j for a,b in mono)
 return G,hard

if __name__=='__main__':
 for r,m in [(3,1),(3,2),(3,3),(4,2)]:
  D=tensor(r,m);val=np.linalg.eigvalsh(nx.to_numpy_array(D));assert abs(val[0]+(r-1)**(m-1))<1e-7
  mis=list(nx.find_cliques(nx.complement(D)));alpha=max(map(len,mis));maxis=[set(x) for x in mis if len(x)==alpha]
  slices=[{v for v in D if v[i]==a} for i in range(m) for a in range(r)]
  assert alpha==r**(m-1);assert len(maxis)==r*m;assert all(x in slices for x in maxis)
  print('Tensor independent-set dictatorship verified',r,m,'maximum sets',len(maxis))
 Fs=[nx.star_graph(3),nx.cycle_graph(3)]
 G,hard=realize(3,Fs)
 assert not colorable(G,3);assert colorable(G,4)
 assert colorable(G,3,[('port',(0,0))])
 print('Explicit family realization checked:',len(G),'vertices',len(G.edges()),'edges; chi4, star center critical, both decorated-host embeddings certified')
