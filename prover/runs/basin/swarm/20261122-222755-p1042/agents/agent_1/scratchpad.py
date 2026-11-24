from sage.all import ZZ, matrix
from itertools import combinations, product
from math import comb
from collections import Counter
import heapq

def C(n,k):
    return comb(n,k) if 0 <= k <= n else 0

def predicted(m):
    return (C(m,4)-C(m,3),
            1+2*m+4*C(m,2)+4*C(m,3)+2*C(m,4))

def invariants(M):
    d = [abs(int(x)) for x in M.elementary_divisors()]
    rank = sum(x != 0 for x in d)
    return M.nrows()-rank, M.ncols()-rank, [x for x in d if x > 1]

def coefficient(v,S,e,m):
    choices = dict(zip(S,e))
    ans = 1
    for j in range(m):
        x = v.get(j,4)
        if x == 1:
            ans = -ans
        elif x != choices.get(j,4):
            return 0
    return ans

def Fmatrix(m):
    columns = [(S,e) for s in range(5)
               for S in combinations(range(m),s)
               for e in product((2,3),repeat=s)]
    targets = []
    for i in (1,2,3):
        c = min({1,2,3}-{i})
        targets += [dict.fromkeys(U,i) for U in combinations(range(m),3)]
        for V in combinations(range(m),4):
            targets.append(dict.fromkeys(V,i))
            for j in V:
                v = dict.fromkeys(V,i); v[j] = c
                targets.append(v)
    entries = {}
    for a,v in enumerate(targets):
        for b,(S,e) in enumerate(columns):
            x = coefficient(v,S,e,m)
            if x: entries[a,b] = x
    return matrix(ZZ,len(targets),len(columns),entries)

def check_local():
    for k in range(1,5):
        subsets = [S for r in range(max(0,k-2),min(k,2)+1)
                   for S in combinations(range(k),r)]
        H = matrix(ZZ, [[1]*len(subsets)] +
                   [[int(j in S) for S in subsets] for j in range(k)])
        d = [x for x in H.elementary_divisors() if x]
        assert d == [1]*(k+1 if k<4 else 4)
        if k==4: assert matrix(ZZ,[[-2,1,1,1,1]])*H == 0

def check_bier(m):
    levels = {s:list(combinations(range(m),s)) for s in range(5)}
    standard = lambda A: all(a+1>=2*(j+1) for j,a in enumerate(A))
    std = [A for s in range(min(4,m-4)+1) for A in levels[s] if standard(A)]
    incidence = lambda rows,cols: matrix(ZZ,[[int(set(A)<=set(T)) for A in cols] for T in rows])
    B = incidence(levels[4],std)
    assert abs(B.det())==1
    for s in (1,2,3):
        dom = [A for i in range(s+1) for A in levels[i] if standard(A)]
        Bs = incidence(levels[s],dom)
        assert abs(Bs.det())==1
        I = incidence(levels[4],levels[s])
        rhs = matrix(ZZ,[[C(4-len(A),s-len(A))*int(set(A)<=set(T))
                          for A in dom] for T in levels[4]])
        assert I*Bs == rhs
    L = incidence(levels[4],sum([levels[s] for s in (1,2,3)],[]))
    free,_,torsion = invariants(L)
    assert (free,torsion)==(predicted(m)[0],[2])

def raw_relative(m):
    # Direct relative simplicial chains C(Z,K), no use of F.
    cells=[]; dims=[]; lookup={}
    for s in range(5):
        for S in combinations(range(m),s):
            B=((1<<m)-1)^sum(1<<j for j in S)
            for v in product(range(4),repeat=s):
                if any(v.count(i)>2 for i in (1,2,3)): continue
                A=tuple(sum(1<<j for j,c in zip(S,v) if c==i) for i in (1,2,3))
                face=A+(B,)
                lookup[face]=len(cells); cells.append(face)
                dims.append(m-1-v.count(0))
    N=len(cells); cols=[{} for _ in cells]; rows=[{} for _ in cells]
    for k,F in enumerate(cells):
        verts=sorted((j,c) for c,mask in enumerate(F) for j in range(m) if mask>>j&1)
        for p,(j,c) in enumerate(verts):
            G=list(F); G[c]^=1<<j
            l=lookup.get(tuple(G))
            if l is not None:
                a=(-1)**p; cols[k][l]=a; rows[l][k]=a
    # Verify d^2=0 before cancelling anything.
    for col in cols:
        dd=Counter()
        for l,a in col.items():
            for h,b in cols[l].items(): dd[h]+=a*b
        assert all(x==0 for x in dd.values())
    alive=set(range(N)); heap=[]
    def push(k):
        if k in alive:
            for l,a in cols[k].items():
                if abs(a)==1: heapq.heappush(heap,(len(cols[k])*len(rows[l]),k,l))
    for k in range(N): push(k)
    while heap:
        cost,k,l=heapq.heappop(heap)
        if k not in alive or abs(cols[k].get(l,0))!=1: continue
        if cost!=len(cols[k])*len(rows[l]): push(k); continue
        a=cols[k][l]; ck=cols[k].copy(); rl=rows[l].copy(); changed=set()
        for j,b in rl.items():
            if j==k: continue
            for i,c in ck.items():
                v=cols[j].get(i,0)-b*a*c
                if v: cols[j][i]=v; rows[i][j]=v
                else: cols[j].pop(i,None); rows[i].pop(j,None)
            changed.add(j)
        for i in list(cols[k]): rows[i].pop(k,None); changed.update(rows[i])
        for j in list(rows[l]): cols[j].pop(l,None); changed.add(j)
        for j in list(rows[k]): cols[j].pop(k,None); changed.add(j)
        for i in list(cols[l]): rows[i].pop(l,None); changed.update(rows[i])
        cols[k].clear(); rows[k].clear(); cols[l].clear(); rows[l].clear()
        alive.remove(k); alive.remove(l)
        for j in changed: push(j)
    assert all(dims[i] in (m-2,m-1) for i in alive)
    low=sorted(i for i in alive if dims[i]==m-2)
    high=sorted(i for i in alive if dims[i]==m-1)
    M=matrix(ZZ,[[cols[j].get(i,0) for j in high] for i in low])
    return invariants(M)

if __name__=='__main__':
    check_local()
    for m in range(7,12): check_bier(m)
    assert raw_relative(7)==(*predicted(7),[2])
    for m in (7,8,9):
        M=Fmatrix(m)
        a,b,t=invariants(M)
        assert (a,b)==predicted(m) and t==[2]
        print(m, 'sphere multiplicities:',a,b, 'torsion:',t)
    print('All assertions passed.')
