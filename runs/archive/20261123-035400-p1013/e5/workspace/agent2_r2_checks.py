import networkx as nx
from itertools import combinations
from pathlib import Path
from fractions import Fraction
from math import factorial

def matching(G):return len(nx.max_weight_matching(G,maxcardinality=True))
def active(G):return G.subgraph([v for v in G if G.degree(v)]).copy()
def embeds(G,P):
 P=active(P)
 return len(P)==0 or nx.algorithms.isomorphism.GraphMatcher(G,P).subgraph_is_monomorphic()
F=nx.Graph()
for i in range(4):F.add_edges_from([(0,1+2*i),(0,2+2*i),(1+2*i,2+2*i)])
Q=nx.complete_bipartite_graph(3,3);Q.remove_edge(0,3);Q.add_edges_from([(0,6),(6,3)])
K=nx.disjoint_union(nx.complete_graph(3),nx.complete_graph(3))
assert Q.number_of_edges()==10 and max(dict(Q.degree()).values())==3 and matching(Q)==3
assert K.number_of_edges()==6 and matching(K)==2 and max(dict(K.degree()).values())==2
valid=[]
for mask in range(256):
 color={0:0,**{i+1:(mask>>i)&1 for i in range(8)}}
 forced=21*sum(color[1+2*i]!=color[1+2*j] or False for i,j in combinations(range(3),2))
 forced+=21*sum(color[2+2*i]!=color[2+2*j] for i,j in combinations(range(3),2))
 if forced>20:continue
 mono=[]
 for side in [0,1]:
  M=F.subgraph([v for v in F if color[v]==side]).copy()
  mono.append(M)
 assert not(embeds(K,mono[0]) and embeds(K,mono[1]))
 assert not(embeds(Q,mono[0]) and embeds(nx.empty_graph(),mono[1]))
 assert not(embeds(nx.empty_graph(),mono[0]) and embeds(Q,mono[1]))
 # Necessary local constraint certificate for every remaining leaf coloring.
 d=[max(dict(M.degree()).values(),default=0) for M in mono]
 nu=[matching(M) for M in mono]
 if max(d+nu)<=3:
  A,B=mono
  dv=A.degree(0) if 0 in A else 0
  assert (dv>=1 and nu[1]>=3) or (dv>=3 and B.number_of_edges()>=1)
 valid.append(mask)
print('all 256 compressed colorings checked;',len(valid),'have connector cost<=20')
for b in range(8):assert 7+b-(b+2)//3<=11
for a1 in range(21):
 for a2 in range(21):
  for a3 in range(21):assert 2*(a1+a2+3*a3)>=a1+2*a2+3*a3
print('deletion-bound integer inequalities checked')
I0=sum(Fraction(1,factorial(j)**2) for j in range(30))
I2=sum(Fraction(1,factorial(j)*factorial(j+2)) for j in range(30))
assert I2<I0/2
print('Bessel truncated sums',float(I0),float(I2),'positive gap',float(4*I0-6*I2))
