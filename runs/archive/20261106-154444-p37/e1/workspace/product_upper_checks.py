"""Exact finite checks of the product upper-bound reversible-set proof.
No external packages required. Run directly, or import run_checks().
"""
from itertools import permutations, combinations

def closure(n, edges):
    le = [[i==j for j in range(n)] for i in range(n)]
    for i,j in edges: le[i][j]=True
    for k in range(n):
        for i in range(n):
            if le[i][k]:
                for j in range(n): le[i][j] |= le[k][j]
    return tuple(map(tuple, le))

def critical(le):
    n=len(le)
    return [(x,y) for x in range(n) for y in range(n)
            if not le[x][y] and not le[y][x]
            and all(not le[z][x] or z==x or le[z][y] for z in range(n))
            and all(not le[y][z] or z==y or le[x][z] for z in range(n))]

def extensions(le):
    out=[]
    for p in permutations(range(len(le))):
        rank={v:i for i,v in enumerate(p)}
        if all(not le[x][y] or rank[x]<=rank[y] for x in rank for y in rank): out.append(rank)
    return out

def realizer(le):
    cp=critical(le)
    ex=extensions(le)
    for t in range(1,len(ex)+1):
        for inds in combinations(range(len(ex)),t):
            if all(any(ex[i][x]>ex[i][y] for i in inds) for x,y in cp):
                return [ex[i] for i in inds]

def acyclic_reversals(le, pairs):
    n=len(le)
    adj=[set(j for j in range(n) if i!=j and le[i][j]) for i in range(n)]
    for x,y in pairs: adj[y].add(x)
    indeg=[0]*n
    for row in adj:
        for y in row: indeg[y]+=1
    todo=[v for v in range(n) if indeg[v]==0]; count=0
    while todo:
        v=todo.pop(); count+=1
        for w in adj[v]:
            indeg[w]-=1
            if indeg[w]==0: todo.append(w)
    return count==n

def suitable(m):
    ps=[{v:i for i,v in enumerate(p)} for p in permutations(range(m))]
    req=[(x,y,z) for x,y,z in permutations(range(m),3)]
    for d in range(1,len(ps)+1):
        for inds in combinations(range(len(ps)),d):
            if all(any(ps[i][x]>max(ps[i][y],ps[i][z]) for i in inds) for x,y,z in req):
                return [ps[i] for i in inds]

def check_product(le, sigmas):
    n=len(le); m=len(sigmas[0]); rs=realizer(le); t=len(rs)
    qs=[frozenset([v]) for v in range(m)]+[frozenset(e) for e in combinations(range(m),2)]
    elems=[(p,q) for p in range(n) for q in qs]
    prod=tuple(tuple(le[p][r] and q<=s for r,s in elems) for p,q in elems)
    cp=critical(prod); cpP=set(critical(le))
    pure=[[] for _ in range(t-1)]; mixed=[[] for _ in sigmas]
    for a,b in cp:
        p,q=elems[a]; r,e=elems[b]
        assert len(q)==1 and len(e)==2
        v=next(iter(q))
        if v in e:
            assert not le[p][r]
            col=next(i for i,R in enumerate(rs) if R[p]>R[r])
            if col<t-1: pure[col].append((a,b))
            else:
                j=next(j for j,s in enumerate(sigmas) if s[v]==max(s[w] for w in e))
                mixed[j].append((a,b))
        else:
            assert all(not le[z][p] or z==p for z in range(n))
            assert all(not le[r][z] or z==r for z in range(n))
            j=next(j for j,s in enumerate(sigmas) if s[v]>max(s[w] for w in e))
            mixed[j].append((a,b))
    assert sum(map(len,pure+mixed))==len(cp)
    assert all(acyclic_reversals(prod, C) for C in pure+mixed)
    return t,len(cp)

def run_checks():
    sigmas=suitable(4)
    assert len(sigmas)==3
    count=0; cps=0
    for n in range(1,5):
        edges=list(combinations(range(n),2)); seen=set()
        for mask in range(1<<len(edges)):
            le=closure(n,[e for i,e in enumerate(edges) if mask>>i&1])
            if le in seen: continue
            seen.add(le)
            t,c=check_product(le,sigmas); count+=1;cps+=c
    # Standard example S_3, dimension three (not included above).
    le=closure(6,[(i,3+j) for i in range(3) for j in range(3) if i!=j])
    t,c=check_product(le,sigmas); assert t==3
    count+=1; cps+=c
    print('Verified',count,'posets times Q_4;',cps,'critical pairs covered and every color acyclic.')
    print('Three suitable vertex orders:',[sorted(s,key=s.get) for s in sigmas])

if __name__=='__main__': run_checks()
