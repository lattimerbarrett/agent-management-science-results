"""Fast exact k-decomposability with ridge-owner purity test."""
from functools import lru_cache
from agent3_checker import subsets

@lru_cache(maxsize=300000)
def fast_certificate(fs,k):
    fs=tuple(sorted(fs))
    if not fs:return None
    rank=fs[0].bit_count()
    if any(f.bit_count()!=rank for f in fs):return None
    if len(fs)==1:return ('simplex',fs[0])
    owners={};ridges={}
    for i,f in enumerate(fs):
        for j in range(1,min(rank,k+1)+1):
            for s in subsets(f,j):owners[s]=owners.get(s,0)|(1<<i)
        for v in subsets(f,1):
            g=f^v;ridges[g]=ridges.get(g,0)|(1<<i)
    allbits=(1<<len(fs))-1
    for s in sorted(owners,key=lambda x:(x.bit_count(),x)):
        star=owners[s];rest=allbits^star
        if not rest:continue
        indices=[];b=star;pure=True
        while b and pure:
            z=b&-b;i=z.bit_length()-1;b^=z;indices.append(i)
            for v in subsets(s,1):
                if not (ridges[fs[i]^v]&rest):pure=False;break
        if not pure:continue
        de=tuple(f for i,f in enumerate(fs) if rest>>i&1)
        dc=fast_certificate(de,k)
        if dc is None:continue
        li=tuple(sorted({fs[i]^s for i in indices}))
        lc=fast_certificate(li,k)
        if lc is not None:return ('shed',s,dc,lc)
    return None

from agent2_homology import cm_obstruction

@lru_cache(maxsize=300000)
def fast_homology_certificate(fs,k):
    fs=tuple(sorted(fs))
    if not fs:return None
    rank=fs[0].bit_count()
    if any(f.bit_count()!=rank for f in fs):return None
    if len(fs)==1:return ('simplex',fs[0])
    if rank>=3 and __import__("functools").reduce(int.__or__,fs,0).bit_count()>=7:
        if cm_obstruction(fs) is not None:return None
    owners={};ridges={}
    for i,f in enumerate(fs):
        for j in range(1,min(rank,k+1)+1):
            for s in subsets(f,j):owners[s]=owners.get(s,0)|(1<<i)
        for v in subsets(f,1):
            g=f^v;ridges[g]=ridges.get(g,0)|(1<<i)
    allbits=(1<<len(fs))-1
    for s in sorted(owners,key=lambda x:(x.bit_count(),x)):
        star=owners[s];rest=allbits^star
        if not rest:continue
        indices=[];b=star;pure=True
        while b and pure:
            z=b&-b;i=z.bit_length()-1;b^=z;indices.append(i)
            for v in subsets(s,1):
                if not (ridges[fs[i]^v]&rest):pure=False;break
        if not pure:continue
        de=tuple(f for i,f in enumerate(fs) if rest>>i&1)
        dc=fast_homology_certificate(de,k)
        if dc is None:continue
        li=tuple(sorted({fs[i]^s for i in indices}))
        lc=fast_homology_certificate(li,k)
        if lc is not None:return ('shed',s,dc,lc)
    return None
