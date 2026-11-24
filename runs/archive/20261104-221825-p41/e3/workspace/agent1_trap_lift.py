"""Exact verification and dimension lifting of the 20-vertex shelling trap.
Needs the team certificate file. Uses the independently verified k=1 base certificate.
"""
from itertools import combinations
import json
from agent3_check import all_faces
from collections import Counter
_checked={}
def check_certificate(F,k,c):
    key=(F,k,id(c))
    if key in _checked:return _checked[key][1]
    if c[0]=='simplex':return len(F)==1 and F[0]==c[1]
    _,s,dc,lc=c
    if not F or not s or s.bit_count()>k+1:return False
    q=F[0].bit_count()
    if any(f.bit_count()!=q for f in F):return False
    D=tuple(f for f in F if f&s!=s)
    containing=tuple(f for f in F if f&s==s)
    if not D or not containing:return False
    counts=Counter(f^(1<<v) for f in F for v in range(f.bit_length()) if f>>v&1)
    if any(counts[f^(1<<v)]==1 for f in containing for v in range(s.bit_length()) if s>>v&1):return False
    L=tuple(sorted(f^s for f in containing))
    ans=check_certificate(D,k,dc) and check_certificate(L,k,lc)
    _checked[key]=(c,ans)
    return ans

def boundary_extend(F,f,k,c):
    if c[0]=='simplex':
        assert F[0].bit_count()==1 and f.bit_count()==1
        return ('shed',f,c,('simplex',0))
    _,s,dc,lc=c
    if f&s!=s:
        D=tuple(g for g in F if g&s!=s)
        return ('shed',s,boundary_extend(D,f,k,dc),lc)
    L=tuple(sorted(g^s for g in F if g&s==s))
    return ('shed',s,dc,boundary_extend(L,f^s,k,lc))

def choose_masks(n,q):
    return (sum(1<<v for v in c) for c in combinations(range(n),q))
def vertices(F):
    W=0
    for f in F:W|=f
    return W

def appendable_from_faces(H,face,q):
    # The vertex set of omitted vertices of old ridges is the restriction face.
    restriction=sum(1<<v for v in range(face.bit_length()) if face>>v&1 and (face^(1<<v)) in H)
    return restriction not in H

def verify_trap(F,n,q):
    F=set(F);assert F and all(f.bit_count()==q for f in F)
    assert vertices(F)==(1<<n)-1
    H=all_faces(tuple(F));missing=0
    for f in choose_masks(n,q):
        if f in F:continue
        assert not appendable_from_faces(H,f,q),f
        missing+=1
    return missing

def full_boundaries(F,n,q):
    F=set(F)
    return tuple(s for s in choose_masks(n,q+1) if all((s^(1<<v)) in F for v in range(n) if s>>v&1))

def cone_certificate(c,a):
    if c[0]=='simplex':return ('simplex',c[1]|a)
    _,s,dc,lc=c
    return ('shed',s,cone_certificate(dc,a),cone_certificate(lc,a))

def lift(F,c,k,n):
    q=F[0].bit_count();a=1<<n
    B=full_boundaries(F,n,q)
    cur=tuple(sorted(f|a for f in F));c=cone_certificate(c,a)
    assert check_certificate(cur,k,c)
    for f in B:
        c=boundary_extend(cur,f,k,c);cur=tuple(sorted(cur+(f,)))
        assert check_certificate(cur,k,c)
    return cur,c,B

if __name__=='__main__':
    data=json.load(open('workspace/agent2_corridor_trap_K1_certified.json'))
    F=tuple(data['facets']);c=data['k1certificate'];k=1;n=20;q=4
    assert check_certificate(F,k,c)
    initial=F;B0=full_boundaries(F,n,q);assert len(B0)==7
    assert not full_boundaries(B0,n,q+1)
    apices=0
    for r in range(5):
        expected=set(f|apices for f in initial)
        for a in (1<<v for v in range(20,20+r)):
            expected.update(b|(apices^a) for b in B0)
        assert set(F)==expected
        assert len(F)==173+7*r
        if r<=3:assert set(full_boundaries(F,n,q))==set(b|apices for b in B0)
        missing=verify_trap(F,n,q)
        print('dimension',q-1,'vertices',n,'facets',len(F),'missing checked',missing,flush=True)
        if r<4:
            F,c,B=lift(F,c,k,n);apices|=1<<n;n+=1;q+=1
