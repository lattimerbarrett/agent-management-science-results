import sys
sys.path.insert(0,'workspace')
from agent3_branches import cycle_count,mul
from agent3_exact_cycles import brute
from math import comb
import networkx as nx
from pathlib import Path

def power(p,k):
 q=[1]
 for _ in range(k):q=mul(q,p)
 return q

def paths(G):
 es=list(G.edges());n=len(G);p=[0]*(n+1)
 for mask in range(1<<len(es)):
  F=nx.Graph();F.add_edges_from(es[i] for i in range(len(es)) if mask>>i&1)
  if max(dict(F.degree()).values(),default=0)>2 or (len(F) and not nx.is_forest(F)):continue
  k=nx.number_connected_components(F);left=n-len(F)
  for j in range(left+1):p[k+j]+=2**k*comb(left,j)
 return p
p4=paths(nx.complete_graph(4));p5=paths(nx.complete_graph(5))
print('K4 path polynomial',p4,'K5',p5)
for k in [10,20,40,80,160]:
 m=2*k+1;n=2*m
 S_A=mul(p5,power([1,4,1],(m-5)//2))
 S_B=mul([1,4,1],[comb(m-2,j) for j in range(m-1)])
 T_A=mul([1,1],power([1,4,1],k))
 T_B=mul(mul(p4,[1,4,1]),[comb(m-6,j) for j in range(m-5)])
 cs=cycle_count([S_A,S_B],[m,m],brute(nx.complete_graph(5)))
 ct=cycle_count([T_A,T_B],[m,m],brute(nx.complete_graph(4)))
 assert ct>cs
 print('n',n,'T/S',float(ct/cs),'n(T/S-1)',float(n*(ct-cs)/cs))
