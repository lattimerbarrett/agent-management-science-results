import networkx as nx
import json

def odd_cube(G):
    V=list(G)
    H=nx.Graph(); H.add_nodes_from(V)
    for u in V:
        ends=set()
        for a in G[u]:
            for b in G[a]:
                ends.update(G[b])
        H.add_edges_from((u,v) for v in ends)
    return H

def walk2(G,s):
    return set().union(*(set(G[a]) for a in G[s])) if G.degree(s) else set()

count=0
for G in nx.graph_atlas_g():
    H=odd_cube(G)
    # C3 or C5 exists iff some N_G(v) has an odd-cube edge (including loops).
    good=not any(any(H.has_edge(a,b) for a in G[v] for b in G[v]) for v in G)
    if not good: continue
    count+=1
    for s in G:
        B=walk2(G,s)
        assert not any(G.has_edge(u,v) for u in B for v in B)
        for u in B:
            for a in G[u]:
                for b in G[a]:
                    for v in G[b]:
                        if v in B:
                            assert a not in B and b not in B
                            assert a not in G[s] and b not in G[s]
        R=set(G)-B-set(G[s])-{s}
        for u in R:
            assert set(G[u]).isdisjoint(G[s])
print('Checked structural lemmas on',count,'atlas graphs with no C3,C5 (<=7 vertices).')
open('workspace/agent3_structural_checks.py','w').write(open('scratchpad.py').read())
