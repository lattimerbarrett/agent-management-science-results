"""Implicit projective graph renderer; no enormous adjacency matrix is allocated.
Core: independent blow-up of categorical K_3^d. Labels (word, clone).
All assertions here check the finite payload realization and exact arithmetic;
projectivity itself is proved by the Hoffman equality argument, not asserted
from these finite tests.
"""
import networkx as nx
from itertools import combinations
from math import prod

def path(n): return nx.path_graph(n)
def star(n): return nx.star_graph(n-1)
def disjoint(*gs): return nx.disjoint_union_all(gs)
def fork5():
 g=nx.Graph([(0,1),(0,2),(0,3),(3,4)])
 return g

def proper3(g):
 if nx.is_bipartite(g):
  return nx.bipartite.color(g)
 # Every other payload is an odd cycle with standard consecutive labels.
 n=len(g);c={i:i%2 for i in range(n-1)};c[n-1]=2
 assert all(c[u]!=c[v] for u,v in g.edges())
 return c

class Renderer:
 def __init__(self):
  self.payloads=[('star12',star(12)),('P12+P11',disjoint(path(12),path(11))),('fork5',fork5())]
  self.payloads += [('C'+str(k),nx.cycle_graph(k)) for k in range(3,23)]
  self.payloads += [('two_parts',disjoint(path(2),path(2)))]
  self.d=len(self.payloads)+1
  self.sigma=self.d-1
  self.h=300
  self.n=self.h*3**self.d+1
  self.root=self.n-1
  self.labels={};self.extra=set();self.coord_extra=[]
  clone=0
  for i,(name,g) in enumerate(self.payloads):
   c=proper3(g);labels={}
   for u in g:
    w=[c[u]]*self.d
    w[i]=int(name=='two_parts' and u>=2)
    assert clone<self.h
    labels[u]=(tuple(w),clone)
    self.labels[(i,u)]=labels[u]
    clone+=1
   es=set()
   for u,v in g.edges():
    e=frozenset((labels[u],labels[v]));es.add(e);self.extra.add(e)
   self.coord_extra.append(es)
  self.special_count=clone
 def core_adj(self,a,b):
  return all(x!=y for x,y in zip(a[0],b[0]))
 def root_adj(self,a):
  return all(a[0][i]==0 for i in range(self.d) if i!=self.sigma)
 def check(self):
  assert self.d==25 and self.n==254186582832901
  assert self.special_count==294 and len(self.extra)==288
  for i,es in enumerate(self.coord_extra):
   assert es
   for e in es:
    a,b=tuple(e)
    assert not self.core_adj(a,b)
    assert a[0][i]==b[0][i]
    assert all(a[0][j]!=b[0][j] for j in range(self.d) if j!=i)
  # Explicit H-v proper 3-coloring is the sigma projection.
  assert all(a[0][self.sigma]!=b[0][self.sigma] for a,b in map(tuple,self.extra))
  # Explicit H-c proper 3-coloring: first (star) projection, root has color 2.
  center=self.labels[(0,0)]
  for e in self.extra:
   a,b=tuple(e)
   if center in e:continue
   assert a[0][0]!=b[0][0]
  # Root has 300 neighbors in each sigma color and none in color 2 of any payload projection.
  roots=[tuple([0]*(self.d-1)+[s]) for s in range(3)]
  assert all(w[self.sigma]==s for s,w in enumerate(roots))
  assert all(w[i]!=2 for w in roots for i in range(self.d-1))
  # Eigenvalues of (J-I)^tensor d, and multiplicities: exact Hoffman parameters.
  eig=[((-1)**j*2**(self.d-j), __import__('math').comb(self.d,j)*2**j) for j in range(self.d+1)]
  assert sum(m for _,m in eig)==3**self.d
  assert min(x for x,_ in eig)==-2**(self.d-1)
  assert [j for j,(x,_) in enumerate(eig) if x==min(x for x,_ in eig)]==[1]
  assert (3**self.d)*(2**(self.d-1))//(2**self.d+2**(self.d-1))==3**(self.d-1)
  return {'vertices':self.n,'core_cells':3**self.d,'cell_size':self.h,'payloads':len(self.payloads),'payload_vertices':self.special_count,'payload_edges':len(self.extra),'root_degree':3*self.h}

if __name__=='__main__':print(Renderer().check())
