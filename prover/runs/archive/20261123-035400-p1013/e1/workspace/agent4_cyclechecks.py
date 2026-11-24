import math,itertools,json
from fractions import Fraction as F
import networkx as nx

def conv(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def matchpoly(n):
 p=[1]
 for i in range(n//2):p=conv(p,[1,4,1])
 if n%2:p=conv(p,[1,1])
 return p

def starpoly(n):
 p=[math.comb(n,j) for j in range(n+1)]
 for j in range(n-1):p[j+1]+=2*(n-1)*math.comb(n-2,j)
 if n>=3:
  for j in range(n-2):p[j+1]+=(n-1)*(n-2)*math.comb(n-3,j)
 return p

def oneedgepoly(n):return conv([math.comb(n-2,j) for j in range(n-1)],[1,4,1])

def crosscycles(p,q,s,t):
 twice=sum(p[b]*q[b]*math.factorial(b)*math.factorial(b-1) for b in range(1,min(len(p),len(q))))-s*t
 assert twice%2==0
 return twice//2

def brute_poly(g):
 n=len(g); edges=list(g.edges()); p=[0]*(n+1)
 for bits in range(1<<len(edges)):
  j=nx.Graph();j.add_nodes_from(g);j.add_edges_from(e for i,e in enumerate(edges) if bits>>i&1)
  if any(d>2 for v,d in j.degree()) or not nx.is_forest(j):continue
  nontriv=[c for c in nx.connected_components(j) if len(c)>1]
  used=sum(map(len,nontriv));blocks=len(nontriv)
  for k in range(n-used+1):p[blocks+k]+=2**blocks*math.comb(n-used,k)
 return p

def count_cycles(g):
 total=0
 def walk(start,path,used):
  nonlocal total
  last=path[-1]
  if len(path)>=3 and g.has_edge(last,start):total+=1
  for v in g[last]:
   if v>start and v not in used:walk(start,path+[v],used|{v})
 for start in g:walk(start,[start],{start})
 assert total%2==0
 return total//2

for n in range(2,8):
 ma=nx.empty_graph(n);ma.add_edges_from((i,i+1) for i in range(0,n-1,2))
 st=nx.star_graph(n-1)
 oe=nx.empty_graph(n);oe.add_edge(0,1)
 assert brute_poly(ma)==matchpoly(n)
 assert brute_poly(st)==starpoly(n)
 assert brute_poly(oe)==oneedgepoly(n)
for s in range(2,5):
 for t in range(2,5):
  for typ in ['match','star']:
   g=nx.complete_bipartite_graph(s,t)
   if typ=='match':
    g.add_edges_from((i,i+1) for i in range(0,s-1,2))
    g.add_edges_from((s+i,s+i+1) for i in range(0,t-1,2))
    value=crosscycles(matchpoly(s),matchpoly(t),s,t)
   else:
    g.add_edges_from((0,i) for i in range(1,s));g.add_edge(s,s+1)
    value=crosscycles(starpoly(s),oneedgepoly(t),s,t)
   assert count_cycles(g)==value,(s,t,typ)

# Rigorous rational series bounds. I_q(2)=sum_j 1/(j!(j+q)!).
I0_upper=F(9,4)+F(1,36)/(1-F(1,16))
I1_upper=F(19,12)+F(1,144)/(1-F(1,20))
matching_lower=F(2)+F(4)+F(8,3)
assert I0_upper<F(23,10)
assert I1_upper<F(8,5)
assert matching_lower>2*(I0_upper+I1_upper)
print('All block polynomials and small cycle counts independently verified.')
print('Certified matching lower',matching_lower,'>',2*(I0_upper+I1_upper),'hub upper')
for m in [10,20,40,80,160]:
 h=math.factorial(m)**2//2
 mat=crosscycles(matchpoly(m+1),matchpoly(m),m+1,m)
 hub=crosscycles(starpoly(m+1),oneedgepoly(m),m+1,m)
 print('n',2*m+1,'matching/h',mat/h,'hub+edge/h',hub/h,'ratio',mat/hub)

H=nx.Graph();H.add_edges_from([(0,i) for i in [1,2,3,4]]+[(1,2),(2,3),(3,4),(4,1)]+[(1,5),(5,6),(6,1),(3,7),(7,8),(8,3)])
for k in [2,3,4,5]:
 a=b=10
 g=nx.complete_bipartite_graph(a,b)
 hub=a+b;g.add_node(hub);g.add_edges_from((hub,v) for v in range(a+b) if v>=k)
 g.add_edges_from(itertools.combinations(range(k),2))
 print('gadget',k,'extra',k*(k-1)//2-k,'Hcopy',nx.algorithms.isomorphism.GraphMatcher(g,H).subgraph_is_monomorphic())

