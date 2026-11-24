import sys,time,pickle
sys.path.insert(0,'workspace')
from agent4_chow_two import *
from pathlib import Path
b=S.symbols('b')
us=[];ch=[]
for i,r in enumerate([3,1,3]):
    cc=[S.Integer(r)]
    for j in range(1,8):
        if r==1:cc.append(red((b*(h+x))**j/S.factorial(j)))
        else:
            vs=S.symbols(f'v{i}_{j}_0:{len(B[j])}')
            us.extend(vs)
            cc.append(sum(v*f for v,f in zip(vs,B[j])))
    ch.append(cc)
expr=[red(sum(sum(ch[i][j]*(2-i)**(k-j)*h**(k-j)/S.factorial(k-j) for j in range(k+1)) for i in range(3))) for k in range(1,8)]
eq=[]
for e in expr:
    eq.extend(c for (ph,px),c in S.Poly(e,h,x).terms() if px>0)
us=list(reversed(us))
print('linear variables',len(us),'equations',len(eq),flush=True)
sol=next(iter(S.linsolve(eq,us)))
sub=dict(zip(us,sol))
free=set().union(*(e.free_symbols for e in sol))-{h,x}
print('remaining',sorted(free,key=str),flush=True)
ccs=[];rankeq=[]
for i in [0,2]:
    co=[S.Integer(1)]
    for k in range(1,7):
        ck=red(sum((-1)**(j-1)*S.factorial(j)*ch[i][j].subs(sub)*co[k-j] for j in range(1,k+1))/k)
        # note Newton p_j=j!*ch_j
        co.append(S.expand(ck))
        if k>3:rankeq.extend(S.Poly(ck,h,x).coeffs())
    ccs.append(co)
rankeq=list(dict.fromkeys(S.factor(e) for e in rankeq if e!=0))
print('rank eq',len(rankeq),flush=True)
for e in rankeq:print(e,flush=True)
pickle.dump({'equations':rankeq,'vars':sorted(free,key=str),'sub':sub,'chern':ccs},open('workspace/agent3_ch313_reduced.pkl','wb'))
Path('workspace/agent3_ch313_reduce.py').write_text(Path(__file__).read_text())
