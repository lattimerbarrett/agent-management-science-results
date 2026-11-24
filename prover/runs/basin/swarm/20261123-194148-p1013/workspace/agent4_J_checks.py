import networkx as nx,z3,json

def cone(G):
 G=nx.convert_node_labels_to_integers(G);n=len(G);G.add_node(n);G.add_edges_from((n,u) for u in range(n));return G

def embeds(H,G):
 x=[z3.Int('x'+str(i)) for i in H];s=z3.Solver();s.add(z3.Distinct(x));s.add(*[z3.And(v>=0,v<len(G)) for v in x]);es=list(G.edges());es+= [(b,a) for a,b in es]
 for u,v in H.edges():s.add(z3.Or(*[z3.And(x[u]==a,x[v]==b) for a,b in es]))
 ok=s.check()==z3.sat
 return ok,([s.model().eval(v).as_long() for v in x] if ok else None)
J=cone(nx.disjoint_union(cone(nx.cycle_graph(4)),cone(nx.path_graph(4))))
res=[]
for active in [0,1,2,3]:
 G=nx.complete_multipartite_graph(6,6,6)
 for j in range(active):G.add_edges_from((6*j+2*i,6*j+2*i+1) for i in range(3))
 ans,wit=embeds(J,G); assert ans==(active==3)
 res.append(dict(active=active,embedding=ans,witness=wit))
G=nx.complete_multipartite_graph(6,6,6);G.add_edges_from([(0,1),(0,2)])
ans,wit=embeds(J,G);assert ans;res.append(dict(P3=True,embedding=ans,witness=wit))
print(json.dumps(res,indent=2))
open('workspace/agent4_J_checks.json','w').write(json.dumps(res,indent=2))
open('workspace/agent4_J_checks.py','w').write(open(__file__).read())
