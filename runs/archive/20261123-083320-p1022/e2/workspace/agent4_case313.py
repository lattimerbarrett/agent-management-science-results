import sys
sys.path.insert(0,'workspace')
from agent4_chow_two import *
parts=(3,1,3)
factors=[factor(r,i,2-i) for i,r in enumerate(parts)]
us=sum((v for f,v in factors),[])
prod=S.prod(f for f,v in factors)
out={}
for (ct,ch,cx),c in S.Poly(S.expand(prod),t,h,x).terms():
    for (rh,rx),rc in redmon(ch,cx).items():
        key=ct,rh,rx
        out[key]=out.get(key,0)+rc*c
eqs=list(dict.fromkeys(S.expand(c) for (ct,ch,cx),c in out.items() if cx>0 and c!=0))
print('unknowns',len(us),'eqs',len(eqs),flush=True)
start=time.time()
original_eqs=eqs[:]
original_us=us[:]
back={}
while True:
    hit=None
    for e in eqs:
      for u in reversed(us):
        c=S.diff(e,u)
        if c!=0 and not c.free_symbols:
          hit=(e,u,c);break
      if hit:break
    if not hit:break
    e,u,c=hit
    val=S.expand(u-e/c)
    back={k:S.expand(v.subs(u,val)) for k,v in back.items()}
    back[u]=val
    eqs=list(dict.fromkeys(S.expand(z.subs(u,val)) for z in eqs if z!=e))
    eqs=[z for z in eqs if z!=0]
    us.remove(u)
print('After linear elimination',len(us),len(eqs),'unknowns',us,flush=True)
for e in eqs:print('EQ',S.factor(e),flush=True)
import json
pickle.dump((eqs,us,back),open('workspace/agent4_cw_313_reduced.pkl','wb'))
gb=S.groebner(eqs,*reversed(us),order='grevlex',modulus=32003)
print('grevlex complete',time.time()-start,flush=True)
if gb.is_zero_dimensional:gb=gb.fglm('lex')
print('elapsed',time.time()-start,'basislength',len(gb.polys),'zero_dim',gb.is_zero_dimensional,flush=True)
pickle.dump((eqs,us,gb),open('workspace/agent4_cw_3_1_3.pkl','wb'))
for p in gb.polys: print(S.factor(p.as_expr()),flush=True)
sol=S.solve([p.as_expr() for p in gb.polys],us,dict=True)
print('Solutions',len(sol),flush=True)
for so in sol:
    assert all(S.expand(e.subs(so))==0 for e in eqs)
    print(so,flush=True)
