from sage.all import *
from itertools import combinations, product
import pickle, os, time

def matrix_map(m):
    cols=[(S,cs) for s in range(5) for S in combinations(range(m),s) for cs in product((0,1),repeat=s)]
    As=list(combinations(range(m),4)); Ts=list(combinations(range(m),3))
    rows=[]
    for i in range(3):
        rows += [(i,'a',A) for A in As]
        rows += [(i,'b',T) for T in Ts]
        rows += [(i,'c',T,j) for T in Ts for j in range(m) if j not in T]
    ri={r:k for k,r in enumerate(rows)}
    mat=matrix(ZZ,len(rows),len(cols),sparse=True)
    for c,(S,cs) in enumerate(cols):
        for extra in combinations([j for j in range(m) if j not in S],4-len(S)):
            A=tuple(sorted(S+extra))
            for mask in product((0,1),repeat=len(S)):
                color={j:2 for j in A}; val=1
                for j,a,b in zip(S,cs,mask):
                    color[j]=a if b==0 else 2
                    if b: val=-val
                for i in range(3):
                    T=tuple(j for j in A if color[j]==i)
                    if len(T)==4: mat[ri[i,'a',A],c]+=val
                    if len(T)==3:
                        j=next(j for j in A if j not in T)
                        a=next(a for a in range(3) if a!=i)
                        if color[j]==a: mat[ri[i,'c',T,j],c]+=val
                    # b_T from one chosen outside j0: sum all color at j0 with mono T
                    for T in combinations(A,3):
                        j=next(j for j in A if j not in T)
                        if j==next(j for j in range(m) if j not in T) and all(color[t]==i for t in T):
                            mat[ri[i,'b',T],c]+=val
    return mat

def direct_check(m,primes=(2,3)):
    faces=[[] for _ in range(m+1)]
    caps=(2,2,2,m-5)
    for a in product(range(5), repeat=m):
        if all(a.count(i+1)<=caps[i] for i in range(4)):
            F=tuple(4*j+a[j]-1 for j in range(m) if a[j])
            faces[len(F)].append(F)
    print('face counts',list(map(len,faces)),flush=True)
    indices=[{F:i for i,F in enumerate(fs)} for fs in faces]
    ranks={p:[0]*(m+2) for p in primes}
    previous={p:None for p in primes}
    for s in range(1,m+1):
        entries={}
        for c,F in enumerate(faces[s]):
            for j in range(s): entries[indices[s-1][F[:j]+F[j+1:]],c]=(-1)**j
        for p in primes:
            B=matrix(GF(p),len(faces[s-1]),len(faces[s]),entries,sparse=True)
            if previous[p] is not None: assert (previous[p]*B).is_zero()
            previous[p]=B
            ranks[p][s]=B.rank()
        print('boundary',s, [ranks[p][s] for p in primes],flush=True)
    A=matrix_map(m)
    for p in primes:
        r=A.change_ring(GF(p)).rank()
        predicted=[0]*(m+1); predicted[m-2]=A.nrows()-r; predicted[m-1]=A.ncols()-r
        # indices are size s, homology dimension s-1
        got=[len(faces[s])-ranks[p][s]-ranks[p][s+1] for s in range(m+1)]
        assert got==predicted,(p,got,predicted)
        print('direct homology checked',p,got,flush=True)

for m in range(7,10):
    A=matrix_map(m); ds=A.elementary_divisors();
    print('integral',m,A.dimensions(),{d:ds.count(d) for d in set(ds)},flush=True)
direct_check(7)
