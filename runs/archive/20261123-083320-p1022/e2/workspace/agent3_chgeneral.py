import sys,time,pickle
sys.path.insert(0,'workspace')
from agent4_chow_two import *
from pathlib import Path

def setup(parts):
    us=[];ch=[];linevars=[]
    for i,r in enumerate(parts):
        cc=[S.Integer(r)]
        if r==1:linevars.append(S.Symbol(f'b{i}'))
        for j in range(1,8):
            if r==1:cc.append(red((linevars[-1]*(h+x))**j/S.factorial(j)))
            else:
                vs=S.symbols(f'v{i}_{j}_0:{len(B[j])}')
                us.extend(vs)
                cc.append(sum(v*f for v,f in zip(vs,B[j])))
        ch.append(cc)
    expr=[red(sum(sum(ch[i][j]*(2-i)**(k-j)*h**(k-j)/S.factorial(k-j) for j in range(k+1)) for i in range(3))) for k in range(1,8)]
    eq=[]
    for e in expr:eq.extend(c for (ph,px),c in S.Poly(e,h,x).terms() if px>0)
    us=list(reversed(us))
    sol=next(iter(S.linsolve(eq,us)))
    sub=dict(zip(us,sol))
    free=set().union(*(e.free_symbols for e in sol))|set(linevars)
    free-=set([h,x])
    ccs=[];rankeq=[]
    for i,r in enumerate(parts):
        co=[S.Integer(1)]
        for k in range(1,7):
            ck=red(sum((-1)**(j-1)*S.factorial(j)*ch[i][j].subs(sub)*co[k-j] for j in range(1,k+1))/k)
            if k>r:
                rankeq.extend(S.Poly(ck,h,x).coeffs())
                co.append(S.Integer(0))
            else:co.append(S.expand(ck))
        ccs.append(co)
    rankeq=list(dict.fromkeys(S.factor(e) for e in rankeq if e!=0))
    print(parts,'initial remaining',len(free),'rankeq',len(rankeq),flush=True)
    elim={}
    while True:
        found=False
        # Eliminate only a variable whose coefficient is a nonzero rational constant.
        for eqn in sorted(rankeq,key=S.count_ops):
            for v in sorted(free,key=str,reverse=True):
                pol=S.Poly(eqn,v)
                if pol.degree()==1 and pol.coeff_monomial(v).is_Rational and pol.coeff_monomial(v)!=0:
                    val=S.expand(-pol.coeff_monomial(1)/pol.coeff_monomial(v))
                    elim[v]=val
                    free.remove(v)
                    rankeq=[S.factor(e.subs(v,val)) for e in rankeq]
                    rankeq=list(dict.fromkeys(e for e in rankeq if e!=0))
                    found=True;break
            if found:break
        if not found:break
    print(parts,'reduced vars',len(free),sorted(free,key=str),'eq',len(rankeq),'maxdegree',max([S.Poly(e,*free).total_degree() for e in rankeq] or [0]),flush=True)
    name=''.join(map(str,parts))
    pickle.dump({'equations':rankeq,'vars':sorted(free,key=str),'sub':sub,'eliminations':elim,'chern':ccs},open(f'workspace/agent3_ch{name}_general.pkl','wb'))
    return rankeq, sorted(free,key=str)
if __name__=='__main__':
    Path('workspace/agent3_chgeneral.py').write_text(Path(__file__).read_text())
    parts=(2,3,2)
    eq,vs=setup(parts)
    for e in eq: print(S.factor(e),flush=True)
