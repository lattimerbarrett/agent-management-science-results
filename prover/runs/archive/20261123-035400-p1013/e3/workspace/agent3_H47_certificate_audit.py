import networkx as nx,z3,json,itertools as it
from pathlib import Path
G=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')))

def audit(A,B,holes=False):
 a=len(A);b=len(B);L=2+a+b
 edges=set()
 for x,y in it.product(range(L),repeat=2):
  ax=x==0 or 2<=x<2+a;ay=y==0 or 2<=y<2+a
  if ax!=ay:
   if not(holes and x>=2 and y>=2):edges.add((x,y))
  elif x==y==0:edges.add((x,y))
  elif 2<=x<2+a and 2<=y<2+a and A.has_edge(x-2,y-2):edges.add((x,y))
  elif x>=2+a and y>=2+a and B.has_edge(x-2-a,y-2-a):edges.add((x,y))
 S=z3.Solver();S.set(timeout=10000);vs=list(G);X={v:z3.Int('x'+str(i)) for i,v in enumerate(vs)}
 for v in G:S.add(X[v]>=0,X[v]<L)
 for u,v in G.edges():S.add(z3.Or(*[z3.And(X[u]==x,X[v]==y) for x,y in edges]))
 for v in G:
  if G.degree(v):S.add(z3.Implies(X[v]==0,z3.PbLe([(X[w]==0,1) for w in G[v]],1)))
 for j in range(2,L):S.add(z3.PbLe([(X[v]==j,1) for v in G],1))
 res=S.check()
 if res!=z3.sat:return str(res),None
 model=S.model();lab={v:model.eval(X[v]).as_long() for v in G}
 # Build a genuine finite simple host and injective embedding.
 H=nx.Graph();AC=[];BC=[]
 for k in range(len(G)):
  u=('pair',k,0);v=('pair',k,1);AC +=[u,v];H.add_edge(u,v)
 for k in range(len(G)):BC.append(('isolatedB',k));H.add_node(BC[-1])
 for u in A:H.add_node(('A',u));AC.append(('A',u))
 for u in B:H.add_node(('B',u));BC.append(('B',u))
 H.add_edges_from((('A',u),('A',v)) for u,v in A.edges());H.add_edges_from((('B',u),('B',v)) for u,v in B.edges())
 H.add_edges_from((u,v) for u in AC for v in BC if not(holes and u[0]=='A' and v[0]=='B'))
 M={};k=0
 for C in nx.connected_components(G.subgraph([v for v in G if lab[v]==0])):
  assert len(C)<=2
  for j,v in enumerate(C):M[v]=('pair',k,j)
  k+=1
 k=0
 for v in G:
  if lab[v]==1:M[v]=('isolatedB',k);k+=1
  elif 2<=lab[v]<2+a:M[v]=('A',lab[v]-2)
  elif lab[v]>=2+a:M[v]=('B',lab[v]-2-a)
 assert len(M)==len(G) and len(set(M.values()))==len(G)
 assert all(H.has_edge(M[u],M[v]) for u,v in G.edges())
 return 'sat',{'map':[[list(u),list(v)] for u,v in M.items()],'host_edges':len(H.edges()),'host_vertices':len(H)}

print('H size',len(G),len(G.edges()),'bipartite',nx.is_bipartite(G),'critical',[v for v in G if nx.is_bipartite(G.subgraph(set(G)-{v}))],flush=True)
cases=[('A2P3',nx.disjoint_union(nx.path_graph(3),nx.path_graph(3)),nx.empty_graph(0),False),('B2P3',nx.empty_graph(0),nx.disjoint_union(nx.path_graph(3),nx.path_graph(3)),False),('Astar7',nx.star_graph(6),nx.empty_graph(0),False),('Bstar4',nx.empty_graph(0),nx.star_graph(4),False),('P3_P3_holes',nx.path_graph(3),nx.path_graph(3),True),('P3_3Bedges_holes',nx.path_graph(3),nx.disjoint_union_all([nx.path_graph(2)]*3),True),('S_free',nx.complete_graph(5),nx.path_graph(2),False),('T_free',nx.empty_graph(0),nx.disjoint_union(nx.complete_graph(4),nx.path_graph(2)),False)]
out={}
for name,A,B,holes in cases:
 res,cert=audit(A,B,holes);print(name,res,flush=True);out[name]={'status':res,'certificate':cert}
 Path('workspace/agent3_H47_audited_certificates.json').write_text(json.dumps(out))
Path('workspace/agent3_H47_audited_certificates.json').write_text(json.dumps(out))
