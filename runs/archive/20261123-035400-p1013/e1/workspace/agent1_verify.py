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

# The forbidden graph and finite embedding certificates.
H=nx.Graph([(0,1),(0,2),(0,3),(0,4),(1,2),(2,3),(3,4),(4,1),
            (1,5),(5,6),(6,1),(3,7),(7,8),(8,3)])
assert nx.is_bipartite(H.subgraph([2,4,6,8]))
assert H.subgraph([2,4,6,8]).number_of_edges()==0
assert nx.is_isomorphic(H.subgraph([0,1,3,5,7]),nx.path_graph(5))
assert H.subgraph([1,3]).number_of_edges()==0
assert nx.is_isomorphic(H.subgraph([0,2,4,5,6,7,8]),
                       nx.disjoint_union_all([nx.path_graph(3),nx.path_graph(2),nx.path_graph(2)]))
colors={0:2,1:0,2:1,3:0,4:1,5:1,6:2,7:1,8:2}
assert all(colors[x]!=colors[y] for x,y in H.edges())
assert sum(1 for t in itertools.combinations(H,3) if H.subgraph(t).number_of_edges()==3)>0
for v in H:
    nodes=[u for u in H if u!=v]
    defect=min(sum(bits[nodes.index(x)]==bits[nodes.index(y)]
                   for x,y in H.edges() if v not in (x,y))
               for bits in itertools.product(range(2),repeat=8))
    assert defect>=2
# For rooted hub gadget certificates, 2 denotes the hub image.
# Each entry: label-color map, core internal edges, exceptional core labels,
# hub neighbors among exceptional labels that must be good.
certs=[
 ({0:2,1:1,2:0,3:1,4:0,5:0,6:0,7:0,8:0},
  {(5,6),(7,8)}, {5,6,7,8}, set()),
 ({0:0,1:2,2:1,3:0,4:1,5:0,6:1,7:0,8:1},
  {(0,3),(3,7)}, {0,3,7}, {0}),
 ({0:2,1:0,2:1,3:0,4:1,5:0,6:1,7:1,8:1},
  {(1,5),(7,8)}, {1,5,7,8}, {1}),
]
for col,edges,exc,required in certs:
    root=next(v for v in col if col[v]==2)
    actual={tuple(sorted((x,y))) for x,y in H.edges()
            if root not in (x,y) and col[x]==col[y]}
    assert actual==edges
    assert {v for v in exc if H.has_edge(root,v)}==required
    # No cross-edge between distinct exceptional labels is required.
    assert not any(x in exc and y in exc and col[x]!=col[y] for x,y in H.edges())
print('Forbidden-graph partitions, colorings, bipartization defects, and all hub certificates verified.')
