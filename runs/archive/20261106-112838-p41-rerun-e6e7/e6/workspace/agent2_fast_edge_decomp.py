import functools,itertools,json,time
from pathlib import Path

def bitlist(x):
    out=[]
    while x:
        v=x&-x;out.append(v);x-=v
    return out
@functools.lru_cache(None)
def edge_decomp(fs):
    if len(fs)<=1:return True
    size=fs[0].bit_count()
    if size<=1:return True
    if size==2:
        vs=0
        for f in fs:vs|=f
        reach=vs&-vs
        while True:
            new=reach
            for f in fs:
                if f&reach:new|=f
            if new==reach:return reach==vs
            reach=new
    owners={};candidates=set()
    for f in fs:
        bs=bitlist(f)
        candidates.update(bs)
        candidates.update(x|y for x,y in itertools.combinations(bs,2))
        for v in bs:
            r=f^v;owners.setdefault(r,[]).append(f)
    blocked=set()
    for r,own in owners.items():
        if len(own)==1:
            f=own[0];v=f^r
            blocked.add(v)
            blocked.update(v|u for u in bitlist(r))
    candidates-=blocked
    candidates=sorted(candidates,key=lambda s:(s.bit_count(),sum(f&s==s for f in fs)),reverse=True)
    for s in candidates:
        dfs=tuple(f for f in fs if f&s!=s)
        lfs=tuple(sorted(f^s for f in fs if f&s==s))
        if edge_decomp(lfs) and edge_decomp(dfs):return True
    return False
if __name__=='__main__':
    Path('workspace/agent2_fast_edge_decomp.py').write_text(Path(__file__).read_text())
    for name in ['ZieglerBall','BarnetteSphere','BrucknerGrunbaumSphere']:
        fs=tuple(json.loads(Path('workspace/agent2_'+name+'.json').read_text())['facets'])
        t=time.time();o=edge_decomp(fs)
        print(name,'edge-decomp',o,'seconds',time.time()-t,'cache',edge_decomp.cache_info(),flush=True)
