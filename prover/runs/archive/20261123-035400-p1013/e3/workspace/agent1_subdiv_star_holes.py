import networkx as nx,z3,json
H=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')))
def embedABholes(H,FA,FB,holes):
 a=len(FA);b=len(FB);q=a+b;RA=nx.convert_node_labels_to_integers(FA,first_label=1);RB=nx.convert_node_labels_to_integers(FB,first_label=a+1);F=nx.compose(RA,RB);F.add_edges_from((i,j) for i in RA for j in RB if (i-1,j-a-1) not in holes)
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

from itertools import combinations

def subdivstar(d):
 G=nx.Graph();G.add_nodes_from(range(2*d+1))
 for i in range(d):G.add_edges_from([(0,i+1),(i+1,d+i+1)])
 return G

if __name__=='__main__':
 out=[]
 B=nx.disjoint_union(nx.complete_graph(4),nx.path_graph(2))
 for d in range(3,6):
  A=subdivstar(d)
  for h in range(0,d-1):
   for hc in range(max(0,h-2),min(4,h)+1):
    he=h-hc
    holes={(0,j) for j in list(range(hc))+list(range(4,4+he))}
    found=embedABholes(H,A,B,holes)
    row=dict(d=d,holes=h,hc=hc,he=he,Hembeds=found,edgebonus=d+7-h)
    print(row,flush=True);out.append(row)
 json.dump(out,open('workspace/agent1_subdiv_star_holes_results.json','w'),indent=2)
