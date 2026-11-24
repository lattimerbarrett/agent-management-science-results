"""Exhaustive exact k-decomposability completion checker (small n only)."""
from itertools import combinations
from functools import lru_cache

def check(n=6,d=3,k=1):
    facets=tuple(sum(1<<v for v in c) for c in combinations(range(n),d+1))
    @lru_cache(None)
    def kd(fs):
        if len(fs)==1:return True
        if not fs:return False
        faces=set()
        for f in fs:
            vs=[v for v in range(n) if f>>v&1]
            for s in range(1,min(k+1,len(vs))+1):
                faces.update(sum(1<<v for v in c) for c in combinations(vs,s))
        for s in faces:
            deletion=tuple(f for f in fs if f&s!=s)
            if not deletion:continue
            containing=tuple(f for f in fs if f&s==s)
            # Every newly exposed codimension-one face must extend to a retained facet.
            if any(not any((f^(1<<v))&g==(f^(1<<v)) for g in deletion)
                   for f in containing for v in range(n) if s>>v&1):continue
            link=tuple(sorted(f^s for f in containing))
            if kd(deletion) and kd(link):return True
        return False
    N=len(facets); full=(1<<N)-1
    finish=bytearray(1<<N); good=0; bad=[]
    for mask in range(full,0,-1):
        fs=tuple(f for j,f in enumerate(facets) if mask>>j&1)
        if not kd(fs):continue
        good+=1
        if mask==full or any(finish[mask|(1<<j)] for j in range(N) if not mask>>j&1):
            finish[mask]=1
        elif all(any(f>>v&1 for f in fs) for v in range(n)):
            bad.append(fs)
    return dict(n=n,d=d,k=k,decomposable=good,noncompletable=len(bad)),bad

if __name__=='__main__':
    for k in (1,2,3):
        result,bad=check(k=k)
        print(result)
        assert not bad
