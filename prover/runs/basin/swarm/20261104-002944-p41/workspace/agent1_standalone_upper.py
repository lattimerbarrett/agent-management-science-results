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

if __name__=='__main__':
    checked=0
    for n in range(3,6):
        ff=choose((1<<n)-1,3)
        for mask in range(1,1<<len(ff)):
            fs=tuple(f for i,f in enumerate(ff) if mask>>i&1)
            if kd(fs,1) is not None:
                complete(fs,1,[]);checked+=1
    print('2D complexes verified:',checked)
    for fs in [(15,),(15,30),(15,23,27,29),(31,),(31,62)]:
        d=fs[0].bit_count()-1;n=max(fs).bit_length()
        out=complete(fs,1,[1<<(n+i) for i in range(d-2)])
        print('dimension',d,'initial',fs,'verified additions',len(out))
