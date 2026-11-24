from itertools import combinations
from functools import lru_cache

def bits(x):
    return [1 << i for i in range(x.bit_length()) if x >> i & 1]

def choose(x, q):
    return [sum(t) for t in combinations(bits(x), q)]

def maximal(fs):
    fs=set(fs)
    return tuple(sorted(f for f in fs if not any(f != g and f & g == f for g in fs)))

def deletion(fs,s):
    return maximal([f for f in fs if f&s != s] +
                   [f^v for f in fs if f&s == s for v in bits(s)])

def link(fs,s):
    return maximal(f^s for f in fs if f&s == s)

@lru_cache(None)
def kd(fs,k):
    if not fs or len({f.bit_count() for f in fs}) != 1: return None
    if len(fs)==1: return ('simplex',fs[0])
    q=fs[0].bit_count()
    faces=set(s for f in fs for r in range(1,min(k+1,q)+1) for s in choose(f,r))
    for s in sorted(faces,key=lambda s:(s.bit_count(),s)):
        D=deletion(fs,s)
        if not D or any(f.bit_count()!=q for f in D):continue
        cd=kd(D,k)
        if cd is None:continue
        cl=kd(link(fs,s),k)
        if cl is not None:return ('shed',s,cd,cl)
    return None

def prefix(c):
    if c[0]=='simplex':return [c[1]]
    return prefix(c[2])+[c[1]|h for h in prefix(c[3])]

def complete(fs,k,fresh):
    fs=maximal(fs);start=set(fs)
    assert kd(fs,k) is not None
    d=fs[0].bit_count()-1
    assert d>=2 and len(fresh)==d-2
    V=0
    for f in fs:V|=f
    assert all(v&(V|sum(fresh[:i]))==0 for i,v in enumerate(fresh))
    out=[]
    def add(F):
        nonlocal fs
        assert F not in fs and F.bit_count()==d+1
        fs=maximal((*fs,F));out.append(F)
        assert kd(fs,k) is not None
    if d==2:
        while True:
            E=set(e for f in fs for e in choose(f,2))
            cand=[u|v|w for u,v in combinations(bits(V),2) if u|v not in E
                  for w in bits(V^(u|v)) if u|w in E and v|w in E]
            if not cand:break
            add(cand[0])
        assert len(E)==len(choose(V,2))
        for F in choose(V,3):
            if F not in fs:add(F)
    else:
        a=fresh[0];G=maximal(h for f in fs for h in choose(f,d))
        for h in prefix(kd(G,k)):add(a|h)
        for h in complete(G,k,fresh[1:]):add(a|h)
        U=V|sum(fresh[1:])
        for F in choose(U,d+1):
            if F not in fs:add(F)
    U=V|sum(fresh)
    assert set(fs)==set(choose(U,d+1)) and len(out)==len(set(out))
    assert set(out)==set(fs)-start
    return out


# Independent, iterative verification of a complete k-decomposition certificate.
def verify(fs,k,c):
    stack=[(set(fs),c)];nodes=0
    while stack:
        F,c=stack.pop();assert F
        p=next(iter(F)).bit_count()
        assert all(f.bit_count()==p for f in F)
        counts={}
        for f in F:
            for v in bits(f):counts[f^v]=counts.get(f^v,0)+1
        while True:
            nodes+=1
            if c[0]=='simplex':
                assert F=={c[1]};break
            _,s,cd,cl=c
            assert s and s.bit_count()<=k+1
            removed=[f for f in F if f&s==s]
            assert removed
            L={f^s for f in removed}
            for f in removed:
                F.remove(f)
                for v in bits(f):counts[f^v]-=1
            assert F
            for f in removed:
                for v in bits(s):assert counts.get(f^v,0)>0
            stack.append((L,cl));c=cd
    return nodes

