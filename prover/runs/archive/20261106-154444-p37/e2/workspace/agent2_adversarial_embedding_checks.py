"""Exhaustive checks of middle-layer grouped suitable families and grid embeddings."""
from itertools import combinations, product
from random import Random

def construction(sizes,max_patterns=32,grid_size=3):
    t=sum(sizes); full=(1<<t)-1; m=t//2
    groups=[]; j=0
    for s in sizes:groups.append(sum(1<<i for i in range(j,j+s)));j+=s
    cross=lambda a:all(a&g and (full^a)&g for g in groups)
    if t%2==0:
        variable=[a for a in range(1<<t) if a.bit_count()==m and a<(full^a) and cross(a)]
    else:
        candidates=[[a for a in range(1<<t) if a.bit_count()==m and a>>i&1 and cross(a)] for i in range(t)]
        variable=max(candidates,key=len)
    V=len(variable)
    if (1<<V)<=max_patterns:patterns=list(range(1<<V))
    else:
        rng=Random(437); patterns=sorted({0,(1<<V)-1,*[rng.getrandbits(V) for _ in range(max_patterns-2)]})
    # Fixed bits can be omitted from lex comparisons; only variable complement pairs differ.
    orders=[]
    for i in range(t):
        orders.append(sorted(range(len(patterns)),key=lambda v:tuple(((patterns[v]>>j)&1) if a>>i&1 else 1-((patterns[v]>>j)&1) for j,a in enumerate(variable))))
    ranks=[{v:j for j,v in enumerate(o)} for o in orders]; n=len(patterns)
    for a,b in combinations(range(n),2):
        for g in groups:
            assert any(ranks[i][a]<ranks[i][b] for i in range(t) if g>>i&1)
            assert any(ranks[i][b]<ranks[i][a] for i in range(t) if g>>i&1)
    for triple in combinations(range(n),3):
        for a in triple:assert any(all(ranks[i][a]>ranks[i][b] for b in triple if b!=a) for i in range(t))
    # Independent grid order-embedding check on first ten vertices.
    nn=min(n,4); Q=[frozenset([v]) for v in range(nn)]+[frozenset(e) for e in combinations(range(nn),2)]
    els=[(p,A) for p in product(range(grid_size),repeat=len(groups)) for A in Q]
    role=[next(j for j,g in enumerate(groups) if g>>i&1) for i in range(t)]
    cs=[tuple(grid_size*max(ranks[i][v] for v in A)+p[role[i]] for i in range(t)) for p,A in els]
    for x,(p,A) in enumerate(els):
        for y,(q,B) in enumerate(els):
            actual=all(a<=b for a,b in zip(p,q)) and A<=B
            represented=all(a<=b for a,b in zip(cs[x],cs[y]))
            assert actual==represented,(sizes,els[x],els[y])
    print({'groups':sizes,'freebits':V,'patterns_checked':n,'all_triples_checked':3*len(list(combinations(range(n),3))),'grid_ordered_pairs_checked':len(els)**2},flush=True)

if __name__=='__main__':
    for sizes,grid_size in [([2,2,2],3),([2,2,2,2],3),([3,3,4],5)]:construction(sizes,grid_size=grid_size)
