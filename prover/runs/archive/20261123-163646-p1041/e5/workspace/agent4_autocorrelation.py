"""Exact check of the autocorrelation degree lemma on supplied ANF masks."""
from itertools import combinations

def autocorrelation_check(m, masks):
    masks=tuple(masks)
    assert len(set(masks))==len(masks)
    r=max((a.bit_count() for a in masks),default=0)
    assert r<=m-2
    f=[sum((x&a)==a for a in masks)%2 for x in range(1<<m)]
    aa=[sum(f[x]*f[x^v] for x in range(1<<m)) for v in range(1<<m)]
    assert all(a%2==0 for a in aa)
    q=[(a//2)%2 for a in aa]
    predicted=[]
    full=(1<<m)-1
    for v in range(1<<m):
        z=0
        for a,b in combinations(masks,2):
            # Correlation has odd size precisely when the union covers all
            # variables and v vanishes on the intersection.
            if a|b==full and v&(a&b)==0: z^=1
        predicted.append(z)
    assert q==predicted
    anf=q[:]
    for i in range(m):
        for v in range(1<<m):
            if v>>i&1: anf[v]^=anf[v^(1<<i)]
    assert all(not z or v.bit_count()<=2*r-m for v,z in enumerate(anf))
    return aa,anf

if __name__=='__main__':
    import random
    rng=random.Random(20260714)
    for m,r in [(4,2),(5,3),(6,3),(7,4)]:
        candidates=[a for a in range(1<<m) if a.bit_count()<=r]
        for j in range(20):
            masks=[a for a in candidates if rng.randrange(2)]
            autocorrelation_check(m,masks)
    print('80 exact autocorrelation identity and degree checks passed')
