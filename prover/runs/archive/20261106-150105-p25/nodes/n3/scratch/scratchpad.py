import networkx as nx
for r in range(1, 7):
    p, q = 5*r+2, 2*r+1
    G = nx.Graph()
    G.add_nodes_from(range(p))
    G.add_edges_from((i,j) for i in range(p) for j in range(i+1,p) if q <= j-i <= p-q)
    # Use circular labels on C5: labels differing by 2 or 3 are adjacent.
    f = {i: (5*i)//p for i in G}
    maps_to_pentagon = all((f[u]-f[v]) % 5 in (2,3) for u,v in G.edges())
    def has_cycle(k):
        def extend(path):
            if len(path)==k:
                return G.has_edge(path[-1],path[0])
            return any(extend(path+[w]) for w in G[path[-1]] if w>path[0] and w not in path)
        return any(extend([v]) for v in G)
    print({'r':r, 'n':p, 'degree':min(dict(G.degree()).values()), 'C3':has_cycle(3), 'C5':has_cycle(5), 'maps_to_C5':maps_to_pentagon})
