"""Checked boundary construction ingredients; does not prove exact Turan structure."""
import math,itertools,networkx as nx
from agent1_cycles import path_polynomial,power,cycles_join_r3

def base_graph():
 g=nx.Graph();g.add_nodes_from(range(6));g.add_edges_from([(0,3),(0,4),(0,5),(1,2),(1,4),(1,5),(2,3),(2,4),(3,4)])
 return g

def lifted_graph(r,M):
 h=base_graph();start=6
 for j in range(r-2):
  old=list(h);new=list(range(start,start+M));start+=M
  h.add_nodes_from(new);h.add_edges_from((u,v) for u in old for v in new)
 return h

def star_poly(L):
 # empty center case: arbitrary subset of L-1 leaves; selected center
 # may have 0,1,2 selected incident edges in a path forest.
 from agent1_cycles import mul
 q=power([1,1],L)
 for deg in range(1,min(2,L-1)+1):
  orient=2
  base=[0,orient*math.comb(L-1,deg)]
  more=power([1,1],L-1-deg)
  terms=mul(base,more)
  for i,x in enumerate(terms):q[i]+=x
 return q

def run_checks():
 s=base_graph()
 assert all(not nx.is_bipartite(nx.subgraph(s,[v for v in s if v!=u])) for u in s)
 # Verify every 2-host assignment of F6 forces either internal triangle/P4
 # (one host independent).
 checked=0
 for mask in range(1<<6):
  A=[v for v in s if mask>>v&1];B=[v for v in s if not mask>>v&1]
  if s.subgraph(B).number_of_edges():continue
  f=s.subgraph(A)
  triangle=any(len(c)==3 for c in nx.enumerate_all_cliques(f))
  p4=any(all(f.has_edge(p[i],p[i+1]) for i in range(3)) for p in itertools.permutations(A,4))
  assert triangle or p4
  checked+=1
 assert not s.has_edge(4,5)
 assert nx.is_bipartite(s.subgraph([0,1,2,3]))
 assert set(s.subgraph([0,2,4,5]).edges())=={(0,4),(0,5),(2,4)}
 assert s.subgraph([2,3,4]).number_of_edges()==3
 # Defective 2-coloring: each side induces one edge and an isolated vertex.
 assert s.subgraph([0,1,2]).number_of_edges()==1
 assert s.subgraph([3,4,5]).number_of_edges()==1
 for L in range(2,12):
  assert star_poly(L)==path_polynomial(L,[(0,j) for j in range(1,L)])
 # Exact rational-free construction inequality from log integral bound.
 for r in range(3,1001):
  L=2*r;s=r-1
  assert 2*(1-1/L)/s>2*math.log1p(1/s)
 print('F6 partitions checked:',checked,'; star polynomial identities:10; log inequalities:998')
 for k in (1,2,4,6,8,10):
  m=6*k;n=3*m
  q=power(star_poly(6),k);qbig=star_poly(m);iso=power([1,1],m)
  small=cycles_join_r3(q,iso,iso,(m,m,m))
  big=cycles_join_r3(qbig,iso,iso,(m,m,m))
  print('n=',n,'bounded-star cycles=',small,'universal cycles=',big,'ratio=',float(small/big))
  if k==10:assert small>big
if __name__=='__main__':run_checks()
