import itertools, networkx as nx, json, os

def shift_graph(N,k):
    vs=list(itertools.combinations(range(N),k))
    G=nx.Graph(); G.add_nodes_from(vs)
    for a in itertools.combinations(range(N),k+1): G.add_edge(a[:-1],a[1:])
    return G

def cover_set(vertices,order):
    rank={x:i for i,x in enumerate(order)}
    return {v for v in vertices if (lambda j: 0<j<len(v)-1 and j%2==0)(max(range(len(v)),key=lambda j:rank[v[j]]))}

def check(N,k):
    F=shift_graph(N,k); counts=dict.fromkeys(F,0); m=0
    for order in itertools.permutations(range(N)):
        A=cover_set(F,order); m+=1
        assert all(not(u in A and v in A) for u,v in F.edges())
        for v in A: counts[v]+=1
    expected=m*(k//2-1)//k
    assert set(counts.values())=={expected}
    # Verify extension-set coloring is proper from a proper greedy coloring.
    color=nx.coloring.greedy_color(F,strategy='largest_first')
    lower=shift_graph(N,k-1)
    C={a:frozenset(color[a+(b,)] for b in range(a[-1]+1,N)) for a in lower}
    assert all(C[u]!=C[v] for u,v in lower.edges())
    return {'N':N,'k':k,'vertices':len(F),'edges':F.number_of_edges(),'permutations':m,'coverage':expected,'fraction':str(expected)+'/'+str(m),'extension_coloring_verified':True}

if __name__=='__main__':
    results=[check(5,4),check(6,4),check(7,4),check(8,6)]
    print(json.dumps(results,indent=2))
