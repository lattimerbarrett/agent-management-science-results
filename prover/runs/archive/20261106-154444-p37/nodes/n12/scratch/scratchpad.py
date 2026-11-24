from itertools import product
import networkx as nx
for sizes in [(2,2,2,2,3),(2,2,2,3),(2,2,3),(3,3,2),(3,3,3),(2,2,2,2,2,2)]:
 blocks=[];s=0
 for a in sizes:blocks.append(((1<<a)-1)<<s);s+=a
 full=(1<<s)-1
 rows=[x for x in range(1<<s) if x&1 and all(x&b and (full^x)&b for b in blocks)]
 G=nx.Graph();G.add_nodes_from(rows)
 for i,a in enumerate(rows):
  for b in rows[i+1:]:
   if a&b and a&(full^b) and (full^a)&b and (full^a)&(full^b):G.add_edge(a,b)
 best=max(nx.find_cliques(G),key=len)
 print(sizes,len(rows),len(best),flush=True)
