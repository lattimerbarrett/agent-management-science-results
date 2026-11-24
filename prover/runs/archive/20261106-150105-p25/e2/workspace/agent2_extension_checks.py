import networkx as nx
from itertools import combinations, product

def oddcube(G):
    X=nx.Graph(); X.add_nodes_from(G)
    for u in G:
        for a in G[u]:
            X.add_edge(u,a)
            for b in G[a]:
                for v in G[b]: X.add_edge(u,v)
    return X

def check():
    cases=0
    for G in nx.graph_atlas_g():
        if not G: continue
        X=oddcube(G)
        if nx.number_of_selfloops(X): continue
        V=list(G)
        # Each N(s) is an independent oddcube-colored core with one color.
        # Include unions of up to two such classes, colored by first covering center.
        cores=[()] + [(s,) for s in V]+list(combinations(V,2))
        for centers in cores:
            col={}
            for i,s in enumerate(centers):
                for x in G[s]: col.setdefault(x,i)
            if any(col[u]==col[v] for u,v in X.edges if u in col and v in col): continue
            A=set(col); U=set(G)-A
            P={v:frozenset(col[x] for x in G[v] if x in A) for v in U}
            for u,v in G.edges:
                if u in U and v in U: assert not P[u]&P[v]
            for u in U:
                for a in G[u]:
                    for b in G[a]:
                        for v in G[b]:
                            if v in U and P[u]==P[v]: assert a not in A and b not in A
            cases+=1
    print('Verified extension-profile lemma on',cases,'atlas graph/core instances.')

if __name__=='__main__':
    check()
    from pathlib import Path
    Path('workspace/agent2_extension_checks.py').write_text(Path(__file__).read_text())
