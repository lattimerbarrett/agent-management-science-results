from functools import lru_cache
from time import perf_counter

def count_intersecting_antichains(m):
    subsets=list(range(1,1<<m));N=len(subsets)
    adjacency=[]
    for a in subsets:
        neighbors=0
        for j,b in enumerate(subsets):
            if (a&b) and (a&b)!=a and (a&b)!=b:neighbors|=1<<j
        adjacency.append(neighbors)
    @lru_cache(None)
    def count(candidates):
        total=1
        while candidates:
            bit=candidates&-candidates;candidates^=bit
            j=bit.bit_length()-1
            total+=count(candidates&adjacency[j])
        return total
    ans=count((1<<N)-1)
    return ans,count.cache_info()
if __name__=='__main__':
    from pathlib import Path

for k in range(1,9):
    start=perf_counter();res,info=count_intersecting_antichains(k-1)
    print(k,res,info,'time',perf_counter()-start,flush=True)
