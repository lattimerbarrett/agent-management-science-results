from functools import lru_cache
from itertools import combinations
from pathlib import Path
import sys,random,time,json

@lru_cache(None)
def dec(facets,k):
    if len(facets)==1:return True
    ridgedeg={};support={}
    for f in facets:
        vs=[1<<i for i in range(f.bit_length()) if f>>i&1]
        for v in vs:ridgedeg[f^v]=ridgedeg.get(f^v,0)+1
        for size in range(1,min(k+1,len(vs))+1):
            for tup in combinations(vs,size):
                s=sum(tup);support.setdefault(s,[]).append(f)
    for s,star in sorted(support.items(),key=lambda z:(len(z[1]),z[0].bit_count())):
        vs=[1<<i for i in range(s.bit_length()) if s>>i&1]
        if any(ridgedeg[f^v]<2 for f in star for v in vs):continue
        dele=tuple(f for f in facets if f&s!=s)
        link=tuple(sorted(f^s for f in star))
        if dec(dele,k) and dec(link,k):return True
    return False

if __name__=='__main__':
    Path('workspace/agent4_fastdec.py').write_text(Path(__file__).read_text())
    sys.path.insert(0,'workspace')
    from agent4_decomposable_check import kd
    allf=[sum(1<<i for i in c) for c in combinations(range(6),4)]
    start=time.time()
    for a in range(1,1<<len(allf)):
        ff=tuple(sorted(allf[j] for j in range(len(allf)) if a>>j&1))
        assert dec(ff,1)==kd(ff,1)
    print('all32767 checked equality',time.time()-start,dec.cache_info())
