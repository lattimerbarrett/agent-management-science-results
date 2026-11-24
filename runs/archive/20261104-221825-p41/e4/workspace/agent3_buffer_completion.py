"""Constructed vertex-decomposable completion of a buffered target from any basis.
Target = rank-r truncation of K * simplex(P), |P| >= r-1.
"""
from agent3_checker import subsets,deletion_link,verify
from agent2_vertex_completion import certified_completion

def buffered_completion(target, free, W):
    T=tuple(sorted(target));r=W.bit_count()
    assert W in T and all(f.bit_count()==r for f in T)
    if r==0:return ()
    U=0
    for f in T:U|=f
    assert free&U==free and free.bit_count()>=r-1
    constrained=U&~free
    outside=constrained&~W
    if not outside:
        assert set(T)==set(subsets(U,r))
        return certified_completion((W,),('simplex',W),U)
    u=outside&-outside
    D,L=deletion_link(T,u)
    assert all(f.bit_count()==r for f in D)
    out=list(buffered_completion(D,free,W))
    dc=out[-1][1] if out else ('simplex',W)
    S=L[0]
    out.append((u|S,('shed',u,dc,('simplex',S))))
    for g,gc in buffered_completion(L,free,S):
        out.append((u|g,('shed',u,dc,gc)))
    cur={W}
    for f,c in out:
        assert f in T and f not in cur
        cur.add(f);verify(tuple(sorted(cur)),0,c)
    assert cur==set(T)
    return tuple(out)
