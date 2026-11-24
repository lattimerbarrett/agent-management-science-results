import networkx as nx,z3,json,time
G=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')))
def embeds(G,ac,bc):
 S=z3.Solver();lab={v:z3.Int('l'+str(v)) for v in G};na=len(ac);nb=len(bc)
 for v in G:S.add(lab[v]>=0,lab[v]<=na+nb+1)
 def apart(v):return lab[v]<=na
 for u,v in G.edges():S.add(z3.Or(apart(u)!=apart(v),z3.And(lab[u]==lab[v],lab[u]!=na+1)))
 for v in G:
  nei=[lab[w]==0 for w in G[v]]
  if nei:S.add(z3.Implies(lab[v]==0,z3.PbLe([(q,1) for q in nei],1)))
 for i,c in enumerate(ac,1):S.add(z3.PbLe([(lab[v]==i,1) for v in G],c))
 for i,c in enumerate(bc,na+2):S.add(z3.PbLe([(lab[v]==i,1) for v in G],c))
 return S.check()==z3.sat
