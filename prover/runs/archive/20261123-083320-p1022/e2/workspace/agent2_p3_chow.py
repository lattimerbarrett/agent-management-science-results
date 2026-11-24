import sympy as S
from functools import lru_cache
import pickle,time
h,x,t=S.symbols('h x t')
@lru_cache(None)
def redmon(a,b):
    if a>=4:return {}
    if b<3:return {(a,b):S.Integer(1)}
    ans={}
    for i in range(1,4):
        for mon,c in redmon(a+i,b-i).items():
            ans[mon]=ans.get(mon,0)-c
    return {k:v for k,v in ans.items() if v}
def red(poly):
    out={}
    for (a,b),c in S.Poly(S.expand(poly),h,x).terms():
        for mon,d in redmon(a,b).items():out[mon]=out.get(mon,0)+c*d
    return S.expand(sum(c*h**a*x**b for (a,b),c in out.items()))

def cbasis(j):
    polys=[red((h+x)**(j-2*b)*(h*x)**b) for b in range(j//2+1)]
    mons=[(j-b,b) for b in range(j+1)]
    M=S.Matrix([[S.Poly(f,h,x).coeff_monomial(h**a*x**b) for f in polys] for a,b in mons])
    piv=M.rref()[1]
    return [polys[k] for k in piv]
B={j:cbasis(j) for j in range(1,6)}
print('Grassmannian homogeneous Chow dimensions:',[len(B[j]) for j in B],flush=True)

def factor(r,idx,a):
    f=(t+a*h)**r
    us=[]
    for j in range(1,r+1):
        for k,b in enumerate(B[j]):
            u=S.Symbol(f'u{idx}_{j}_{k}')
            us.append(u)
            f+=u*b*(t+a*h)**(r-j)
    return S.expand(f),us

def compositions(n):
 if n==0:yield ()
 else:
  for j in range(1,n+1):
   for c in compositions(n-j):yield (j,)+c

def equations(parts):
    f=S.Integer(1);us=[]
    for i,r in enumerate(parts):
        g,vs=factor(r,i,len(parts)-1-i)
        f=S.expand(f*g);us+=vs
    out={}
    for (ct,ch,cx),c in S.Poly(f,t,h,x).terms():
        for (rh,rx),rc in redmon(ch,cx).items():
            key=(ct,rh,rx)
            out[key]=out.get(key,0)+rc*c
    eqs=[S.expand(c) for (ct,ch,cx),c in out.items() if cx>0 and c!=0]
    eqs=list(dict.fromkeys(eqs))
    return eqs,us

if __name__=='__main__':
 for parts in compositions(5):
    if len(parts)==1:continue
    eqs,us=equations(parts)
    print('parts',parts,'unknowns',len(us),'equations',len(eqs),flush=True)
    start=time.time()
    gb=S.groebner(eqs,*reversed(us))
    print('elapsed',time.time()-start,'basis length',len(gb.polys),'zero_dim',gb.is_zero_dimensional,flush=True)
    print([S.factor(p.as_expr()) for p in gb.polys],flush=True)
    pickle.dump((eqs,us,gb),open('workspace/agent2_p3_cw_'+''.join(map(str,parts))+'.pkl','wb'))
