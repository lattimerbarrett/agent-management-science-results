import sys,itertools,pathlib
pathlib.Path('workspace/agent2_vd_complete.py').write_text(pathlib.Path(__file__).read_text())
sys.path.insert(0,'workspace')
from agent3_check import k_certificate,all_faces,maximal

def vd_complete(F,ambient):
    '''Return a facet-addition order completing pure VD F on ambient bitmask.'''
    F=tuple(sorted(F));d=F[0].bit_count()-1
    assert k_certificate(F,0) is not None
    if d==0:
        return [1<<i for i in range(ambient.bit_length()) if ambient>>i&1 and (1<<i) not in F]
    if ambient.bit_count()==d+1:return []
    used=0
    for f in F:used|=f
    ghost=ambient&~used;out=[]
    if ghost:
        v=ghost&-ghost
        ridge=F[0]^(F[0]&-F[0])
        g=v|ridge;out.append(g);F=tuple(sorted(F+(g,)))
    else:
        cert=k_certificate(F,0)
        assert cert[0]=='shed';v=cert[1]
    S=all_faces(F)
    D=maximal(f for f in S if f&v==0)
    L=maximal(f^v for f in F if f&v)
    for g in vd_complete(D,ambient^v):
        out.append(g);F=tuple(sorted(F+(g,)))
    for h in vd_complete(L,ambient^v):
        out.append(v|h);F=tuple(sorted(F+(v|h,)))
    return out

def verify(F,ambient):
    out=vd_complete(F,ambient);cur=set(F)
    d=next(iter(cur)).bit_count()-1
    for g in out:
        assert g not in cur;cur.add(g)
        assert k_certificate(tuple(sorted(cur)),0) is not None
    assert cur=={sum(1<<v for v in ss) for ss in itertools.combinations([i for i in range(ambient.bit_length()) if ambient>>i&1],d+1)}
    return len(out)

if __name__=='__main__':
    checks=0;steps=0
    for n,d in [(4,1),(5,2),(6,3)]:
        fs=[sum(1<<v for v in ss) for ss in itertools.combinations(range(n),d+1)]
        for bits in range(1,1<<len(fs)):
            F=tuple(f for j,f in enumerate(fs) if bits>>j&1)
            if k_certificate(F,0) is None:continue
            steps+=verify(F,(1<<n)-1);checks+=1
    print('VD completion verified:',checks,'inputs;',steps,'intermediate facet additions')