@lru_cache(None)
def uniform(U,q):
    assert 0<=q<=U.bit_count()
    if q==0:return ('simplex',0)
    if U.bit_count()==q:return ('simplex',U)
    v=U&-U
    return ('shed',v,uniform(U^v,q),uniform(U^v,q-1))

BASE='012 023 124 234 015 145 035 356 567 346 457 347 146 167 137 017 047 046 026 256 027'
B=[tuple(map(int,t)) for t in BASE.split()]
S=set(B)|{(1,2,7)}

def seed_checks():
    oldE=set();oldV=set();restrictions=[]
    for i,F in enumerate(B):
        e=set(combinations(F,2));nv=set(F)-oldV;ne=e-oldE
        if i==0:assert len(F)==3
        elif nv:
            assert len(nv)==1 and len(ne)==2
            assert all(next(iter(nv)) in a for a in ne)
            restrictions.append(tuple(nv))
        else:
            assert len(ne)==1
            restrictions.append(next(iter(ne)))
        oldE|=e;oldV|=set(F)
    assert oldV==set(range(8)) and len(oldE)==28
    assert (0,1,3) not in S and len(S)==22
    hist={j:0 for j in range(5)}
    for F in combinations(range(8),4):
        hist[sum(t in S for t in combinations(F,3))]+=1
    assert hist=={0:9,1:14,2:46,3:0,4:1}
    return restrictions,hist

def lower(q):
    # A rank-q edge-decomposable obstruction on 8q vertices.
    assert q>=4
    R,hist=seed_checks();m=q
    X=[sum(1<<(m*v+j) for j in range(m)) for v in range(8)]
    def cluster_union(F):return sum(X[v] for v in F)
    U=cluster_union(B[0]);fs=set(choose(U,q));c=uniform(U,q)
    phases=0
    for F,R in zip(B[1:],R):
        s=len(R)
        for inds in sorted(__import__('itertools').product(range(m),repeat=s),reverse=True):
            sig=sum(1<<(m*v+i) for v,i in zip(R,inds))
            U=cluster_union(set(F)-set(R))
            U|=sum(1<<(m*v+j) for v,i in zip(R,inds) for j in range(i+1,m))
            new={sig|h for h in choose(U,q-s)}
            assert not fs&new
            fs|=new;c=('shed',sig,c,uniform(U,q-s));phases+=1
    expected={h for F in B for h in choose(cluster_union(F),q)}
    assert fs==expected
    nodes=verify(fs,1,c)
    actualE={e for f in fs for e in choose(f,2)}
    actualT={t for f in fs for t in choose(f,3)}
    V=(1<<(8*m))-1
    assert actualE==set(choose(V,2))
    def allowed(t):
        P=tuple(sorted({i//m for i in range(8*m) if t>>i&1}))
        return len(P)<=2 or P in S
    barrier={t for t in choose(V,3) if allowed(t)}
    assert actualT<=barrier
    witness=(1<<0)|(1<<m)|(1<<(3*m))
    assert witness not in barrier
    assert all(sum(t in barrier for t in choose(f,3))!=3 for f in choose(V,4))
    return len(fs),nodes,phases,len(actualT),len(barrier)

if __name__=='__main__':
    checked=0
    for n in range(3,6):
        ff=choose((1<<n)-1,3)
        for mask in range(1,1<<len(ff)):
            fs=tuple(f for i,f in enumerate(ff) if mask>>i&1)
            if kd(fs,1) is not None:
                complete(fs,1,[]);checked+=1
    print('Upper: verified 2D input cases:',checked)
    for fs in [(15,), (15,30), (15,23,27,29), (31,), (31,62)]:
        d=fs[0].bit_count()-1;n=max(fs).bit_length()
        out=complete(fs,1,[1<<(n+i) for i in range(d-2)])
        print('Upper: dimension',d,'initial',fs,'verified additions',len(out))
    print('Lower: base barrier histogram',seed_checks()[1])
    for q in [4,5]:
        print('Lower: rank',q,'facets,nodes,phases,triangles,barrier:',lower(q))
