"""Exact, independently checkable integral verifications. Run check(m,full=True)
for full simplicial-vs-fiber comparison, or check(m) for polynomial-size model.
Uses actual integer boundary cancellations and Smith forms, not guessed output.
"""
from a3_fiber import fiber_complex,reduce_bd
from a3_reducer import faces_for,reduce
from sage.all import ZZ,matrix,binomial
from collections import Counter

def smith_summary(bd,sz,alive,lo):
    assert all(sz[i] in [lo,lo+1] for i in alive)
    rows=[i for i in alive if sz[i]==lo]
    cols=[i for i in alive if sz[i]==lo+1]
    B=matrix(ZZ,len(rows),len(cols),[bd[j].get(i,0) for i in rows for j in cols])
    D=B.smith_form()[0]
    diag=[abs(D[i,i]) for i in range(min(D.dimensions()))]
    rank=sum(x!=0 for x in diag)
    return len(rows)-rank,len(cols)-rank,tuple(x for x in diag if x>1)

def check(m,full=False):
    gens,bd,sz=fiber_complex(m)
    expected=[binomial(m-1,4),3*m*binomial(m-2,3),9*binomial(m,2)*binomial(m-3,2),24*(m-4)*binomial(m,3),54*binomial(m,4)]
    assert Counter(sz)==Counter({k:int(n) for k,n in enumerate(expected)})
    for j,col in enumerate(bd):
        dd=Counter()
        for i,v in col.items():
            assert sz[i]==sz[j]-1
            for h,w in bd[i].items():dd[h]+=v*w
        assert not any(dd.values())
    bd,alive=reduce_bd(bd,sz,verbose=False)
    result=smith_summary(bd,sz,alive,3)
    # An independently conjectured closed form, verified here only at input m.
    b=int(binomial(m,4)-binomial(m,3))
    E=(m**4+14*m**3-m*m+34*m+24)//24
    assert result==(b,b+E,(ZZ(2),)),(m,result)
    if full:
        fs,fb,fa=reduce(faces_for(m),verbose=False)
        fsz=[len(f)-1 for f in fs]
        assert smith_summary(fb,fsz,fa,m-3)==result
    return result
