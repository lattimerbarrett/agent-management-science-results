from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json,time


def subsets(mask):
    s=mask
    while True:
        yield s
        if not s: break
        s=(s-1)&mask

def maximal(fs):
    fs=set(fs)
    return tuple(sorted(f for f in fs if not any(f!=g and f&g==f for g in fs)))

def pure(fs):
    return bool(fs) and len({f.bit_count() for f in fs})==1

@lru_cache(None)
def kd(fs,k):
    # Independent direct implementation of recursive definition, on facet sets.
    if len(fs)==1: return True
    assert pure(fs)
    size=fs[0].bit_count()
    faces=set().union(*(set(subsets(f)) for f in fs))-{0}
    for sig in faces:
        if sig.bit_count()>k+1: continue
        dele=[]
        for f in fs:
            if f&sig!=sig: dele.append(f)
            else:
                dele.extend(f^(1<<v) for v in range(f.bit_length()) if sig>>v&1)
        dele=maximal(dele)
        if not pure(dele) or dele[0].bit_count()!=size: continue
        link=maximal(f^sig for f in fs if f&sig==sig)
        if kd(dele,k) and kd(link,k): return True
    return False

def intersection_good(old,F,size):
    inter=maximal(f&F for f in old)
    return pure(inter) and inter[0].bit_count()==size-1

@lru_cache(None)
def shellable(fs):
    # Exhaust all possible last facets, with no use of k-decomposability.
    if len(fs)==1: return True
    size=fs[0].bit_count()
    for F in fs:
        old=tuple(f for f in fs if f!=F)
        if intersection_good(old,F,size) and shellable(old): return True
    return False

def check(n,d):
    start=time.time(); size=d+1
    facets=[sum(1<<v for v in c) for c in combinations(range(n),size)]
    total=0;shellcount=0;paircount=0
    shell_status={}
    for mask in range(1,1<<len(facets)):
        fs=tuple(sorted(facets[i] for i in range(len(facets)) if mask>>i&1))
        a=shellable(fs);b=kd(fs,d)
        assert a==b,(n,d,fs,a,b)
        shell_status[mask]=a
        total+=1;shellcount+=a
    for mask,ok in shell_status.items():
        if not ok:continue
        old=tuple(facets[i] for i in range(len(facets)) if mask>>i&1)
        for i,F in enumerate(facets):
            if not(mask>>i&1) and shell_status[mask|(1<<i)]:
                assert intersection_good(old,F,size),(n,d,old,F)
                paircount+=1
    result=dict(n=n,d=d,complexes=total,shellable=shellcount,shellable_adjacent_pairs=paircount,seconds=round(time.time()-start,3))
    print(json.dumps(result),flush=True)
    return result

def check_vertex_introduction(d,start_n,end_n):
    size=d+1
    old=[sum(1<<v for v in c) for c in combinations(range(start_n),size)]
    count=0
    for x in range(start_n,end_n):
        for H in combinations(range(x),d):
            F=(1<<x)|sum(1<<v for v in H)
            assert intersection_good(old,F,size),(d,start_n,end_n,F)
            old.append(F);count+=1
    assert len(old)==len(list(combinations(range(end_n),size)))
    return count

if __name__=='__main__':
    results=[check(n,d) for n,d in [(4,1),(5,2),(6,3)]]
    blocks=sum(check_vertex_introduction(d,n,9) for d in range(1,5) for n in range(d+1,9))
    print('Vertex-introduction shelling steps checked:',blocks)
    Path('workspace/agent4_checks.json').write_text(json.dumps({'exhaustive':results,'vertex_introduction_steps':blocks},indent=2))
    Path('workspace/agent4_exhaustive.py').write_text(Path(__file__).read_text())
