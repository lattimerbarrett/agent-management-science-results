"""Finite checks for lambda and lower-bound proof. Run/import with Python."""
from itertools import combinations, permutations
import networkx as nx

def maximal_intersecting(k):
    G=nx.Graph()
    G.add_nodes_from(range(1,1<<k))
    G.add_edges_from((a,b) for a in G for b in G if a<b and a&b)
    return [frozenset(c) for c in nx.find_cliques(G)]

def verify_family(F,k):
    U=(1<<k)-1
    assert all(a&b for a in F for b in F)
    assert all(any(not(a&b) for b in F) for a in range(1<<k) if a not in F)
    assert all((a in F) != ((U^a) in F) for a in range(1<<k))
    assert all(b in F for a in F for b in range(1<<k) if a&b==a)

def verify_permutations(ps):
    n=len(ps[0]);t=len(ps)
    ranks=[{v:i for i,v in enumerate(p)} for p in ps]
    assert all(any(r[x]>r[y] and r[x]>r[z] for r in ranks)
               for x in range(n) for y,z in combinations([v for v in range(n) if v!=x],2))
    fams=maximal_intersecting(t)
    chosen=[]
    for x in range(n):
        sets={sum(1<<i for i,r in enumerate(ranks) if r[x]>r[y]) for y in range(n) if y!=x}
        assert all(a&b for a in sets for b in sets)
        chosen.append(next(F for F in fams if sets<=F))
    assert len(set(chosen))==n
    return chosen

if __name__=='__main__':
    prev=None
    for k in range(1,7):
        fams=maximal_intersecting(k)
        for F in fams:verify_family(F,k)
        if prev is not None:
            lifted={frozenset(a for a in range(1<<k) if (a&((1<<(k-1))-1)) in F) for F in prev}
            assert len(lifted)==len(prev) and lifted<=set(fams)
        print('lambda(%s) = %s; all families and lift injections checked'%(k,len(fams)))
        prev=fams
    ps=[(0,1,2,3),(0,3,2,1),(1,3,2,0)]
    verify_permutations(ps)
    print('3-suitable orders on 4 points -> 4 distinct maximal intersecting families checked')
