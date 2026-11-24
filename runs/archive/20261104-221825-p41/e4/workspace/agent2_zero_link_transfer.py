"""Transfer any deletion completion through a shedding face with 0-dimensional link."""
from agent3_checker import verify,subsets,deletion_link
from agent2_boundary_fill import fill_boundary

def transfer_zero_link(facets,k,cert,deletion_steps):
    fs=tuple(sorted(facets));r=fs[0].bit_count();s=cert[1]
    assert cert[0]=='shed' and s.bit_count()==r-1
    verify(fs,k,cert)
    D,L=deletion_link(fs,s);H=set(D);oldstar={s|v for v in L}
    G=set(fs);out=[]
    for F,dc in deletion_steps:
        assert F not in H
        H.add(F);verify(tuple(sorted(H)),k,dc)
        if not any(f&s==s for f in H):
            gc=('shed',s,dc,cert[3])
        else:
            current=tuple(sorted(H));gc=dc
            for T in sorted(oldstar-H):
                gc=fill_boundary(current,k,gc,T)
                current=tuple(sorted(current+(T,)))
        verify(tuple(sorted(H|oldstar)),k,gc)
        if F not in G:
            G.add(F);out.append((F,gc))
        assert G==H|oldstar
    return tuple(out)
