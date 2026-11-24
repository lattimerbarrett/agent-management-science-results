from itertools import combinations
from functools import lru_cache
import os,pickle

def allfaces(F):
    return {frozenset(c) for i in range(len(F)+1) for c in combinations(F,i)}

def facets_normalize(facets):
    fs=set(map(frozenset,facets))
    return frozenset(f for f in fs if not any(f<g for g in fs))

@lru_cache(None)
def kdecomp(fs,k):
    fs=facets_normalize(fs)
    if len(fs)==1:return True
    sizes={len(f) for f in fs}
    if len(sizes)!=1:return False
    q=next(iter(sizes))
    faces=set().union(*(allfaces(f) for f in fs))
    for sig in sorted((s for s in faces if 0<len(s)<=k+1),key=lambda s:(len(s),sorted(s))):
        dele=facets_normalize(s for s in faces if not sig<=s)
        if any(len(f)!=q for f in dele):continue
        link=facets_normalize(f-sig for f in fs if sig<=f)
        if kdecomp(dele,k) and kdecomp(link,k):return True
    return False

def eligible(fs,F):
    ridges=[F-{v} for v in F if any(F-{v}<=f for f in fs)]
    return bool(ridges) and all(any((f&F)<=R for R in ridges) for f in fs)

def search(n=6,q=4):
    allf=list(map(frozenset,combinations(range(n),q)))
    blocked=[]
    for mask in range(1,1<<len(allf)):
        fs=frozenset(f for i,f in enumerate(allf) if mask>>i&1)
        missing=[f for f in allf if f not in fs]
        if missing and not any(eligible(fs,f) for f in missing):
            blocked.append(fs)
            if kdecomp(fs,1):
                print('FOUND',sorted(map(sorted,fs)),flush=True)
                return fs
    print('blocked',len(blocked))
def random_fast(n,trials):
    import random,time
    allf=[sum(1<<v for v in c) for c in combinations(range(n),4)]
    sub={f:[g for g in range(1<<n) if g&f==g] for f in allf}
    ridges={f:[(v,f^(1<<v)) for v in range(n) if f>>v&1] for f in allf}
    for trial in range(trials):
        fs={random.choice(allf)}; faces=set(sub[next(iter(fs))])
        remaining=set(allf)-fs
        while True:
            eligiblef=[]
            for f in remaining:
                R=sum(1<<v for v,r in ridges[f] if r in faces)
                if R not in faces:eligiblef.append(f)
            if not eligiblef:break
            f=random.choice(eligiblef);fs.add(f);faces.update(sub[f]);remaining.remove(f)
        if remaining:
            result=frozenset(frozenset(v for v in range(n) if f>>v&1) for f in fs)
            print('BLOCKED',n,trial,len(result),sorted(map(sorted,result)),flush=True)
            with open(f'workspace/blocked_agent4_{n}_{trial}.pkl','wb') as out:pickle.dump(result,out)
            print('edge_decomp',kdecomp(result,1),flush=True)
            return result
    return None

if __name__=='__main__':
    import random,time
    os.makedirs('workspace',exist_ok=True)
    with open('workspace/kdecomp_agent4.py','w') as out:
        out.write(open(__file__).read().split("if __name__==")[0])
    random.seed(71251)
    start=time.time()
    if os.path.basename(__file__)!='verify_shelling_agent4.py':
        source=open(__file__).read()
        with open('workspace/verify_shelling_agent4.py','w') as out:out.write(source)
    n=6;q=4
    allf=list(map(frozenset,combinations(range(n),q)))
    shellable=[False]*(1<<len(allf))
    shellable[0]=True
    counts=[0,0,0]
    for mask in range(1,1<<len(allf)):
        fs=frozenset(f for i,f in enumerate(allf) if mask>>i&1)
        if len(fs)==1:shellable[mask]=True
        else:
            shellable[mask]=any(shellable[mask^(1<<i)] and eligible(fs-{f},f) for i,f in enumerate(allf) if mask>>i&1)
        if shellable[mask]:
            counts[0]+=1
            for i,f in enumerate(allf):
                if not mask>>i&1:
                    e=eligible(fs,f)
                    if e:counts[1]+=1
                    if shellable[mask|(1<<i)] and not e:counts[2]+=1
    # Check transitions separately once every state has been computed.
    for mask in range(1,1<<len(allf)):
        if not shellable[mask]:continue
        fs=frozenset(f for i,f in enumerate(allf) if mask>>i&1)
        for i,f in enumerate(allf):
            if not mask>>i&1:
                assert shellable[mask|(1<<i)]==eligible(fs,f)
    print('n6 rank4 shellable complexes, eligible additions, temporary unchecked',counts)
    print('All shellable additions exactly satisfy ridge-intersection criterion.')
