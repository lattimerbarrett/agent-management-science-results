import itertools, json
import networkx as nx

def target(k):
    V=[(a,S) for a in range(k) for S in range(1,1<<k) if not S>>a&1]
    H=nx.Graph(); H.add_nodes_from(V)
    for (a,S),(b,T) in itertools.combinations(V,2):
        if T>>a&1 and S>>b&1 and not S&T: H.add_edge((a,S),(b,T))
    return H

def odd_cube(G):
    X=G.copy()
    for a in G:
        for b in G[a]:
            for c in G[b]:
                for d in G[c]: X.add_edge(a,d)
    return X

def check_map(G,color):
    f={v:(color[v],sum(1<<c for c in set(color[w] for w in G[v]))) for v in G}
    for a,S in f.values(): assert not S>>a&1
    for v,w in G.edges():
        a,S=f[v];b,T=f[w]
        assert T>>a&1 and S>>b&1 and not S&T
    return True

def run_checks():
    report={}
    for k in range(1,8):
        H=target(k)
        assert len(H)==k*((1<<(k-1))-1)
        assert sum(nx.triangles(H).values())==0
        report[k]={'vertices':len(H),'edges':H.number_of_edges(),'triangles':0}
    count=0
    for G in nx.graph_atlas_g():
        if not G or min(dict(G.degree()).values())==0: continue
        X=odd_cube(G)
        if nx.number_of_selfloops(X): continue
        col=nx.coloring.greedy_color(X,strategy='largest_first')
        check_map(G,col); count+=1
    return {'targets':report,'atlas_graph_homomorphisms_checked':count}

if __name__=='__main__': print(json.dumps(run_checks(),indent=2))
