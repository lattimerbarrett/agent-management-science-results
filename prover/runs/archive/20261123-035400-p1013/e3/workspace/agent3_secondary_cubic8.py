import sys
sys.path.insert(0,'workspace')
from agent3_crossdefect_search import embeds
import networkx as nx,itertools as it
from pathlib import Path
cs=[]
for seed in range(300):
 G=nx.random_regular_graph(3,8,seed=seed)
 if nx.is_connected(G) and not any(nx.is_isomorphic(G,H) for H in cs):cs.append(G)
print('connected cubic8 types found',len(cs),flush=True)
for i,G in enumerate(cs):print('Cubic8',i,embeds(0,[8],B_edges=G.edges()),list(G.edges()),flush=True)
# Distinct dense subcubic subgraphs on8 vertices from cubic completions.
subs=[]
for G in cs:
 for k in [1,2,3]:
  for es in it.combinations(list(G.edges()),k):
   H=G.copy();H.remove_edges_from(es)
   if not nx.is_connected(H):continue
   if any(nx.is_isomorphic(H,J) for J in subs):continue
   subs.append(H)
print('dense subcubic8 nonregular types',len(subs),flush=True)
for i,G in enumerate(subs):
 res=embeds(0,[8],B_edges=G.edges())
 if res!='sat':print('ALLOWED secondary8',len(G.edges()),list(G.edges()),res,flush=True)
print('all subcubic8 checks completed')
