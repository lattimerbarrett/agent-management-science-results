from itertools import combinations
from functools import lru_cache
import json, time

# Exhaust all pure 3-complexes whose facets are subsets of a six-vertex set.
n=6; d=3
facets=[sum(1<<v for v in c) for c in combinations(range(n),d+1)]
m=len(facets); full=(1<<m)-1
# For each potential facet, precompute its intersection with all other facets.
inter=[[f&g for g in facets] for f in facets]

def legal(mask,j):
    if not mask:return True
    ints=[inter[j][i] for i in range(m) if mask>>i&1]
    ridges=[x for x in ints if x.bit_count()==d]
    return bool(ridges) and all(any(x&r==x for r in ridges) for x in ints)

shellable=bytearray(1<<m); shellable[0]=1
for mask in range(1<<m):
    if shellable[mask]:
        for j in range(m):
            if not(mask>>j&1) and legal(mask,j):shellable[mask|1<<j]=1
extends=bytearray(1<<m); extends[full]=1
for mask in range(full-1,-1,-1):
    extends[mask]=any(not(mask>>j&1) and extends[mask|1<<j] and legal(mask,j) for j in range(m))
assert all(not s or e for s,e in zip(shellable,extends))

# Independent recursive implementation of the definition in the question.
def canonical(fs):
    fs=set(fs)
    return tuple(sorted(f for f in fs if not any(f!=g and f&g==f for g in fs)))

@lru_cache(None)
def kd(fs,k):
    if len(fs)==1:return True
    sizes={f.bit_count() for f in fs}
    if len(sizes)!=1:return False
    size=next(iter(sizes))
    faces=set()
    for f in fs:
        s=f
        while s:
            if s.bit_count()<=k+1:faces.add(s)
            s=(s-1)&f
    for s in faces:
        # Deletion's faces: retain facets avoiding s; split those containing s.
        df=[]; lf=[]
        for f in fs:
            if f&s!=s:df.append(f)
            else:
                lf.append(f^s)
                x=s
                while x:
                    v=x&-x; x-=v
                    df.append(f^v)
        df=canonical(df); lf=canonical(lf)
        if df and all(f.bit_count()==size for f in df) and kd(df,k) and kd(lf,k):return True
    return False

count=0
for mask in range(1,1<<m):
    fs=tuple(facets[i] for i in range(m) if mask>>i&1)
    answer=kd(tuple(sorted(fs)),d)
    assert answer==bool(shellable[mask]),(mask,answer)
    count+=answer
report=dict(d=d,n=n,facets=m,pure_nonempty_complexes=full,shellable_complexes=count,
            all_shellable_extend=True,all_d_decomposable_iff_shellable=True,kd_cache=str(kd.cache_info()))
print(json.dumps(report,indent=2))
with open('workspace/agent1_checks.json','w') as f:json.dump(report,f,indent=2)
# Preserve executable independent verifier.
with open('workspace/agent1_verifier.py','w') as f:f.write(open(__file__).read())

bad=[]; checked=0
for mask in range(1,1<<m):
    if not shellable[mask]: continue
    fs=tuple(facets[i] for i in range(m) if mask>>i&1)
    ridges=canonical([f^(1<<v) for f in fs for v in range(n) if f>>v&1])
    if not kd(ridges,0):
        bad.append(mask)
        print('NONVD SKELETON',mask,fs,ridges)
        break
    nc=canonical(list(fs)+[r|(1<<n) for r in ridges])
    if not kd(nc,0):
        bad.append(mask)
        print('NONVD NEARCONE',mask,fs)
        break
    checked+=1
print('nearcone VD checked',checked,'bad',bad,'cache',kd.cache_info())
print('original VD count',sum(kd(tuple(sorted(facets[i] for i in range(m) if mask>>i&1)),0) for mask in range(1,1<<m) if shellable[mask]))
