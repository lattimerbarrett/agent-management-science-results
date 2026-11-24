import networkx as nx,json,z3
from pathlib import Path
G=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')))
vs=list(G);x={v:z3.Bool('A'+str(i)) for i,v in enumerate(vs)};c={v:z3.Bool('C'+str(i)) for i,v in enumerate(vs)}
S=z3.Solver();S.add(z3.PbEq([(c[v],1) for v in G],1))
for v in G:
 S.add(z3.Implies(c[v],z3.Not(x[v])))
 nei=[x[w] for w in G[v]]
 if nei:S.add(z3.Implies(x[v],z3.PbLe([(b,1) for b in nei],1)))
for u,v in G.edges():S.add(z3.Or(x[u],x[v],c[u],c[v]))
b=[z3.And(z3.Not(x[u]),z3.Not(x[v])) for u,v in G.edges()]
for d in range(1,25):
 S.push();S.add(z3.PbLe([(q,1) for q in b],d));res=S.check()
 print('minsecondarypurestar edges<=',d,res,flush=True)
 S.pop()
 if res==z3.sat:break
