import networkx as nx
from itertools import combinations

def kg(m,k):
    sets=list(combinations(range(m),k)); F=nx.Graph(); F.add_nodes_from(range(len(sets)))
    for a,b in combinations(range(len(sets)),2):
        if set(sets[a]).isdisjoint(sets[b]): F.add_edge(a,b)
    return F,sets

def core(F):
    D=nx.Graph(); D.add_nodes_from((v,i) for v in F for i in range(3))
    for v in F: D.add_edges_from([((v,0),(v,1)),((v,1),(v,2))])
    for u,v in F.edges: D.add_edges_from([((u,2),(v,0)),((v,2),(u,0))])
    return D

def odd_cycle_witness(G,L):
    for start in G:
        def dfs(path):
            if len(path)==L:
                return path if G.has_edge(path[-1],start) else None
            for w in G[path[-1]]:
                if w not in path:
                    z=dfs(path+[w])
                    if z:return z
        z=dfs([start])
        if z:return z

def test(m,k):
    F,sets=kg(m,k); D=core(F)
    for L in (3,5): assert odd_cycle_witness(D,L) is None
    for a in D:
        for b in D[a]:
            for c in D[b]:
                for d in D[c]:
                    if a[1]==d[1]: assert F.has_edge(a[0],d[0]),(a,b,c,d)
    G=D.copy()
    for i in range(3):
        Y=[('y',i,j) for j in range(m)]
        z=('z',i); G.add_edges_from((y,z) for y in Y)
        for v in F:
            G.add_edges_from(((v,i),Y[j]) for j in sets[v])
    for L in (3,5): assert odd_cycle_witness(G,L) is None
    print((m,k),'F',F.number_of_nodes(),F.number_of_edges(),'G',G.number_of_nodes(),G.number_of_edges(),'passed exhaustive C3,C5 and all same-layer 3-walk checks')
for p in [(3,1),(5,2),(7,3)]:
    if p[0]<3*p[1]: test(*p)
