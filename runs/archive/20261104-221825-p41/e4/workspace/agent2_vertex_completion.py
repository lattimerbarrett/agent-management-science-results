"""Certified constructive vertex-decomposable completion (k=0 subclass)."""
from itertools import combinations
from functools import reduce
from operator import or_
from agent3_checker import certificate, deletion_link, subsets, verify

def vertex_completion(facets, ambient=None):
    fs=tuple(sorted(facets)); rank=fs[0].bit_count()
    verts=reduce(or_,fs,0)
    if ambient is None: ambient=verts
    assert verts & ambient == verts
    c=certificate(fs,0)
    assert c is not None
    if rank==0:return ()
    out=[]
    if c[0]=='simplex':
        current=verts
        for v in subsets(ambient^verts,1):
            old=current
            t=next(subsets(old,rank-1))
            out.append(v|t)
            for g in vertex_completion((t,),old):out.append(v|g)
            current|=v
    else:
        v=c[1]
        de,li=deletion_link(fs,v)
        out.extend(vertex_completion(de,ambient^v))
        out.extend(v|g for g in vertex_completion(li,ambient^v))
    # Independent recursive checker verifies every step, not just final output.
    current=set(fs)
    for f in out:
        assert f not in current and f.bit_count()==rank
        current.add(f)
        cc=certificate(tuple(sorted(current)),0)
        assert cc is not None
        verify(tuple(sorted(current)),0,cc)
    assert current==set(subsets(ambient,rank))
    return tuple(out)


def full_certificate(ambient, rank):
    """Explicit vertex-decomposition of a complete uniform skeleton."""
    assert 0<=rank<=ambient.bit_count()
    if rank==0:return ('simplex',0)
    if ambient.bit_count()==rank:return ('simplex',ambient)
    v=ambient&-ambient
    return ('shed',v,full_certificate(ambient^v,rank),
            full_certificate(ambient^v,rank-1))

def certified_completion(facets, initial_certificate, ambient=None):
    """Compute witnesses directly: no decomposition search for intermediates."""
    fs=tuple(sorted(facets)); rank=fs[0].bit_count()
    verts=reduce(or_,fs,0)
    if ambient is None:ambient=verts
    assert verts&ambient==verts
    verify(fs,0,initial_certificate)
    if rank==0:return ()
    c=initial_certificate;out=[]
    if c[0]=='simplex':
        current=verts
        for v in subsets(ambient^verts,1):
            old=current
            dc=full_certificate(old,rank)
            t=next(subsets(old,rank-1));lc=('simplex',t)
            out.append((v|t,('shed',v,dc,lc)))
            for g,gc in certified_completion((t,),lc,old):
                out.append((v|g,('shed',v,dc,gc)))
            current|=v
    else:
        v=c[1]; de,li=deletion_link(fs,v)
        for g,gc in certified_completion(de,c[2],ambient^v):
            out.append((g,('shed',v,gc,c[3])))
        dc=full_certificate(ambient^v,rank)
        for g,gc in certified_completion(li,c[3],ambient^v):
            out.append((v|g,('shed',v,dc,gc)))
    current=set(fs)
    for g,gc in out:
        assert g not in current
        current.add(g)
        verify(tuple(sorted(current)),0,gc)
    assert current==set(subsets(ambient,rank))
    return tuple(out)
