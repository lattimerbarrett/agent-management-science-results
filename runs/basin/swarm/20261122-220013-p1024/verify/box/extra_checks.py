import sys
sys.path.insert(0,'agents/agent_1')
from scratchpad import matrices, delta
from sage.all import QQ, PolynomialRing, matrix

def labels(g, B, kind):
    N=4*g-3
    rr=[(c,m,e) for c in (['h','v'] if kind=='S' else ['q']) for m in range(N) for e in range(-B-3*m+int(c=='h'),0)]
    cc=[]
    for typ in (['H','V'] if kind=='S' else [kind]):
        for n in range(N):
            cap=4*n+B+{'H':-2*g+1,'L':-2*g+2}.get(typ,0)
            cc += [(typ,n,q) for q in range(0,cap+1,2)]
            cc += [(typ,n,q) for q in range(2*g+1,cap+1,2)]
    return rr,cc

for g in [4,7]:
    r=(g+2)//3
    R=PolynomialRing(QQ, ['b%d'%i for i in range(r)])
    K=R.fraction_field()
    b=list(R.gens())
    base=matrices(g,b,K)
    big=matrices(g,b,K,B=4*g+2)
    for kind in ['O','S','L']:
        rows,cols=labels(g,4*g,kind)
        rows2,cols2=labels(g,4*g+2,kind)
        ri={lab:i for i,lab in enumerate(rows2)}
        ci={lab:i for i,lab in enumerate(cols2)}
        old_r=[ri[x] for x in rows]
        old_c=[ci[x] for x in cols]
        setr=set(old_r); setc=set(old_c)
        new_r=[i for i in range(len(rows2)) if i not in setr]
        new_c=[i for i in range(len(cols2)) if i not in setc]
        assert big[kind].matrix_from_rows_and_columns(old_r,old_c)==base[kind]
        assert big[kind].matrix_from_rows_and_columns(new_r,old_c).is_zero()
        assert len(new_r)==len(new_c)
        T=big[kind].matrix_from_rows_and_columns(new_r,new_c)
        # The omitted block is triangular in fiber degree.
        assert all(rows2[new_r[i]][1]>=cols2[new_c[j]][1] for (i,j),v in T.dict().items() if v)
        det=K.one()
        for n in range(4*g-3):
            ir=[i for i in new_r if rows2[i][1]==n]
            jc=[j for j in new_c if cols2[j][1]==n]
            d=big[kind].matrix_from_rows_and_columns(ir,jc).det()
            assert d != 0 and d in QQ
            det*=d
        print('symbolic tail block checked',g,kind,'size',T.nrows(),'nonzero constant determinant',det,flush=True)

for g in range(2,8):
    r=(g+2)//3
    d,h=delta(g,[0]*r)
    def h0(q):
        return sum(1 for j in range(q+1) if j%2==0 or j>=2*g+1)
    po=sum(h0(2*g-2-n) for n in range(4*g-3))
    pl=sum(h0(4*g-4-n) for n in range(4*g-3))
    assert d==1 and h=={'O':po,'L':pl,'S':po+pl-1}
    print('independent split count',g,h,flush=True)
assert delta(7,[0,0,1])==(-2,{'O':35,'S':221,'L':184})
print('All extra checks passed')
