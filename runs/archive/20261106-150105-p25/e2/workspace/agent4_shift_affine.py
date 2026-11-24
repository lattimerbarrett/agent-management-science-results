"""Exact bitset verification of shift-graph reservoir examples; no networkx needed."""
from itertools import combinations
import json

def bits(x):
    while x:
        b=x&-x; yield b.bit_length()-1; x-=b

def build_and_check(m):
    V=list(combinations(range(m),2)); index={v:i for i,v in enumerate(V)}; r=len(V)
    E=[(index[i,j],index[j,k]) for i,j,k in combinations(range(m),3)]
    nf=r+2*len(E); q=max(1,(max(m,r)-1).bit_length())
    D0=1<<(q-1); scale=(nf+D0-1)//D0
    D=scale*D0; n=nf+15*D
    adj=[0]*n
    def join(u,v):adj[u]|=1<<v;adj[v]|=1<<u
    for t,(u,v) in enumerate(E):
        a=r+2*t;b=a+1
        join(u,a);join(a,b);join(b,v)
    start=nf; regions=[]
    for i in range(3):
        A=range(start,start+D);B=range(start+D,start+5*D);start+=5*D
        amask=sum(1<<a for a in A);bmask=sum(1<<b for b in B)
        for a in A:adj[a]|=bmask
        for b in B:adj[b]|=amask
        regions.append((A,B))
    def attach(v,region,domain,left,right):
        # Palette colors are pairwise-independent affine GF(2) cuts.
        B=regions[region][1]
        for a in range(1<<q):
            for b in range(2):
                l=((a&left).bit_count()&1)^b
                h=((a&right).bit_count()&1)^b
                if l==1 and h==0:
                    S=2*a+b
                    for j in range(scale):join(v,B.start+S*scale+j)
    for u,(i,j) in enumerate(V):attach(u,0,m,i,j)
    for t,(u,v) in enumerate(E):
        attach(r+2*t,1,r,u,v);attach(r+2*t+1,2,r,u,v)
    assert min(x.bit_count() for x in adj)>=D
    assert 16*D>=n
    # Exact triangles: no adjacent pair has a common neighbor.
    # Exact closed walks length5: no adjacent pair has a common length2 endpoint.
    two=[]
    for row in adj:
        out=0
        for u in bits(row):out|=adj[u]
        two.append(out)
    edges=0
    for u,row in enumerate(adj):
        for v in bits(row>>u):
            v+=u
            assert not adj[u]&adj[v],('C3',u,v)
            assert not two[u]&two[v],('C5',u,v)
            edges+=1
    for t,(u,v) in enumerate(E):
        a=r+2*t;b=a+1
        assert adj[u]>>a&1 and adj[a]>>b&1 and adj[b]>>v&1
    return dict(m=m,palette_size=1<<(q+1),shift_vertices=r,shift_edges=len(E),vertices=n,edges=edges,D=D,min_degree=min(x.bit_count() for x in adj),triangle_free=True,C5_free=True,shift_in_odd_cube=True)

def check_shift_chromatic(m):
    import z3
    V=list(combinations(range(m),2));index={v:i for i,v in enumerate(V)}
    E=[(index[i,j],index[j,k]) for i,j,k in combinations(range(m),3)]
    k=(m-1).bit_length()
    # Explicit upper coloring: index of most significant differing binary digit.
    color=[(i^j).bit_length()-1 for i,j in V]
    assert max(color)<k
    assert all(color[u]!=color[v] for u,v in E)
    # Exact solver proves no (k-1)-coloring for these concrete graphs.
    s=z3.Solver();x=[z3.Int('x%d'%i) for i in range(len(V))]
    s.add(*[z3.And(t>=0,t<k-1) for t in x])
    s.add(*[x[u]!=x[v] for u,v in E])
    assert s.check()==z3.unsat
    # Verify all outgoing color sets distinct (general lower-bound proof invariant).
    masks=[sum(1<<c for c in {color[index[i,j]] for j in range(i+1,m)}) for i in range(m)]
    assert len(set(masks))==m
    return k

if __name__=='__main__':
    results=[]
    for m in range(3,10):
        report=build_and_check(m)
        report['shift_chromatic_number']=check_shift_chromatic(m)
        results.append(report)
    print(json.dumps(results,indent=2))
