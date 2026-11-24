from pathlib import Path
# Export a short self-contained checker for inclusion in the answer.
source=r'''from itertools import combinations, product
from collections import Counter
from functools import lru_cache
from random import Random

def sk(W,q):
    return {frozenset(c) for c in combinations(sorted(W),q)}
def faces(fs):
    return set().union(*(sk(f,q) for f in fs for q in range(len(f)+1)))
def norm(fs):
    fs=set(fs)
    return frozenset(f for f in fs if not any(f<g for g in fs))

@lru_cache(None)
def certificate(fs,k):
    if len(fs)==1: return ()
    if not fs or len({len(f) for f in fs})!=1: return None
    q=len(next(iter(fs))); ff=faces(fs)
    for s in sorted((s for s in ff if 0<len(s)<=k+1),key=lambda s:(len(s),sorted(s))):
        D=norm(f for f in ff if not s<=f)
        if not D or any(len(f)!=q for f in D): continue
        L=norm(f-s for f in fs if s<=f)
        if certificate(D,k) is not None and certificate(L,k) is not None:
            return s,D,L
    return None

def prefix(fs,k):
    c=certificate(fs,k); assert c is not None
    if not c: return list(fs)
    s,D,L=c
    return prefix(D,k)+[s|h for h in prefix(L,k)]

def upper(fs,k,A):
    fs=norm(fs); d=len(next(iter(fs)))-1; V=set().union(*fs)
    assert len(A)==d-2 and not V.intersection(A)
    present=set(fs); order=[]
    def add(f):
        f=frozenset(f)
        if f not in present: present.add(f); order.append(f)
    if d==2:
        a=min(V); E=set().union(*(sk(f,2) for f in fs))
        N={a}|{v for v in V if frozenset((a,v)) in E}
        while N!=V:
            e=next(e for e in E if len(e&N)==1)
            u=next(iter(e&N)); v=next(iter(e-N))
            add((a,u,v)); E.add(frozenset((a,v))); N.add(v)
        for u,v in combinations(sorted(V-{a}),2): add((a,u,v))
    else:
        a=A[0]; S=norm(h for f in fs for h in sk(f,d))
        for h in prefix(S,k): add(h|{a})
        for h in upper(S,k,A[1:]): add(h|{a})
    for f in sk(V|set(A),d+1): add(f)
    return order

def check_upper(fs,k,A):
    fs=norm(fs); d=len(next(iter(fs)))-1; V=set().union(*fs)|set(A)
    assert certificate(fs,k) is not None
    order=upper(fs,k,A)
    for f in order:
        assert f not in fs
        fs=fs|{f}
        assert certificate(fs,k) is not None
    assert fs==frozenset(sk(V,d+1))
    return len(order)

T={frozenset(map(int,s)) for s in """058 137 125 129 289 169 018 038 379 578 029 023
016 234 458 136 014 567 459 157 346 026 268 267
123 349 468 056 579 149 079 147 247 378 258 356""".split()}

def seed():
    E=set().union(*(sk(t,2) for t in T)); tt=set(T)
    assert E==sk(range(10),2)
    assert all(sum(t<=Q for t in T)<=2 for Q in sk(range(10),4))
    collapses=[]
    while tt:
        choices=[(e,t) for e in sorted(E,key=lambda e:sorted(e))
                 for t in tt if e<t and sum(e<u for u in tt)==1]
        assert choices
        e,t=choices[0]; E.remove(e); tt.remove(t); collapses.append((e,t))
    reached={0}
    while True:
        new=reached|{v for e in E if e&reached for v in e}
        if new==reached: break
        reached=new
    assert len(E)==9 and len(reached)==10 and len(collapses)==36
    return E,collapses

def check_lower(d):
    tree,collapses=seed(); B=[set(range(d*v,d*(v+1))) for v in range(10)]
    q=d+1; first=min(tree,key=lambda e:sorted(e))
    present=sk(set().union(*(B[v] for v in first)),q)
    ridges=Counter(h for f in present for h in sk(f,d))
    def add(new):
        assert not(new&present)
        for f in new:
            for h in sk(f,d): ridges[h]+=1
        present.update(new)
    reached=set(first); vs=es=0
    while len(reached)<10:
        u,v=next((next(iter(e&reached)),next(iter(e-reached)))
                 for e in tree if len(e&reached)==1)
        old=set()
        for x in sorted(B[v]):
            L=sk(B[u]|old,d); new={h|{x} for h in L}
            assert all(h in ridges for h in L)
            add(new); old.add(x); vs+=1
        reached.add(v)
    for e,t in reversed(collapses):
        a,b=sorted(e); c=next(iter(t-e)); A,Bb,C=B[a],B[b],B[c]
        allowed=set(); region=sk(A|Bb|C,q)
        for x,y in product(sorted(A),sorted(Bb)):
            edge=frozenset((x,y)); allowed.add(edge)
            new={f for f in region if edge<=f and all(
                frozenset((aa,bb)) in allowed for aa in f&A for bb in f&Bb)}
            assert new
            assert all(f-{x} in ridges and f-{y} in ridges for f in new)
            L={f-edge for f in new}; X={h-C for h in L}
            assert L=={h|z for h in X for z in sk(C,d-1-len(h))}
            assert all(g in X for h in X for j in range(len(h)+1) for g in sk(h,j))
            add(new); es+=1
    expected=set().union(*(sk(set().union(*(B[v] for v in t)),q) for t in T))
    assert present==expected
    print('lower',d,len(present),'facets;',vs,'vertex steps;',es,'edge steps')

def check_patterns(d):
    count=0
    for s in (3,4):
        for P in sk(range(10),s):
            if s==3 and P in T: continue
            P=sorted(P)
            for counts in product(range(1,d+1),repeat=s):
                if not 4<=sum(counts)<=d+1: continue
                R={v for v,c in zip(P,counts) if c==1 and
                   (s==3 or frozenset(set(P)-{v}) in T)}
                assert len(R)<=2
                count+=1
    print('buffer patterns',d,count)

if __name__=='__main__':
    count=steps=0; ff=list(sk(range(5),3))
    for mask in range(1,1<<len(ff)):
        fs=frozenset(f for j,f in enumerate(ff) if mask>>j&1)
        for k in (1,2):
            if certificate(fs,k) is not None:
                steps+=check_upper(fs,k,[]); count+=1
    print('upper exhaustive:',count,'inputs;',steps,'additions')
    rng=Random(20260401)
    for d,n,trials in [(3,6,40),(4,6,12)]:
        ff=sorted(sk(range(n),d+1),key=lambda f:sorted(f)); count=steps=0
        for _ in range(trials):
            fs=frozenset(rng.sample(ff,rng.randrange(1,len(ff)+1)))
            if certificate(fs,1) is not None:
                steps+=check_upper(fs,1,list(range(n,n+d-2)));count+=1
        print('upper sampled:',d,count,'inputs;',steps,'additions')
    for d in (3,4,5): check_lower(d)
    for d in range(3,11): check_patterns(d)
'''
Path('workspace/compact_complete_agent1.py').write_text(source)
exec(compile(source,'compact_complete_agent1.py','exec'),{'__name__':'__main__'})
