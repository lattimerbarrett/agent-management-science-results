"""Exact SMALL-DIMENSION experiment, not a proof for c=7.
Checks ordinary 3-plane counts for every one of 2^20 alternating
3-forms on F2^6, using a Walsh transform of the full Grassmannian sum.
"""
from itertools import combinations
import numpy as np

def fwht(a):
    a=a.copy(); h=1
    while h<len(a):
        v=a.reshape(-1,2*h)
        u=v[:,:h].copy(); w=v[:,h:].copy()
        v[:,:h]=u+w;v[:,h:]=u-w
        h*=2
    return a

def verify():
    mons=[sum(1<<i for i in inds) for inds in combinations(range(6),3)]
    mi={M:i for i,M in enumerate(mons)}
    def wedge(vs):
        d={0}
        for v in vs:
            nd=set()
            for M in d:
                for i in range(6):
                    if v>>i&1 and not M>>i&1:
                        z=M|(1<<i)
                        if z in nd:nd.remove(z)
                        else:nd.add(z)
            d=nd
        return sum(1<<mi[M] for M in d)
    spaces={}
    for a,b,c in combinations(range(1,64),3):
        if a^b==c:continue
        S=(1<<a)|(1<<b)|(1<<c)|(1<<(a^b))|(1<<(a^c))|(1<<(b^c))|(1<<(a^b^c))
        spaces.setdefault(S,(a,b,c))
    assert len(spaces)==1395
    indicator=np.zeros(1024,dtype=np.int64)
    for z in range(0,1024,2):
        a=(z>>1)&7;b=(z>>4)&7;c=(z>>7)&7
        if a and b and a!=b and c and c!=a and c!=b and c!=a^b:
            indicator[z]=1
    assert sum(indicator)==168
    hat=fwht(indicator)
    spectrum=np.zeros(1<<20,dtype=np.int64)
    for basis in spaces.values():
        span={0}
        for b in basis:span|={x^b for x in list(span)}
        X=[]
        for e in [1<<i for i in range(6)]:
            if e not in span:
                X.append(e);span|={x^e for x in list(span)}
        assert len(X)==3
        # Matrix rows are indexed by the 3 pairs of Y basis vectors.
        forms=[wedge(basis)]+[wedge([basis[i],basis[j],x]) for i,j in combinations(range(3),2) for x in X]
        masks=[0]
        for form in forms:masks += [m^form for m in masks]
        np.add.at(spectrum,np.array(masks),hat)
    raw=fwht(spectrum)
    assert np.all(raw%1024==0)
    counts=raw//1024
    vals,pop=np.unique(counts,return_counts=True)
    result=dict(zip(map(int,vals),map(int,pop)))
    assert result=={0:56080,168:357120,256:468720,360:166656},result
    v=np.arange(1<<20,dtype=np.uint32);q=np.zeros(len(v),dtype=np.uint8)
    for M in mons:
        if M<(63^M):q^=((v>>mi[M])&(v>>mi[63^M])&1).astype(np.uint8)
    assert np.all(counts%8==0)
    assert np.array_equal(((counts//8)&1).astype(np.uint8),q)
    print('All 2^20 alternating 3-forms checked on all 1395 three-planes.')
    print('Ordinary-zero count histogram:',result)
    print('N/8 mod2 = divided-square invariant q in all cases.')
    print('WARNING: this does not establish an ordinary-zero theorem for 7-forms.')

if __name__=='__main__':verify()
