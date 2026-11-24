import networkx as nx,json,time
G=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')));V=set(G);best=999;ct=0

def check(B):
 global best,ct
 ct+=1;A=V-set(B);a=G.subgraph(A);req=sum(len(c) for c in nx.connected_components(a) if len(c)>=3);best=min(best,req)
for I in nx.find_cliques(nx.complement(G)):check(I)
for u,v in G.edges():
 U=V-{u,v}-set(G[u])-set(G[v])
 for I in nx.find_cliques(nx.complement(G.subgraph(U))):check(set(I)|{u,v})
assert best==6,(best,ct)
print('PASS: exhaustive maximal B sets inducing <=1 edge:',ct,'minimum primary-clique requirement:',best)
