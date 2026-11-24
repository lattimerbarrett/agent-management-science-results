"""Nonface boundary-join closure of k-decomposable complexes."""
from agent3_checker import subsets,deletion_link,maximal,verify
from agent3_nonface_vertex_delete import nonface_vertex_delete
from agent3_buffer_completion import buffered_completion

def joined_trunc(K,P,r):
    return tuple(sorted({g for f in K for g in subsets(f|P,r)}))

def buffer_lift(K,P,r,k,lowcert):
    p=P.bit_count();q=max(0,r-p)
    T=joined_trunc(K,P,r)
    assert T
    if q==0:
        W=T[0];steps=buffered_completion(T,P,W)
        out=steps[-1][1] if steps else ('simplex',W)
    elif lowcert[0]=='simplex':
        assert T==(lowcert[1]|P,)
        out=('simplex',T[0])
    else:
        s=lowcert[1];D,L=deletion_link(K,s)
        out=('shed',s,buffer_lift(D,P,r,k,lowcert[2]),
             buffer_lift(L,P,r-s.bit_count(),k,lowcert[3]))
    verify(T,k,out)
    return out

def boundary_lift(K,S,r,k,lowcert):
    assert S
    T=tuple(sorted({g for v in subsets(S,1) for f in K
                    for g in subsets((S^v)|f,r)}))
    if S.bit_count()==1:out=lowcert
    else:
        v=S&-S;P=S^v
        out=('shed',v,buffer_lift(K,P,r,k,lowcert),
             boundary_lift(K,P,r-1,k,lowcert))
    verify(T,k,out)
    return out

def nonface_boundary_closure(fs,k,c,S):
    r=fs[0].bit_count()
    assert 1<=S.bit_count()<=r+1 and not any(f&S==S for f in fs)
    K=maximal(f&~S for f in fs)
    low=nonface_vertex_delete(fs,k,c,S)
    out=boundary_lift(K,S,r,k,low)
    T=tuple(sorted({g for v in subsets(S,1) for f in K
                    for g in subsets((S^v)|f,r)}))
    assert set(fs)<=set(T)
    verify(T,k,out)
    return T,out
