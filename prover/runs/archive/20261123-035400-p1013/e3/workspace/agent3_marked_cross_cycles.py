import sys
sys.path.insert(0,'workspace')
from agent3_branches import cycle_count,mul
from agent3_exact_cycles import brute,join_forests
import networkx as nx
from math import comb,factorial
from itertools import combinations
from pathlib import Path

def poly_mark(G,u):
 n=len(G);es=list(G.edges());p=[0]*(n+1);q=[0]*(n+1)
 for mask in range(1<<len(es)):
  F=nx.Graph();F.add_edges_from(es[i] for i in range(len(es)) if mask>>i&1)
  if max(dict(F.degree()).values(),default=0)>2 or (len(F) and not nx.is_forest(F)):continue
  c=nx.number_connected_components(F);rem=n-len(F);wt=2**c
  for j in range(rem+1):p[c+j]+=wt*comb(rem,j)
  if u in F:
   if F.degree(u)==1:
    for j in range(rem+1):q[c+j]+=wt*comb(rem,j)
  else:
   for j in range(rem):q[c+j+1]+=2*wt*comb(rem-1,j)
 return p,q

def forced_cross(pa,pb):
 ans=sum(pa[l]*pb[l]*factorial(l-1)**2 for l in range(1,min(len(pa),len(pb))))
 assert ans%4==0
 return ans//4-1

def powpoly(p,k):
 q=[1]
 for _ in range(k):q=mul(q,p)
 return q

# Brute-force verification of marked polynomial formula.
checks=0
for a,b in [(2,2),(3,2),(3,3),(4,3)]:
 for FA,FB in [(nx.empty_graph(a),nx.empty_graph(b)),(nx.path_graph(a),nx.empty_graph(b)),(nx.path_graph(a),nx.path_graph(b))]:
  G=join_forests([FA,FB]);base=brute(G)
  for u in FA:
   for v in FB:
    H=G.copy();H.remove_edge(u,a+v)
    pa,qa=poly_mark(FA,u);pb,qb=poly_mark(FB,v)
    x=forced_cross(qa,qb);y=base-brute(H)
    assert x==y,(a,b,u,v,x,y)
    checks+=1
print('Marked cross-edge formula brute verified',checks)

import mpmath as mp
eta=float(mp.besseli(1,2*mp.sqrt(2))/(mp.sqrt(2)*mp.besseli(0,2*mp.sqrt(2))))
print('eta',eta)
for d in [0,1]:
 F=lambda k:mp.mpf(2)**(mp.mpf(k)/2)*mp.besseli(abs(k),2*mp.sqrt(2))
 print('d',d,'eta',F(d-1)/F(d),'theta',F(d+1)/F(d))
for m in [20,40,80,160,320]:
 pa=powpoly([1,4,1],m//2)
 qa=mul([0,4,2],powpoly([1,4,1],m//2-1))
 pb=[comb(m,k) for k in range(m+1)]
 qb=[0]+[2*comb(m-1,k) for k in range(m)]
 c=cycle_count([pa,pb],[m,m]);f=forced_cross(qa,qb)
 scaled=float((f/c-2/m)*m*m)
 print('m',m,'singlehole correction',scaled,'prediction',-4*eta)
