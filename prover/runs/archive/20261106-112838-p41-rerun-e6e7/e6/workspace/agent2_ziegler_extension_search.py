import sys,itertools,time,functools,json
from pathlib import Path
sys.path.insert(0,'workspace')
from agent2_fast_edge_decomp import edge_decomp,bitlist

@functools.lru_cache(None)
def shelling(fs):
    if len(fs)<=1:return fs
    ridgecount={}
    for f in fs:
        for v in bitlist(f):
            r=f^v;ridgecount[r]=ridgecount.get(r,0)+1
    for f in fs:
        r=sum(v for v in bitlist(f) if ridgecount[f^v]>1)
        if not r or any(g!=f and g&r==r for g in fs):continue
        dfs=tuple(g for g in fs if g!=f)
        order=shelling(dfs)
        if order is not None:return order+(f,)
    return None
if __name__=='__main__':
    Path('workspace/agent2_ziegler_extension_search.py').write_text(Path(__file__).read_text())
    fs=tuple(json.loads(Path('workspace/agent2_ZieglerBall.json').read_text())['facets'])
    t=time.time();print('Ziegler shellable?',shelling(fs) is not None,'cache',shelling.cache_info(),flush=True)
    positives=0
    for idx,c in enumerate(itertools.combinations(range(10),4)):
        f=sum(1<<i for i in c)
        if f in fs:continue
        gs=tuple(sorted(fs+(f,)));order=shelling(gs)
        if order is None:continue
        positives+=1
        kd=edge_decomp(gs)
        print('shellable extension',f,'edge-decomp',kd,'seconds',time.time()-t,flush=True)
        if not kd:
            out={'facets':gs,'shelling':order,'newfacet':f}
            Path('workspace/agent2_shellable_nonedge3.json').write_text(json.dumps(out));break
    print('total shellable extension',positives,'seconds',time.time()-t,'cache',shelling.cache_info())
