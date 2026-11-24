"""Exact finite H-embedding template checks; no asymptotic claims."""
import networkx as nx

def colorable(G,k):
    order=sorted(G,key=lambda v:-G.degree(v)); cs={}
    def rec(i):
        if i==len(order): return True
        v=order[i]; bad={cs[w] for w in G[v] if w in cs}
        for c in range(k):
            if c not in bad:
                cs[v]=c
                if rec(i+1): return True
                del cs[v]
        return False
    return rec(0)

def embeds_triangle_part(G,r):
    n=len(G)
    for mask in range(1<<n):
        S=[v for v in G if mask>>v&1]
        if any(len(c)>3 for c in nx.connected_components(G.subgraph(S))): continue
        if colorable(G.subgraph(set(G)-set(S)),r-1): return S
    return None

def embeds_matching_parts(G,r,k):
    n=len(G)
    def rec(w,m,ds,act):
        if len(w)==n: return w
        v=len(w)
        for c in range(min(m+1,r-1)+1):
            same=[j for j in G[v] if j<v and w[j]==c]
            if len(same)>1 or any(ds[j] for j in same): continue
            na=act|({c} if same else set())
            if len(na)>k: continue
            nd=ds[:]+[len(same)]
            for j in same: nd[j]+=1
            ans=rec(w+[c],max(m,c),nd,na)
            if ans is not None:return ans
        return None
    return rec([0],0,[0],set())

def cycle_power(r):
    n=3*r+3
    G=nx.Graph();G.add_nodes_from(range(n))
    G.add_edges_from((i,j) for i in range(n) for j in range(i+1,n) if min(j-i,n-j+i)<=r)
    return G

if __name__=='__main__':
    for r in range(2,5):
        for d in range(1,r+1):
            G=cycle_power(r);G.remove_edge(0,d)
            assert embeds_matching_parts(G,r,2) is None
            assert embeds_triangle_part(G,r) is None
            assert colorable(G,r+1)
            assert not colorable(G,r)
            print('verified r=',r,'deleted edge distance',d)
