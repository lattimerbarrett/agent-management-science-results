from functools import lru_cache
from itertools import combinations

def bits(x):
    return [1<<i for i in range(x.bit_length()) if x>>i&1]
def maximal(fs):
    fs=set(fs)
    return tuple(sorted(f for f in fs if not any(f!=g and f&g==f for g in fs)))
def subsets(x, maxsize=None):
    bs=bits(x)
    for s in range(len(bs)+1 if maxsize is None else min(len(bs),maxsize)+1):
        for c in combinations(bs,s):
            yield sum(c)
def pure(fs):
    return len({f.bit_count() for f in fs})==1

def deletion(fs,s):
    return maximal([f for f in fs if f&s!=s]+[f^v for f in fs if f&s==s for v in bits(s)])
def link(fs,s):
    return maximal([f^s for f in fs if f&s==s])

@lru_cache(None)
def certificate(fs,k):
    fs=maximal(fs)
    if not pure(fs): return None
    if len(fs)==1: return ('simplex',fs[0])
    q=fs[0].bit_count()
    faces=set(s for f in fs for s in subsets(f,min(k+1,q)))
    for s in sorted(faces-{0},key=lambda x:(x.bit_count(),x)):
        de=deletion(fs,s)
        if not de or any(f.bit_count()!=q for f in de):continue
        cd=certificate(de,k)
        if cd is None:continue
        li=link(fs,s)
        cl=certificate(li,k)
        if cl is not None:return ('shed',s,cd,cl)
    return None

def verify(fs,k,c):
    fs=maximal(fs)
    assert pure(fs)
    if c[0]=='simplex':
        assert len(fs)==1 and c[1]==fs[0]
        return True
    _,s,cd,cl=c
    assert s and s.bit_count()<=k+1 and any(f&s==s for f in fs)
    de=deletion(fs,s)
    assert de and all(f.bit_count()==fs[0].bit_count() for f in de)
    assert verify(de,k,cd) and verify(link(fs,s),k,cl)
    return True

@lru_cache(None)
def shellable(fs):
    fs=maximal(fs)
    if len(fs)==1:return True
    q=fs[0].bit_count()
    for f in fs:
        rem=tuple(g for g in fs if g!=f)
        inter=maximal([f&g for g in rem])
        if all(h.bit_count()==q-1 for h in inter) and shellable(rem):return True
    return False

def completion(fs,n,k,max_states=100000):
    fs=maximal(fs); q=fs[0].bit_count()
    allf=set(sum(c) for c in combinations([1<<i for i in range(n)],q))
    visited=set()
    def dfs(cur):
        if set(cur)==allf:return []
        if cur in visited:return None
        visited.add(cur)
        if len(visited)>max_states:raise RuntimeError('search limit')
        for f in sorted(allf-set(cur)):
            nxt=tuple(sorted((*cur,f)))
            if certificate(nxt,k) is not None:
                ans=dfs(nxt)
                if ans is not None:return [f]+ans
        return None
    return dfs(fs),len(visited)
