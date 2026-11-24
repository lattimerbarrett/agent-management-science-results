from itertools import combinations
from functools import lru_cache
from pathlib import Path

@lru_cache(None)
def vd(facets):
    fs=list(facets)
    if len(fs)==1:return True
    if not fs:return False
    size=fs[0].bit_count()
    if any(f.bit_count()!=size for f in fs):return False
    vertices=0
    for f in fs:vertices|=f
    for v in range(vertices.bit_length()):
        bit=1<<v
        if not vertices&bit:continue
        delete=[f for f in fs if not f&bit]
        link=[f^bit for f in fs if f&bit]
        if not delete:continue
        # deletion pure iff all facets with v removed covered by retained facets
        if any(not any(g&h==h for g in delete) for h in link):continue
        if vd(tuple(sorted(delete))) and vd(tuple(sorted(link))):return True
    return False

def mask(c):return sum(1<<v for v in c)
def check(d,n):
    # n old vertices; apex n
    mandatory=[mask(c)|(1<<n) for c in combinations(range(n),d)]
    optional=[mask(c) for c in combinations(range(n),d+1)]
    for choice in range(1<<len(optional)):
        fs=mandatory+[f for i,f in enumerate(optional) if choice>>i&1]
        assert vd(tuple(sorted(fs))), (d,n,choice)
    print('reservoir checked:',d,n,1<<len(optional),'complexes')

if __name__=='__main__':
    check(2,5)
    check(3,5)
    print(vd.cache_info())
    Path('workspace/agent2_reservoir_check.py').write_text(Path(__file__).read_text())
