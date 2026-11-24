"""Delete all vertices of a nonface, retaining the codimension |S|-1 skeleton."""
from agent3_checker import subsets,deletion_link,verify,maximal
from agent2_vertex_completion import full_certificate

def nonface_vertex_delete(fs,k,c,S):
    fs=tuple(sorted(fs));r=fs[0].bit_count();R=r-S.bit_count()+1
    assert R>=0 and S and not any(f&S==S for f in fs)
    if c[0]=='simplex':
        out=full_certificate(c[1]&~S,R)
    else:
        s=c[1];D,L=deletion_link(fs,s)
        if s&S or s.bit_count()>R:
            out=nonface_vertex_delete(D,k,c[2],S)
        else:
            out=('shed',s,nonface_vertex_delete(D,k,c[2],S),nonface_vertex_delete(L,k,c[3],S))
    target=maximal(g for f in fs for q in range(R+1) for g in subsets(f&~S,q))
    assert target and all(f.bit_count()==R for f in target)
    verify(target,k,out)
    return out
