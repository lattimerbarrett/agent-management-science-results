"""Construct and independently check the dimension-minus-two upper bound.
Complexes are tuples of integer bitmasks for their facets.
Imports agent2_checker.py for exhaustive decomposition certificates/checking.
"""
from itertools import combinations
from agent2_checker import maximal, bits, subsets, pure, deletion, link, certificate, verify

def uniform_cert(vertices, rank):
    if rank == 0: return ('simplex',0)
    if len(bits(vertices)) == rank: return ('simplex',vertices)
    v=bits(vertices)[0]
    return ('shed',v,uniform_cert(vertices^v,rank),uniform_cert(vertices^v,rank-1))

def skeleton(fs, rank):
    return maximal(s for f in fs for s in subsets(f,rank) if s.bit_count()==rank)

def skeleton_cert(fs,c,rank):
    if rank==0:return ('simplex',0)
    if c[0]=='simplex':return uniform_cert(c[1],rank)
    _,s,cd,cl=c
    de=deletion(fs,s)
    if s.bit_count()>rank:return skeleton_cert(de,cd,rank)
    return ('shed',s,skeleton_cert(de,cd,rank),skeleton_cert(link(fs,s),cl,rank-s.bit_count()))

def prefix_order(c):
    if c[0]=='simplex':return [c[1]]
    _,s,cd,cl=c
    return prefix_order(cd)+[s|f for f in prefix_order(cl)]

def zero_cert(vertices):
    vs=bits(vertices)
    if len(vs)==1:return ('simplex',vs[0])
    return ('shed',vs[0],zero_cert(vertices^vs[0]),('simplex',0))

def cone_cert(gamma,c,D,a):
    # All boundaries of facets D are in gamma.
    rank=gamma[0].bit_count()
    if c[0]=='simplex':
        if rank==0:return zero_cert(a|sum(D))
        assert not D
        return ('simplex',a|gamma[0])
    _,s,cd,cl=c
    dd=tuple(f for f in D if f&s!=s)
    dl=tuple(f^s for f in D if f&s==s)
    return ('shed',s,cone_cert(deletion(gamma,s),cd,dd,a),cone_cert(link(gamma,s),cl,dl,a))

def boundary_fill(fs,c,F,k):
    # Add a missing facet all of whose proper faces already occur.
    if fs[0].bit_count()==1:
        return ('shed',F,c,('simplex',0))
    assert c[0]=='shed'
    _,s,cd,cl=c
    if F&s!=s:
        return ('shed',s,boundary_fill(deletion(fs,s),cd,F,k),cl)
    return ('shed',s,cd,boundary_fill(link(fs,s),cl,F^s,k))

def complete(fs,c,k,fresh):
    # fresh is a list of exactly max(dim-2,0) unused vertex bitmasks.
    fs=maximal(fs)
    d=fs[0].bit_count()-1
    assert len(fresh)==max(d-2,0)
    verify(fs,k,c)
    V=0
    for f in fs:V|=f
    if d==2:
        out=[]
        while True:
            edges=set(s for f in fs for s in subsets(f,2) if s.bit_count()==2)
            choice=None
            for u,v in combinations(bits(V),2):
                if u|v in edges:continue
                for w in bits(V^(u|v)):
                    if u|w in edges and v|w in edges:
                        choice=(u|v,u|v|w,w);break
                if choice:break
            if not choice:break
            e,F,w=choice
            c=('shed',e,c,('simplex',w))
            fs=maximal((*fs,F)); out.append(F)
            verify(fs,k,c)
        assert len(edges)==len(list(combinations(bits(V),2)))
        for vv in combinations(bits(V),3):
            F=sum(vv)
            if F not in fs:
                c=boundary_fill(fs,c,F,k)
                fs=maximal((*fs,F));out.append(F)
                verify(fs,k,c)
        return out,c
    assert d>=3
    a=fresh[0]
    G=skeleton(fs,d)
    cg=skeleton_cert(fs,c,d)
    verify(G,k,cg)
    out=[]
    current=fs
    # First introduce a by coning a k-decomposable prefix order of the skeleton.
    pg=[]
    for g in prefix_order(cg):
        pg.append(g)
        cp=certificate(tuple(sorted(pg)),k)
        assert cp is not None
        cc=('shed',a,c,cp)
        current=maximal((*current,a|g));out.append(a|g)
        verify(current,k,cc)
    extra,cfull=complete(G,cg,k,fresh[1:])
    for g in extra:
        G=maximal((*G,g))
        # For checks use an independently found certificate of the link.
        # The mathematical construction can instead retain its inductive cert.
        cg=certificate(G,k)
        assert cg is not None
        current=maximal((*current,a|g));out.append(a|g)
        cc=cone_cert(G,cg,fs,a)
        verify(current,k,cc)
    U=V
    for b in fresh[1:]:U|=b
    for vv in combinations(bits(U),d+1):
        F=sum(vv)
        if F not in current:
            fs=maximal((*fs,F));current=maximal((*current,F));out.append(F)
            cc=cone_cert(G,cfull,fs,a)
            verify(current,k,cc)
    return out,cc

if __name__=='__main__':
    count=0
    # Exhaust every k=1 decomposable triangle complex on <=5 vertices.
    for n in range(3,6):
        ff=[sum(c) for c in combinations([1<<i for i in range(n)],3)]
        for mask in range(1,1<<len(ff)):
            fs=tuple(f for i,f in enumerate(ff) if mask>>i&1)
            c=certificate(fs,1)
            if c is None:continue
            out,cc=complete(fs,c,1,[])
            end=maximal((*fs,*out))
            verify(end,1,cc)
            count+=1
    print('Verified 2D constructions:',count)
    # Distinct nontrivial 3D and 4D examples, including initial simplices.
    tests=[((15,),3),((15,30),3),((15,23,27,29),3),((31,),4),((31,62),4)]
    for fs,d in tests:
        c=certificate(fs,1)
        if c is None:continue
        n=max(fs).bit_length()
        fresh=[1<<(n+i) for i in range(d-2)]
        out,cc=complete(fs,c,1,fresh)
        U=0
        for f in fs:U|=f
        for b in fresh:U|=b
        end=maximal((*fs,*out))
        assert set(end)==set(sum(v) for v in combinations(bits(U),d+1))
        verify(end,1,cc)
        print('Verified dimension',d,'initial',fs,'added',len(out),'facets')
