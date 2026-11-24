import networkx as nx,z3,json,time
H=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')))
def embeds_holes(H,a,b,f,holes):
 # rare Aclique a, Brare clique b then f matchingedges. Core Ac=-1,Bc=0
 q=a+b+2*f;AA=set(range(1,a+1));BB=set(range(a+1,q+1));F=nx.Graph();F.add_nodes_from(range(1,q+1));F.add_edges_from((i,j) for i in AA for j in AA if i<j);F.add_edges_from((i,j) for i in range(a+1,a+b+1) for j in range(i+1,a+b+1));F.add_edges_from((a+b+2*t+1,a+b+2*t+2) for t in range(f));F.add_edges_from((i,j) for i in AA for j in BB if (i,j) not in holes)
 S=z3.Solver();lab={v:z3.Int('z'+str(v)) for v in H}
 for v in H:S.add(lab[v]>=-1,lab[v]<=q)
 for p in range(1,q+1):S.add(z3.PbLe([(lab[v]==p,1) for v in H],1))
 def A(x):return z3.Or(x==-1,z3.And(x>=1,x<=a))
 good=list(F.edges());good +=[(v,u) for u,v in good]
 for u,v in H.edges():
  x,y=lab[u],lab[v]
  S.add(z3.Or(z3.And(x==-1,y==-1),z3.And(A(x)!=A(y),z3.Or(x<=0,y<=0)),*[z3.And(x==i,y==j) for i,j in good]))
 for v in H:
  ns=[lab[w]==-1 for w in H[v]]
  if ns:S.add(z3.Implies(lab[v]==-1,z3.PbLe([(x,1) for x in ns],1)))
 return S.check()==z3.sat
