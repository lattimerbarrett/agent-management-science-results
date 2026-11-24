import itertools
import networkx as nx

def odd_cube(G):
    F=nx.Graph();F.add_nodes_from(G)
    for x in G:
        reach=set(G[x])
        for a in G[x]:
            for b in G[a]:
                reach.update(G[b])
        assert x not in reach
        F.add_edges_from((x,y) for y in reach)
    return F

def universal(k):
    V=[(a,mask) for a in range(k) for mask in range(1<<k) if not(mask>>a&1)]
    H=nx.Graph();H.add_nodes_from(V)
    for (a,A),(b,B) in itertools.combinations(V,2):
        if (B>>a&1) and (A>>b&1) and not(A&B):H.add_edge((a,A),(b,B))
    assert not any(nx.triangles(H).values())
    return H

def verify_map(G):
    F=odd_cube(G)
    col=nx.coloring.greedy_color(F,strategy='largest_first')
    k=max(col.values(),default=-1)+1
    images={v:(col[v],sum(1<<a for a in {col[w] for w in G[v]})) for v in G}
    for x,y in G.edges():
        a,A=images[x];b,B=images[y]
        assert a!=b and B>>a&1 and A>>b&1 and not(A&B)

def main():
    for k in range(1,6):
        H=universal(k)
        print('Universal target',k,H.number_of_nodes(),H.number_of_edges(),'triangle-free')
    count=0
    for G in nx.graph_atlas_g():
        if len(G)==0:continue
        # exact closed-odd-walk test by adjacency matrix integer powers
        import numpy as np
        A=nx.to_numpy_array(G,dtype='int64')
        if np.trace(A@A@A) or np.trace(A@A@A@A@A):continue
        verify_map(G);count+=1
    print('Odd-cube and target-map checks on all',count,'C3,C5-free atlas graphs through 7 vertices')
    # Exhaustively verify six-set disjointness from the reduced-graph constraints.
    count=0;k=4
    pairs=list(itertools.combinations(range(k),2))
    for bits in range(1<<len(pairs)):
        nbr=[0]*k
        for j,(a,b) in enumerate(pairs):
            if bits>>j&1:nbr[a]|=1<<b;nbr[b]|=1<<a
        def N(S):
            ans=0
            for i in range(k):
                if S>>i&1:ans|=nbr[i]
            return ans
        for S,T,U in itertools.product(range(1,1<<k),repeat=3):
            sets=(S,T,U); ns=tuple(map(N,sets))
            if any(not z for z in ns):continue
            if any(a&b for a,b in itertools.combinations(sets,2)):continue
            if any(a&b for a,b in itertools.combinations(ns,2)):continue
            union=S|T|U
            if union&(ns[0]|ns[1]|ns[2]):continue
            allsets=sets+ns
            assert all(not(a&b) for a,b in itertools.combinations(allsets,2))
            assert sum(z.bit_count() for z in allsets)<=k
            count+=1
    print('Exhaustive six-set count for all reduced graphs through 4 nodes:',count)
if __name__=='__main__':main()
