import networkx as nx, z3, json

def cone(G):
 G=nx.convert_node_labels_to_integers(G); n=len(G); G.add_node(n); G.add_edges_from((n,v) for v in range(n)); return G

def fan(k):return cone(nx.disjoint_union_all([nx.path_graph(2) for _ in range(k)]))
def W5():return cone(nx.cycle_graph(4))
def host(a,b,universal=False,one=None,both=False):
 G=nx.complete_bipartite_graph(a,b)
 if one is not None:G.add_edges_from((2*i,2*i+1) for i in range(min(one,a//2)))
 if both:
  G.add_edges_from((2*i,2*i+1) for i in range(a//2));G.add_edges_from((a+2*i,a+2*i+1) for i in range(b//2))
 return cone(G) if universal else G

def embeds(H,G):
 x=[z3.Int('x'+str(i)) for i in H]
 s=z3.Solver();s.add(z3.Distinct(x));s.add(*[z3.And(v>=0,v<len(G)) for v in x])
 for u,v in H.edges():s.add(z3.Or(*[z3.And(x[u]==a,x[v]==b) for a,b in list(G.edges())+[(b,a) for a,b in G.edges()]]))
 return s.check()==z3.sat

results=[]
H=nx.Graph([(0,4),(0,5),(0,6),(0,7),(1,3),(1,7),(2,3),(2,6),(2,7),(4,7),(5,7),(6,7)])
for p,q in [(2,2),(3,1),(3,2),(3,3)]:
 G=nx.complete_bipartite_graph(12,12)
 for base,k in [(0,p),(12,q)]:
  for j in range(12//k):G.add_edges_from((base+j*k+i,base+j*k+i+1) for i in range(k-1))
 print('newH path blocks',p,q,embeds(H,G))
for k in []:
 H=nx.disjoint_union(W5(),fan(k))
 for a,b in [(6,6),(7,6),(8,8)]:
  for kind,G in [('universal_bounded',host(a,b,True,k-1)),('both_matchings',host(a,b,both=True)),('two_universal',cone(host(a,b,True)))]:
   ok=embeds(H,G);assert ok==(kind=='two_universal'),(k,a,b,kind)
   results.append(dict(k=k,a=a,b=b,kind=kind,embeds=ok))
print(json.dumps(results,indent=2))
open('workspace/agent4_construction_checks.json','w').write(json.dumps(results,indent=2))
open('workspace/agent4_construction_checks.py','w').write(open(__file__).read())
