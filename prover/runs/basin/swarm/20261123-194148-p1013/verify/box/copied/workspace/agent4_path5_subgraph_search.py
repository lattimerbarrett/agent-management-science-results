import networkx as nx,sys,json,time,functools
sys.path.insert(0,'workspace');from agent3_packing_host import packing_embedding
D=json.load(open('workspace/agent4_subdivide_star_family.json'))[0];edges=[tuple(e)for e in D['edges']];n=max(max(e)for e in edges)+1;P=nx.path_graph(5);seen=set();start=time.time();mins=[]
@functools.lru_cache(None)
def free(mask):
 H=nx.Graph();H.add_nodes_from(range(n));H.add_edges_from(e for i,e in enumerate(edges)if mask>>i&1)
 return packing_embedding(H,P) is None
found=None
def search(mask):
 global found
 if mask in seen or found:return
 seen.add(mask)
 H=nx.Graph();H.add_nodes_from(range(n));H.add_edges_from(e for i,e in enumerate(edges)if mask>>i&1)
 if packing_embedding(H,nx.cycle_graph(4)) is not None and packing_embedding(H,nx.cycle_graph(5)) is not None:
  print('FOUND',list(H.edges()),flush=True);found=list(H.edges());return
 children=[mask^(1<<i)for i in range(len(edges))if mask>>i&1 and free(mask^(1<<i))]
 if not children:mins.append(mask)
 for sub in children:search(sub)
search((1<<len(edges))-1)
print('visited',len(seen),'tested',free.cache_info(),'minimal',len(mins),'elapsed',time.time()-start)
open('workspace/agent4_path5_subgraph_search.json','w').write(json.dumps(dict(found=found,visited=len(seen),minimals=len(mins))))
open('workspace/agent4_path5_subgraph_search.py','w').write(open(__file__).read())
