import itertools,json,pathlib
from sage.all import Matrix,GF

def homology_cocycle_cuts(n,triangles,p):
    '''Necessary clauses for simply connected/fullgraph complexes, encoded as triangle masks.
    Each returned list is a disjunction: at least one listed triangle must become present.
    Gauge-fix every edge from vertex0 to zero; nonzero cocycles then are non-coboundaries.
    '''
    triangles=set(triangles);edges=list(itertools.combinations(range(1,n),2));E={e:i for i,e in enumerate(edges)}
    tris=list(itertools.combinations(range(n),3));rows=[]
    for a,b,c in tris:
        mask=(1<<a)|(1<<b)|(1<<c)
        if mask not in triangles:continue
        row=[0]*len(edges)
        for x,y,sign in [(b,c,1),(a,c,-1),(a,b,1)]:
            if x:row[E[x,y]]=sign%p
        rows.append(row)
    A=Matrix(GF(p),rows,ncols=len(edges))
    cuts=[]
    for z in A.right_kernel().basis():
        cut=[]
        for a,b,c in tris:
            t=(1<<a)|(1<<b)|(1<<c)
            hol=z[E[b,c]]-(z[E[a,c]] if a else 0)+(z[E[a,b]] if a else 0)
            if hol:
                assert t not in triangles;cut.append(t)
        assert cut;cuts.append(cut)
    return cuts

if __name__=='__main__':
    data=json.load(open('workspace/agent3_locallyflag_12.json'))
    print('data type',type(data),str(data)[:160])
    F=data['facets'] if isinstance(data,dict) else data
    if not isinstance(F[0],int):F=[sum(1<<x for x in f) for f in F]
    n=max(f.bit_length() for f in F)
    T={f^(1<<x) for f in F for x in range(n) if f>>x&1}
    for p in [2,3,5]:
        cuts=homology_cocycle_cuts(n,T,p)
        print('p',p,'cocyclecuts',len(cuts),'lengths',list(map(len,cuts)))
    pathlib.Path('workspace/agent2_homology_cuts.py').write_text(pathlib.Path(__file__).read_text())
