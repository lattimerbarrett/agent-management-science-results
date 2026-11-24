import networkx as nx,sys,json
sys.path.insert(0,'workspace');from agent3_packing_host import packing_embedding
res=[]
for k in range(3,8):
 H=nx.Graph();H.add_edges_from([(0,1),(0,2),(0,3),(1,2),(1,3),(3,4)])
 U=list(range(5,k+4));W=list(range(k+4,2*k+2))
 for u in U:H.add_edges_from([(u,0),(u,2)])
 for w in W:H.add_edges_from([(w,0),(w,4)])
 z1=2*k+2;z2=z1+1;H.remove_edge(3,4);H.add_edges_from([(3,z1),(z1,z2),(z2,4),(z1,W[0]),(z2,1)])
 paths=[s for s in range(2,13)if packing_embedding(H,nx.path_graph(s)) is not None]
 stars=[s for s in range(1,12)if packing_embedding(H,nx.star_graph(s)) is not None]
 cycles=[s for s in range(3,13)if packing_embedding(H,nx.cycle_graph(s)) is not None]
 print(k,'n',len(H),'paths',paths,'stars',stars,'cycles',cycles,flush=True)
 res.append(dict(k=k,edges=list(H.edges()),paths=paths,stars=stars,cycles=cycles))
open('workspace/agent4_subdivide_star_family.json','w').write(json.dumps(res,indent=2));open('workspace/agent4_subdivide_star_family.py','w').write(open(__file__).read())
