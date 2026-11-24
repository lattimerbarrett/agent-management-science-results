"""Exact finite cycle counters; all arithmetic integer/rational.
Path-forest contraction formula for a join of an arbitrary graph and an independent set.
"""
import math
from fractions import Fraction

def poly_mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c

def path_forest_poly(G):
    """Exponential in vertices+edges; suitable for bounded components."""
    vs=list(G); n=len(vs); idx={v:i for i,v in enumerate(vs)}
    edges=[(idx[u],idx[v]) for u,v in G.edges()]
    p=[0]*(n+1)
    for sm in range(1<<n):
        es=[(u,v) for u,v in edges if sm>>u&1 and sm>>v&1]
        for em in range(1<<len(es)):
            parent=list(range(n)); degree=[0]*n; good=True; ec=0
            def root(v):
                while parent[v]!=v: v=parent[v]
                return v
            for j,(u,v) in enumerate(es):
                if em>>j&1:
                    degree[u]+=1; degree[v]+=1
                    ru,rv=root(u),root(v)
                    if degree[u]>2 or degree[v]>2 or ru==rv:
                        good=False; break
                    parent[ru]=rv; ec+=1
            if good:
                comp=sm.bit_count()-ec
                nontrivial=len({root(v) for v in range(n) if degree[v]})
                p[comp]+=2**nontrivial
    return p

def cycles_bruteforce(G):
    """Count each simple undirected cycle by unique least vertex and orientation."""
    vs=list(G); index={v:i for i,v in enumerate(vs)}
    adj=[{index[w] for w in G[v]} for v in vs]; total=0
    for start in range(len(vs)):
        def dfs(v,seen,length):
            nonlocal total
            for w in adj[v]:
                if w==start and length>=3: total+=1
                elif w>start and not (seen>>w&1): dfs(w,seen|(1<<w),length+1)
        dfs(start,1<<start,1)
    assert total%2==0
    return total//2

def cycles_join_independent(G,b):
    import networkx as nx
    p=[1]
    for component in nx.connected_components(G):
        p=poly_mul(p,path_forest_poly(G.subgraph(component)))
    ans=Fraction(-len(G)*b,2)+cycles_bruteforce(G)
    for k in range(1,min(len(G),b)+1):
        ans+=Fraction(math.factorial(k)*math.factorial(k-1)*p[k]*math.comb(b,k),2)
    assert ans.denominator==1
    return int(ans)
