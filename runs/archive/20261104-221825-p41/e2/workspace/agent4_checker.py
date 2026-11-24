from functools import lru_cache
from itertools import combinations
import random, time

def maximal(fs):
    fs=set(fs)
    return tuple(sorted(f for f in fs if not any(f!=g and f&g==f for g in fs)))

def subsets(s):
    t=s
    while t:
        yield t
        t=(t-1)&s

@lru_cache(None)
def dec(fs,k):
    if len(fs)==1:return True
    if not fs:return False
    sizes={f.bit_count() for f in fs}
    if len(sizes)>1:return False
    sz=next(iter(sizes))
    candidates=set(x for f in fs for x in subsets(f) if x.bit_count()<=k+1)
    for s in sorted(candidates,key=lambda x:x.bit_count()):
        link=tuple(sorted(f^s for f in fs if f&s==s))
        dl=maximal([f for f in fs if f&s!=s]+[f^v for f in fs if f&s==s for v in subsets(s) if v.bit_count()==1])
        if dl and all(f.bit_count()==sz for f in dl) and dec(link,k) and dec(dl,k):return True
    return False

def search(n,d,k,exhaust=False,trials=10000):
    allf=[sum(1<<v for v in c) for c in combinations(range(n),d+1)]
    t=time.time()
    if exhaust:
        cand=(tuple(allf[i] for i in range(len(allf)) if m>>i&1) for m in range(1,1<<len(allf)))
    else:
        cand=(tuple(f for f in allf if random.random()<random.random()) for _ in range(trials))
    cnt=0
    for fs in cand:
        if not fs or not dec(fs,k):continue
        cnt+=1
        if not any(dec(tuple(sorted(fs+(f,))),k) for f in allf if f not in fs) and len(fs)<len(allf):
            print('OBSTRUCTION',n,d,k,fs,flush=True);return fs
    print('none',n,d,k,'decomp',cnt,'time',time.time()-t,'cache',dec.cache_info(),flush=True)

def greed(n,d,k,trials):
    allf=[sum(1<<v for v in c) for c in combinations(range(n),d+1)]
    for trial in range(trials):
        fs=(random.choice(allf),)
        while len(fs)<len(allf):
            cand=[f for f in allf if f not in fs];random.shuffle(cand)
            for f in cand:
                new=tuple(sorted(fs+(f,)))
                if dec(new,k):fs=new;break
            else:
                print('OBSTRUCTION',n,d,k,len(fs),fs,flush=True);return fs
        if trial%10==0:print('trial',trial,'cache',dec.cache_info(),flush=True)
        if dec.cache_info().currsize>400000:dec.cache_clear()
    print('none',flush=True)
def shellgreed(n,d,trials):
    allf=[sum(1<<v for v in c) for c in combinations(range(n),d+1)]
    for trial in range(trials):
        fs=[random.choice(allf)]
        while len(fs)<len(allf):
            cand=[f for f in allf if f not in fs];random.shuffle(cand)
            ridges=set(g^v for g in fs for v in subsets(g) if v.bit_count()==1)
            for f in cand:
                rs=[f^v for v in subsets(f) if v.bit_count()==1 and f^v in ridges]
                if rs and all(any((g&f)&r==g&f for r in rs) for g in fs):
                    fs.append(f);break
            else:
                print('SHELL OBSTRUCTION',n,d,len(fs),fs,flush=True);return fs
        if trial%100==0:print('trial',trial,flush=True)
    print('none',flush=True)
