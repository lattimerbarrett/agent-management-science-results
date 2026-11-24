"""Exact bitset verification of shift-graph reservoir examples; no networkx needed."""
from itertools import combinations
import json

def bits(x):
    while x:
        b=x&-x; yield b.bit_length()-1; x-=b

def build_and_check(m):
    V=list(combinations(range(m),2)); index={v:i for i,v in enumerate(V)}; r=len(V)
    E=[(index[i,j],index[j,k]) for i,j,k in combinations(range(m),3)]
    nf=r+2*len(E); q=max(m,r,2)
    scale=max(1,(nf+(1<<(q-2))-1)//(1<<(q-2)))
    D=scale*(1<<(q-2)); n=nf+15*D
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
        B=regions[region][1];rep=scale*(1<<(q-domain))
        for S in range(1<<domain):
            if (S>>left)&1 and not (S>>right)&1:
                for j in range(rep):join(v,B.start+S*rep+j)
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
    return dict(m=m,shift_vertices=r,shift_edges=len(E),vertices=n,edges=edges,D=D,min_degree=min(x.bit_count() for x in adj),triangle_free=True,C5_free=True,shift_in_odd_cube=True)

if __name__=='__main__':
    print(json.dumps([build_and_check(m) for m in (3,4,5)],indent=2))
