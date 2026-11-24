"""Explicit degree-seven words realizing every required weight <=308.
All computations exact. Coordinate numbering starts at zero.
"""
from itertools import combinations
import numpy as np

def flat_truth(free, shift=0):
    fixed = ((1<<14)-1)^sum(1<<i for i in free)
    return np.fromiter((int(x&fixed == shift&fixed) for x in range(1<<14)),dtype=np.uint8)

def degree(truth):
    a=truth.copy()
    for j in range(14):
        step=1<<j
        for start in range(0,1<<14,2*step):
            a[start+step:start+2*step]^=a[start:start+step]
    return max((i.bit_count() for i in np.flatnonzero(a)),default=-1)

def verify():
    words={0:np.zeros(1<<14,dtype=np.uint8)}
    A=set(range(7))
    words[128]=flat_truth(A)
    for t in range(7):
        B=set(range(t))|set(range(7,14-t))
        words[256-2**(t+1)]=flat_truth(A)^flat_truth(B)
    words[256]=flat_truth(A)^flat_truth(A,1<<7)
    tuples={272:(2,5,4,4),288:(2,5,4,3),296:(1,5,3,3),304:(2,4,4,4),308:(1,5,3,1)}
    for wt,(d,p,q,r) in tuples.items():
        counts=[d,p-d,q-d,r-d,7-p-q+d,7-p-r+d,7-q-r+d]
        assert min(counts)>=0 and sum(counts)<=14
        sets=[set(),set(),set()];offset=0
        for count,members in zip(counts,[(0,1,2),(0,1),(0,2),(1,2),(0,),(1,),(2,)]):
            for j in members: sets[j].update(range(offset,offset+count))
            offset+=count
        assert all(len(s)==7 for s in sets)
        words[wt]=flat_truth(sets[0])^flat_truth(sets[1])^flat_truth(sets[2])
    assert set(words)=={0,128,192,224,240,248,252,254,256,272,288,296,304,308}
    for wt,f in sorted(words.items()):
        actual=int(f.sum()); deg=degree(f)
        assert actual==wt and deg<=7,(wt,actual,deg)
        print('verified weight',wt,'degree',deg)
    return words
if __name__=='__main__':verify()
