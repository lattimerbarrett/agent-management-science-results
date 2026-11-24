from itertools import combinations
from pathlib import Path
code = r'''from itertools import combinations

def check(n=6,d=3):
    facets=[sum(1<<v for v in f) for f in combinations(range(n),d+1)]
    m=len(facets)
    # For each candidate last facet, tabulate the trace of each other facet.
    traces=[[F&G for G in facets] for F in facets]
    proper=[[(F ^ (1<<v)) for v in range(n) if F>>v&1] for F in facets]
    shell=[False]*(1<<m)
    shell[0]=True
    shelling_extensions=[False]*(1<<m)
    shelling_extensions[-1]=True
    def attachment_ok(S,j):
        if S==0: return True
        F=facets[j]
        intersections=[traces[j][i] for i in range(m) if S>>i&1]
        ridges=[R for R in proper[j] if any(R&T==R for T in intersections)]
        # Intersection must be nonempty and pure of dimension d-1.
        return bool(ridges) and all(any(T&R==T for R in ridges) for T in intersections)
    for S in range(1,1<<m):
        for j in range(m):
            if S>>j&1 and shell[S^(1<<j)] and attachment_ok(S^(1<<j),j):
                shell[S]=True
                break
    # Fixed shelling prefixes can be extended precisely by these attachments.
    for S in range((1<<m)-2,-1,-1):
        shelling_extensions[S]=any(not(S>>j&1) and attachment_ok(S,j) and shelling_extensions[S|(1<<j)] for j in range(m))
    bad=[S for S in range(1,1<<m) if shell[S] and not shelling_extensions[S]]
    result={'n':n,'dimension':d,'facets':m,'subsets':1<<m,'shellable_nonempty':sum(shell)-1,'nonextendable_shellable':len(bad)}
    assert not bad, result
    return result

if __name__=='__main__':
    print(check())
'''
Path('workspace/agent3_check_shelling.py').write_text(code)
exec(compile(code, 'workspace/agent3_check_shelling.py', 'exec'))
# A separate recursive implementation of k-decomposability, with explicit
# deletion/link and purity checks, verifies the shellability equivalence.
from functools import lru_cache
from itertools import combinations
@lru_cache(None)
def faces_of(F):
    return tuple(G for G in range(64) if G&F==G)
@lru_cache(None)
def dim(C):
    ff=[G for G in range(64) if C>>G&1]
    maximal=[G for G in ff if not any(G!=H and G&H==G for H in ff)]
    sizes={G.bit_count() for G in maximal}
    return sizes.pop()-1 if len(sizes)==1 else -99
@lru_cache(None)
def kd(C,k):
    dimension=dim(C)
    if dimension==-99: return False
    ff=[G for G in range(64) if C>>G&1]
    if len(ff)==1<<(dimension+1): return True
    for sigma in ff:
        if not sigma or sigma.bit_count()>k+1: continue
        deletion=sum(1<<G for G in ff if G&sigma!=sigma)
        if dim(deletion)!=dimension: continue
        link=sum(1<<G for G in ff if G&sigma==0 and C>>(G|sigma)&1)
        if kd(deletion,k) and kd(link,k): return True
    return False
facets=[sum(1<<v for v in f) for f in combinations(range(6),4)]
closures=[sum(1<<G for G in faces_of(F)) for F in facets]
m=len(facets)
shell=[False]*(1<<m); shell[0]=True
complexes=[0]*(1<<m)
for S in range(1,1<<m):
    low=S&-S; j=low.bit_length()-1
    complexes[S]=complexes[S^low]|closures[j]
    for j,F in enumerate(facets):
        if not S>>j&1 or not shell[S^(1<<j)]: continue
        old=complexes[S^(1<<j)]
        if old==0:
            shell[S]=True; break
        intersection=old&closures[j]
        if dim(intersection)==2:
            shell[S]=True; break
    assert kd(complexes[S],3)==shell[S], S
print('Independently checked shellable iff 3-decomposable for all 32767 nonempty facet families; cache:',kd.cache_info())
