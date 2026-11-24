from itertools import combinations
from agent4_checker import dec

def bmsets(n,s):
    return [sum(1<<v for v in c) for c in combinations(range(n),s)]

def capped_cone_tests(n,d,k):
    # L has facets of cardinality d; cap facets cardinality d+1.
    candidates=bmsets(n,d)
    checks=0
    for z in range(1,1<<len(candidates)):
        L=tuple(f for j,f in enumerate(candidates) if z>>j&1)
        if not dec(L,k):
            continue
        Lset=set(L)
        caps=[B for B in bmsets(n,d+1) if all(B^(1<<v) in Lset for v in range(n) if B>>v&1)]
        for w in range(1<<len(caps)):
            G=tuple(sorted([f|(1<<n) for f in L]+[B for j,B in enumerate(caps) if w>>j&1]))
            assert dec(G,k),(n,d,k,L,caps,w)
            checks+=1
    return checks

if __name__=='__main__':
    for n,d,k in [(4,2,0),(4,2,1),(5,3,0),(5,3,1),(5,3,2)]:
        print((n,d,k),capped_cone_tests(n,d,k),flush=True)
