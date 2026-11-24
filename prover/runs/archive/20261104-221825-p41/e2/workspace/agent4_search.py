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
if __name__=='__main__':
    import pathlib
    code=pathlib.Path('scratchpad.py').read_text().split("if __name__=='__main__':")[0]
    pathlib.Path('workspace/agent4_checker.py').write_text(code)
    print('wrote workspace/agent4_checker.py')
    # optimized random shelling, preserving all faces explicitly
    def fast(n,d,trials):
        allf=[sum(1<<v for v in c) for c in combinations(range(n),d+1)]
        subs={f:set(subsets(f))|{0} for f in allf}
        bits={f:[1<<v for v in range(n) if f>>v&1] for f in allf}
        for trial in range(trials):
            fs=[random.choice(allf)];faces=set(subs[fs[0]]);todo=set(allf)-set(fs)
            while todo:
                cand=list(todo);random.shuffle(cand)
                for f in cand:
                    restriction=sum(v for v in bits[f] if f^v in faces)
                    if restriction not in faces:
                        fs.append(f);faces.update(subs[f]);todo.remove(f);break
                else:
                    print('OBSTRUCTION',n,d,len(fs),fs,flush=True);return fs
            if trial%1000==0:print('fast trial',n,d,trial,flush=True)
        print('none fast',n,d,flush=True)
    def skeleton_test(n,D,k,trials):
        allf=[sum(1<<v for v in c) for c in combinations(range(n),D+1)]
        subs={f:set(subsets(f))|{0} for f in allf}
        bits={f:[1<<v for v in range(n) if f>>v&1] for f in allf}
        for trial in range(trials):
            fs=[random.choice(allf)];faces=set(subs[fs[0]]);todo=set(allf)-set(fs)
            for _ in range(random.randint(2,15)):
                cand=list(todo);random.shuffle(cand)
                for f in cand:
                    restriction=sum(v for v in bits[f] if f^v in faces)
                    if restriction not in faces and restriction.bit_count()<=k+1:
                        fs.append(f);faces.update(subs[f]);todo.remove(f);break
                else:break
            sk=tuple(sorted(set(f^v for f in fs for v in bits[f])))
            if not dec(sk,k-1):
                print('SKELETON COUNTEREXAMPLE',n,D,k,fs,flush=True);return fs
            print('skeleton pass',trial,len(fs),dec.cache_info(),flush=True)
            if dec.cache_info().currsize>200000:dec.cache_clear()
    def antigreed(n,d,trials):
        allf=[sum(1<<v for v in c) for c in combinations(range(n),d+1)]
        subs={f:set(subsets(f))|{0} for f in allf}
        bits={f:[1<<v for v in range(n) if f>>v&1] for f in allf}
        def options(todo,faces):
            return [f for f in todo if sum(v for v in bits[f] if f^v in faces) not in faces]
        for trial in range(trials):
            fs=[random.choice(allf)];faces=set(subs[fs[0]]);todo=set(allf)-set(fs)
            while todo:
                cand=options(todo,faces)
                if not cand:
                    print('ANTI OBSTRUCTION',n,d,len(fs),fs,flush=True);return fs
                random.shuffle(cand)
                f=min(cand[:20],key=lambda f:len(options(todo-{f},faces|subs[f]))+random.random()*0.1)
                fs.append(f);faces.update(subs[f]);todo.remove(f)
            if trial%10==0:print('anti pass',trial,flush=True)
        print('none anti',n,d,flush=True)
    random.seed(12345)
    skeleton_test(8,4,2,1000)
    antigreed(10,3,1000)
