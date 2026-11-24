from functools import lru_cache
from itertools import combinations
import sys
sys.path.insert(0,"workspace")
from agent2_decomp import witness, maximal, rank

@lru_cache(None)
def shellable(fs):
    r=rank(fs)
    if r is None: return False
    if len(fs)==1: return True
    for f in fs:
        old=fs-{f}
        meet=maximal(f&g for g in old)
        if rank(meet)==r-1 and shellable(old): return True
    return False

def check(nmax=5):
    count=0; additions=0
    for n in range(1,nmax+1):
      for r in range(1,n+1):
        ff=[sum(1<<v for v in c) for c in combinations(range(n),r)]
        for bits in range(1,1<<len(ff)):
          fs=frozenset(f for j,f in enumerate(ff) if bits>>j&1)
          sh=shellable(fs)
          assert sh==(witness(fs,r-1) is not None), (fs,r)
          count+=1
          if sh:
            for f in ff:
              if f in fs: continue
              if shellable(fs|{f}):
                meet=maximal(f&g for g in fs)
                assert rank(meet)==r-1, (fs,f)
                additions+=1
    return count, additions

if __name__=="__main__": print(check())
