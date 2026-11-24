from itertools import combinations
from functools import lru_cache
import os
print('cwd',os.getcwd())
print('experiments exists',os.path.exists('experiments'))

# Shellability tested by the ordered-facet ridge-witness criterion:
# for each earlier A and later B, an intervening earlier C has
# A intersect B subset C intersect B, with |C intersect B|=d.
# This uses neither links nor the separate maximal-intersection test.
for n,d in [(5,2),(6,3)]:
    facets=[frozenset(c) for c in combinations(range(n),d+1)]
    N=len(facets)
    @lru_cache(None)
    def witnesses(mask,last):
        b=facets[last]
        earlier=[j for j in range(N) if mask>>j&1]
        return all(any(len(facets[c]&b)==d and (facets[a]&b)<=(facets[c]&b) for c in earlier) for a in earlier)
    @lru_cache(None)
    def shell(mask):
        if mask & (mask-1)==0:return True
        return any(shell(mask^(1<<j)) and witnesses(mask^(1<<j),j) for j in range(N) if mask>>j&1)
    counter=None
    checked=0
    for mask in range(1,1<<N):
        if not shell(mask):continue
        for j in range(N):
            if mask>>j&1:continue
            union=mask|(1<<j)
            if not shell(union):continue
            checked+=1
            ints={facets[j]&facets[a] for a in range(N) if mask>>a&1}
            maximal=[s for s in ints if not any(s<t for t in ints)]
            if any(len(s)!=d for s in maximal):
                counter=([sorted(facets[a]) for a in range(N) if mask>>a&1],sorted(facets[j]),[sorted(s) for s in maximal])
                break
        if counter:break
    print({'n':n,'d':d,'adjacent_shellable_pairs':checked,'counterexample':counter},flush=True)
