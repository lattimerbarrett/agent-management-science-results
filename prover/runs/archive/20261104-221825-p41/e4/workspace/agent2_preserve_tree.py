"""Try facet insertion preserving every old internal decomposition label."""
from agent3_checker import subsets,deletion_link,verify

def try_insert(fs,k,c,F):
    fs=tuple(sorted(fs));r=fs[0].bit_count()
    if F in fs:return None
    if c[0]=='simplex':
        W=c[1]
        if (W&F).bit_count()!=r-1:return None
        out=('shed',F^ (W&F),c,('simplex',W&F))
    else:
        s=c[1];de,li=deletion_link(fs,s)
        if F&s==s:
            if not all(any((F^v)&f==(F^v) for f in de) for v in subsets(s,1)):return None
            lc=try_insert(li,k,c[3],F^s)
            if lc is None:return None
            out=('shed',s,c[2],lc)
        else:
            dc=try_insert(de,k,c[2],F)
            if dc is None:return None
            out=('shed',s,dc,c[3])
    verify(tuple(sorted(fs+(F,))),k,out)
    return out
