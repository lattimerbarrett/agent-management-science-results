"""A full-boundary facet filling preserves k-decomposability, all k>=0."""
from agent3_checker import verify,subsets,deletion_link

def fill_boundary(facets,k,cert,F):
    fs=tuple(sorted(facets));r=fs[0].bit_count()
    verify(fs,k,cert)
    assert F.bit_count()==r and F not in fs
    assert all(any((F^v)&f==(F^v) for f in fs) for v in subsets(F,1))
    if cert[0]=='simplex':
        assert r==1
        out=('shed',F,cert,('simplex',0))
    else:
        s=cert[1];de,li=deletion_link(fs,s)
        if F&s==s:
            lc=fill_boundary(li,k,cert[3],F^s)
            out=('shed',s,cert[2],lc)
        else:
            dc=fill_boundary(de,k,cert[2],F)
            out=('shed',s,dc,cert[3])
    verify(tuple(sorted(fs+(F,))),k,out)
    return out
