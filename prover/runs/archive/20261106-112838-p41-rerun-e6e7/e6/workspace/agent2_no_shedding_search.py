import itertools,random,time,json
from pathlib import Path

def subs(f):
    s=f
    while True:
        yield s
        if not s:break
        s=(s-1)&f

def search(n,trials=100):
    rng=random.Random(1729+n)
    fac=[sum(1<<i for i in c) for c in itertools.combinations(range(n),4)]
    ridges={f:[t for t in subs(f) if t.bit_count()==3] for f in fac}
    start=time.time();total=0;best=100000
    for trial in range(trials):
        order=[rng.choice(fac)];faces=set(subs(order[0]));rem=set(fac)-set(order)
        owners={t:{order[0]} for t in ridges[order[0]]}
        while rem:
            cand=[]
            for f in rem:
                r=sum(f^t for t in ridges[f] if t in faces)
                if r and r not in faces:cand.append(f)
            if not cand:break
            # Favor additions sharing 3 ridges: these introduce new triangles,
            # not new edges or vertices, and can erase edge-shedding witnesses.
            if rng.random()<0.8:
                scores=[{1:0,2:1,3:3,4:-1}[sum(t in faces for t in ridges[f])] for f in cand]
                mx=max(scores)
                pool=[f for f,s in zip(cand,scores) if s==mx]
                f=rng.choice(pool)
            else:f=rng.choice(cand)
            order.append(f);rem.remove(f);faces.update(subs(f))
            for t in ridges[f]:owners.setdefault(t,set()).add(f)
            blocked=set();blocked_v=0
            for t,own in owners.items():
                if len(own)==1:
                    ff=next(iter(own));v=ff^t;blocked_v|=v
                    for u in subs(t):
                        if u.bit_count()==1:blocked.add(v|u)
            vs=0
            for ff in order:vs|=ff
            edge=[e for e in faces if e.bit_count()==2]
            free_v=(vs&~blocked_v).bit_count()
            free_e=sum(e not in blocked for e in edge)
            gap=free_v+free_e
            best=min(best,gap);total+=1
            if gap==0:
                # Exact structural certificate: for every vertex/edge there
                # is a deletion-orphan ridge supported only by a removed facet.
                for s in faces:
                    if s.bit_count() not in (1,2):continue
                    okay=False
                    for ff in order:
                        if ff&s!=s:continue
                        for t in ridges[ff]:
                            if t&s!=s and owners[t]=={ff}:okay=True
                    assert okay
                out={'n':n,'shelling':order,'trial':trial,'steps':total}
                Path('workspace/agent2_no_shedding_shellable.json').write_text(json.dumps(out))
                return out
    return {'n':n,'trials':trials,'prefixes':total,'best_gap':best,'seconds':time.time()-start}
if __name__=='__main__':
    Path('workspace/agent2_no_shedding_search.py').write_text(Path(__file__).read_text())
    for n in [9,10,11,12]:
        result=search(n,200)
        print(result,flush=True)
        if 'shelling' in result:break
