from agent3_checker import *
for k in (0,1,3):
    fs=list(subsets(63,4)); tested=steps=0
    for sel in range(1,1<<len(fs)):
        facets=tuple(f for i,f in enumerate(fs) if sel>>i&1)
        union=0
        for f in facets: union|=f
        if union!=63: continue
        c=certificate(facets,k)
        if c is None: continue
        verify(facets,k,c); tested+=1
        path=completion(facets,k)
        assert path is not None
        cur=facets
        for f in path:
            assert f not in cur
            cur=tuple(sorted(cur+(f,)))
            verify(cur,k,certificate(cur,k)); steps+=1
        assert set(cur)==set(fs)
    print(k,tested,steps)
