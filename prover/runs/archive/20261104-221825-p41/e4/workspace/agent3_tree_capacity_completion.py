"""Conditional completion: old tree pure in target; leaf capacities >= ranks.
All output witnesses are constructed. This module does NOT assert every input
has a tree satisfying those unproved conditions.
"""
from functools import lru_cache
from agent3_checker import subsets
from agent2_vertex_completion import certified_completion

def normalize(U,N,r):
    N=set(N)
    assert 0 not in N
    loops=0
    for s in N:
        if s.bit_count()==1:loops|=s
    U &= ~loops
    N={s for s in N if s&U==s and s.bit_count()<=r}
    N=tuple(sorted(s for s in N if not any(t!=s and t&s==t for t in N)))
    return U,N

@lru_cache(None)
def facets(U,N,r):
    U,N=normalize(U,N,r)
    return tuple(sorted(f for f in subsets(U,r) if not any(f&s==s for s in N)))

def score(U,N,r):
    U,N=normalize(U,N,r)
    parent={v:v for v in subsets(U,1)}
    def find(v):
        while parent[v]!=v:v=parent[v]
        return v
    for s in N:
        bs=list(subsets(s,1));a=find(bs[0])
        for b in bs[1:]:parent[find(b)]=a
    comps={}
    for v in parent:comps.setdefault(find(v),[]).append(v)
    out=0
    for comp in comps.values():
        mask=sum(comp);ns=[s for s in N if s&mask]
        out+=min(s.bit_count()-1 for s in ns) if ns else len(comp)
    return out

_checked={}
def verify_cached(fs,k,c):
    key=(fs,k,id(c))
    if key in _checked:return True
    assert fs and len({f.bit_count() for f in fs})==1
    if c[0]=='simplex':assert fs==(c[1],)
    else:
        assert c[0]=='shed';s=c[1]
        assert 1<=s.bit_count()<=k+1
        inside=tuple(f for f in fs if f&s==s)
        D=tuple(f for f in fs if f&s!=s)
        assert inside and D
        covered={f^v for f in D for v in subsets(f,1)}
        assert all(f^v in covered for f in inside for v in subsets(s,1))
        L=tuple(sorted(f^s for f in inside))
        verify_cached(D,k,c[2]);verify_cached(L,k,c[3])
    _checked[key]=c
    return True

def capacity_completion(U,N,r,W):
    U,N=normalize(U,N,r)
    T=facets(U,N,r)
    assert W in T and score(U,N,r)>=r
    if not N:return certified_completion((W,),('simplex',W),U)
    s=N[0];v=next(subsets(s&~W,1))
    nd=tuple(n for n in N if not n&v)
    nl=tuple(n&~v for n in N)
    out=list(capacity_completion(U^v,nd,r,W))
    dc=out[-1][1] if out else ('simplex',W)
    L=facets(U^v,nl,r-1);S=L[0]
    out.append((v|S,('shed',v,dc,('simplex',S))))
    for g,gc in capacity_completion(U^v,nl,r-1,S):
        out.append((v|g,('shed',v,dc,gc)))
    cur=(W,)
    for f,c in out:
        assert f not in cur and f in T
        cur=tuple(sorted(cur+(f,)));verify_cached(cur,0,c)
    assert cur==T
    return tuple(out)

def conditional_completion(fs,k,c,U=None,N=()):
    fs=tuple(sorted(fs));r=fs[0].bit_count()
    if U is None:
        U=0
        for f in fs:U|=f
    U,N=normalize(U,N,r);T=facets(U,N,r)
    assert set(fs)<=set(T)
    if c[0]=='simplex':
        assert fs==(c[1],)
        assert score(U,N,r)>=r,('UNPROVED leaf condition fails',U,N,r)
        out=capacity_completion(U,N,r,c[1])
    else:
        s=c[1]
        D=tuple(f for f in fs if f&s!=s)
        L=tuple(sorted(f^s for f in fs if f&s==s))
        TD=tuple(f for f in T if f&s!=s)
        covered={f^v for f in TD for v in subsets(f,1)}
        assert all(f^v in covered for f in T if f&s==s for v in subsets(s,1)),('UNPROVED purity condition fails',s)
        out=[]
        dc=c[2]
        for f,fc in conditional_completion(D,k,c[2],U,tuple(N)+(s,)):
            dc=fc;out.append((f,('shed',s,dc,c[3])))
        for f,fc in conditional_completion(L,k,c[3],U&~s,tuple(n&~s for n in N)):
            out.append((s|f,('shed',s,dc,fc)))
        out=tuple(out)
    cur=fs
    for f,fc in out:
        assert f not in cur and f in T
        cur=tuple(sorted(cur+(f,)));verify_cached(cur,k,fc)
    assert cur==T
    return tuple(out)
