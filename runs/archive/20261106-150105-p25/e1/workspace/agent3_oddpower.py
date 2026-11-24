"""Exact utilities for the odd-third-power reduction; no dependencies."""
from itertools import combinations, product

def odd_third_power(adj):
    n=len(adj)
    out=[set(a) for a in adj]
    for u in range(n):
        for x in adj[u]:
            for y in adj[x]:
                out[u].update(adj[y])
    return out

def universal_target(t):
    vertices=[(i,frozenset(j for j in range(t) if mask>>j&1))
              for i in range(t) for mask in range(1<<t) if not (mask>>i&1)]
    adj=[set() for _ in vertices]
    for a,b in combinations(range(len(vertices)),2):
        i,A=vertices[a];j,B=vertices[b]
        if i in B and j in A and not A&B:
            adj[a].add(b);adj[b].add(a)
    return vertices,adj

def has_triangle(adj):
    return any(adj[u]&adj[v] for u in range(len(adj)) for v in adj[u])

def is_hom(adj,target,mapping):
    return all(mapping[v] in target[mapping[u]] for u in range(len(adj)) for v in adj[u])

def induced_map(adj,colors,t):
    vertices,target=universal_target(t)
    lookup={v:i for i,v in enumerate(vertices)}
    mapping=[lookup[(colors[v],frozenset(colors[w] for w in adj[v]))] for v in range(len(adj))]
    assert is_hom(adj,target,mapping)
    return mapping

def checks(max_n=6):
    counts={}
    for t in range(1,7):
        vertices,adj=universal_target(t)
        assert len(vertices)==t*2**(t-1)
        assert not has_triangle(adj)
    for n in range(1,max_n+1):
        pairs=list(combinations(range(n),2)); good=0;maps=0
        for mask in range(1<<len(pairs)):
            adj=[set() for _ in range(n)]
            for i,(u,v) in enumerate(pairs):
                if mask>>i&1:adj[u].add(v);adj[v].add(u)
            F=odd_third_power(adj)
            # A loop in F is precisely a triangle in a simple G.
            if any(u in F[u] for u in range(n)):continue
            # N(v) independent in F is precisely no C3 or C5.
            if any(F[x]&adj[v] for v in range(n) for x in adj[v]):continue
            good+=1
            for colors in product(range(3),repeat=n):
                if any(colors[u]==colors[v] for u in range(n) for v in F[u]):continue
                induced_map(adj,colors,3);maps+=1
        counts[n]=(good,maps)
    return counts

if __name__=='__main__':print(checks())
