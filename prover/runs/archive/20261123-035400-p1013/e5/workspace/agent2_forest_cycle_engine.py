import networkx as nx
from itertools import product
from collections import Counter
from math import comb,factorial
from fractions import Fraction
from pathlib import Path

def forest_stats(G):
 es=list(G.edges()); out=Counter()
 for mask in range(1<<len(es)):
  F=nx.Graph();F.add_edges_from(e for i,e in enumerate(es) if mask>>i&1)
  if max(dict(F.degree()).values(),default=0)>2:continue
  if any(F.subgraph(C).number_of_edges()>=len(C) for C in nx.connected_components(F)):continue
  out[(F.number_of_edges(),nx.number_connected_components(F))]+=1
 return out

def internal_cycles(G):
 ans=0
 for root in G:
  def walk(path):
   z=0
   for v in G[path[-1]]:
    if v==root and len(path)>=3:z+=1
    elif v>root and v not in path:z+=walk(path+[v])
   return z
  ans+=walk([root])
 return ans//2

def full_count(a,b,A,B):
 z=Fraction(internal_cycles(A)+internal_cycles(B))
 for (ea,ra),na in forest_stats(A).items():
  for (eb,rb),nb in forest_stats(B).items():
   va=ea+ra;vb=eb+rb
   lower=max(1,ra,rb)
   if ea+eb==0:lower=2
   for k in range(lower,min(a-va+ra,b-vb+rb)+1):
    x=k-ra;y=k-rb
    if not(0<=x<=a-va and 0<=y<=b-vb):continue
    z+=Fraction(na*nb*2**(ra+rb)*comb(a-va,x)*comb(b-vb,y)*factorial(k)*factorial(k-1),2)
 assert z.denominator==1
 return int(z)

Q=nx.complete_bipartite_graph(3,3);Q.remove_edge(0,3);Q.add_edges_from([(0,6),(6,3)])
K=nx.disjoint_union(nx.complete_graph(3),nx.complete_graph(3))
for n in [13,17,21,31,41,61,101]:
 m=n//2
 q=full_count(m+1,m,Q,nx.empty_graph())
 ext=full_count(m+1,m,K,K)
 print(n,float(Fraction(q,ext)),q>ext)
source=Path('scratchpad.py').read_text();source=source[:source.rfind('