"""Exact finite checks for the lower-bound ingredients. Run python agent3_lower_checks.py."""
import itertools
import networkx as nx

def check_standard_example():
    n=3
    R={(i,i) for i in range(6)}|{(i,3+j) for i in range(n) for j in range(n) if i!=j}
    orders=[]
    for k in range(n):
        others=[i for i in range(n) if i!=k]
        orders.append(others+[3+k,k]+[3+i for i in others])
    common=set(itertools.product(range(6), repeat=2))
    for order in orders:
        rank={x:i for i,x in enumerate(order)}
        L={(a,b) for a in range(6) for b in range(6) if rank[a]<=rank[b]}
        assert R<=L
        common &= L
    assert common==R
    count=0
    for order in itertools.permutations(range(6)):
        rank={x:i for i,x in enumerate(order)}
        if all(rank[a]<=rank[b] for a,b in R):
            count+=1
            assert sum(rank[3+i]<rank[i] for i in range(3))<=1
    return count,orders

def maximal_intersecting(k):
    G=nx.Graph()
    G.add_nodes_from(range(1,1<<k))
    G.add_edges_from((a,b) for a in G for b in G if a<b and a&b)
    families=[frozenset(C) for C in nx.find_cliques(G)]
    for F in families:
        assert all(a&b for a in F for b in F)
        assert all(any(not(a&b) for b in F) for a in range(1<<k) if a not in F)
    return families

def check_lower_encoding(k):
    # Any suitable system encodes each vertex in a distinct maximal intersecting family.
    # Check this for all suitable systems of k permutations on three vertices.
    perms=list(itertools.permutations(range(3)))
    maxfamilies=maximal_intersecting(k)
    tested=0
    for orders in itertools.product(perms,repeat=k):
        ranks=[{x:i for i,x in enumerate(o)} for o in orders]
        S={(x,y):sum((1<<i) for i,r in enumerate(ranks) if r[x]>r[y]) for x in range(3) for y in range(3) if x!=y}
        if not all(S[x,y]&S[x,z] for x,y,z in itertools.permutations(range(3))): continue
        choices=[]
        for x in range(3):
            Fx=[F for F in maxfamilies if all(S[x,y] in F for y in range(3) if y!=x)]
            assert Fx
            choices.append(Fx)
        assert all(F!=H for x in range(3) for y in range(x) for F in choices[x] for H in choices[y])
        tested+=1
    return tested

if __name__=='__main__':
    print('S3 extension count and 3-realizer:',check_standard_example())
    print('lambda(k), k=1..5:',[len(maximal_intersecting(k)) for k in range(1,6)])
    print('suitable systems checked at k=3,4:',[check_lower_encoding(k) for k in (3,4)])
