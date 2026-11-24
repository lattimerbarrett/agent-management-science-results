"""Exact integral homology certificate for the column-constrained K_7.
No external packages. Vertices are 4*column+row with row=0,...,3.
Run with Python 3. All chain-complex checks and all arithmetic are exact.
"""
import itertools, collections, math

def main():
    faces=[[] for _ in range(8)]
    for a in itertools.product(range(5),repeat=7):
        if any(a.count(i)>2 for i in range(1,5)):
            continue
        f=tuple(4*j+a[j]-1 for j in range(7) if a[j])
        faces[len(f)].append(f)
    assert list(map(len,faces))==[1,28,336,2100,7140,12600,10080,2520]
    D=[{}]
    for k in range(1,8):
        ix={f:i for i,f in enumerate(faces[k-1])}
        D.append({j:{ix[f[:t]+f[t+1:]]:(-1)**t for t in range(k)}
                  for j,f in enumerate(faces[k])})
    active=[set(range(len(ff))) for ff in faces]
    def check():
        for k in range(2,8):
            for c,b in D[k].items():
                acc={}
                for r,v in b.items():
                    for s,w in D[k-1][r].items():
                        acc[s]=acc.get(s,0)+v*w
                assert all(x==0 for x in acc.values()), (k,c,acc)
    check()
    cancelled=[]
    for k in range(1,8):
        B=D[k]
        incidence=collections.defaultdict(set)
        for c,b in B.items():
            for r in b: incidence[r].add(c)
        queue=collections.deque((c,r) for c,b in B.items()
                                for r,v in b.items() if abs(v)==1)
        count=0
        while queue:
            c,r=queue.popleft()
            if c not in B or abs(B[c].get(r,0))!=1:
                continue
            b=B[c]; p=b[r]
            # Other basis columns j become j-(B[r,j]/p)c.
            for cc in list(incidence[r]):
                if cc==c: continue
                bb=B[cc]; a=bb[r]*p
                for rr,v in b.items():
                    old=bb.get(rr,0); new=old-a*v
                    if new:
                        bb[rr]=new
                        if not old: incidence[rr].add(cc)
                        if abs(new)==1: queue.append((cc,rr))
                    elif old:
                        del bb[rr]; incidence[rr].discard(cc)
            for rr in b: incidence[rr].discard(c)
            del B[c]
            active[k].remove(c);active[k-1].remove(r)
            count+=1
        # Complete each cancellation in the neighboring matrices.
        # The new pivot coordinate of the upper differential is zero by d^2=0.
        # The lower differential kills the new pivot boundary, also by d^2=0.
        for ell in range(1,8):
            D[ell]={c:{r:v for r,v in b.items() if r in active[ell-1]}
                     for c,b in D[ell].items() if c in active[ell]}
        check()
        cancelled.append(count)
        print('degree',k-1,'unit cancellations',count,'remaining',list(map(len,active)))
    assert cancelled==[1,27,309,1791,5349,7250,2520]
    assert list(map(len,active))==[0,0,0,0,0,1,310,0]
    vals=[v for b in D[6].values() for v in b.values()]
    assert math.gcd(*vals)==2
    assert all(not b for k in (1,2,3,4,5,7) for b in D[k].values())
    print('Nonzero residual differential:',collections.Counter(vals),'gcd=',math.gcd(*vals))
    print('Exact result: Htilde_4=Z/2, Htilde_5=Z^309; all other groups zero.')
    return faces,active,D

if __name__=='__main__':
    main()
