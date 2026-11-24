import networkx as nx, itertools, json, os

def subdivision3(F):
    G=nx.Graph(); G.add_nodes_from(('v',v) for v in F)
    for j,(u,v) in enumerate(F.edges()):
        G.add_edges_from([(('v',u),('a',j)),(('a',j),('b',j)),(('b',j),('v',v))])
    return G

def odd_walk_graph(G):
    W=nx.Graph(); W.add_nodes_from(G)
    for u in G:
        reach=set(G[u])
        for a in G[u]:
            for b in G[a]: reach.update(G[b])
        if u in reach: raise ValueError('triangle/odd short closed walk')
        W.add_edges_from((u,v) for v in reach)
    return W

def has_cycle(G,k):
    def search(path):
        if len(path)==k:return G.has_edge(path[-1],path[0])
        return any(search(path+[v]) for v in G[path[-1]] if v not in path)
    return any(search([s]) for s in G)

def profile_target(G,col):
    typ={u:(col[u],frozenset(col[v] for v in G[u])) for u in G}
    H=nx.Graph(); H.add_nodes_from(typ.values())
    H.add_edges_from((typ[u],typ[v]) for u,v in G.edges())
    assert nx.number_of_selfloops(H)==0
    return H,typ

