from itertools import product
from pathlib import Path

def run_checks():
    # Every monotone Boolean coordinate on three input bits.
    n=3; masks=range(1<<n)
    subset=lambda a,b: (a & ~b)==0
    coords=[]
    for truth in product((0,1), repeat=1<<n):
        if all(not truth[a] or truth[b] for a in masks for b in masks if subset(a,b)):
            coords.append(truth)
    assert len(coords)==20
    checked=0
    for fs in product(coords,repeat=n):
        monotone=[sum(fs[i][a]<<i for i in range(n)) for a in masks]
        anti=[((1<<n)-1)^v for v in monotone]
        fixed=[a for a in masks if anti[a]==a]
        assert all(not subset(a,b) for a in fixed for b in fixed if a!=b)
        checked+=1
    assert checked==8000
    # Cototal representative construction: C<=complement B and B<=C
    # is implemented abstractly as monotone maps on a finite powerset.
    # Check the tagged complement identities used by the construction.
    for c in masks:
        for b in masks:
            joined=c | (b<<n)
            complement=((1<<(2*n))-1)^joined
            assert complement & ((1<<n)-1)==((1<<n)-1)^c
            assert complement>>n==((1<<n)-1)^b
    return {'antitone_maps':checked,'join_complement_cases':64}

if __name__=='__main__':
    print(run_checks())
