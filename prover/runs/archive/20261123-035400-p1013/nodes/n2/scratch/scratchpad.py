import networkx as nx

def cycles(G):
    n=len(G); total=0
    adj=[set(G[i]) for i in range(n)]
    for s in range(n):
        dp={(1<<s,s):1}
        for mask in range(1<<s,1<<n):
            if not(mask>>s&1) or mask&((1<<s)-1):continue
            for v in range(s,n):
                val=dp.get((mask,v),0)
                if not val:continue
                if mask.bit_count()>=3 and s in adj[v]:total+=val
                for w in adj[v]:
                    if w>s and not(mask>>w&1):
                        k=(mask|(1<<w),w);dp[k]=dp.get(k,0)+val
    return total//2

def graph(a,b,matching_sides=(),extra=False):
    G=nx.complete_bipartite_graph(a,b)
    for side in matching_sides:
        vertices=list(range(a)) if side==0 else list(range(a,a+b))
        G.add_edges_from(zip(vertices[::2],vertices[1::2]))
    if extra:G.add_edge(0,1)
    return G

for n in [8,12]:
    for label,G in [('bipartite',graph(n//2,n//2)),('one extra edge',graph(n//2,n//2,extra=True)),('matchings, balanced',graph(n//2,n//2,(0,1))),('matchings, unbalanced',graph(n//2+1,n//2-1,(0,1)))]:
        print(n,label,'edges=',G.number_of_edges(),'cycles=',cycles(G))
