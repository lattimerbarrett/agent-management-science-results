"""Exact P4/rank7 width3 (133),(142) Chow certificates.
Uses agent3_chgeneral.setup to generate incidence and Newton equations.
"""
import sys,pickle,time,itertools
import sympy as S
sys.path.insert(0,'workspace')
from agent3_chgeneral import setup
for parts in [(1,3,3),(1,4,2)]:
 es,us=setup(parts)
 es=[S.Poly(e,*us).clear_denoms()[1].as_expr() for e in es]
 start=time.time();gb=S.groebner(es,*reversed(us),order='grevlex',domain=S.QQ).fglm('lex')
 sols=S.solve([p.as_expr() for p in gb.polys],us,dict=True)
 vals=[sorted({s[u] for s in sols}) for u in us]
 for u,vs in zip(us,vals):
  f=S.prod(u-v for v in vs)
  assert any(gb.reduce(S.expand(f**power))[1]==0 for power in range(1,9))
 grid=[]
 for tup in itertools.product(*vals):
  d=dict(zip(us,tup))
  if all(S.expand(e.subs(d))==0 for e in es):grid.append(tup)
 assert set(grid)=={tuple(d[u] for u in us) for d in sols}
 b=next(u for u in us if str(u)=='b0')
 assert {d[b] for d in sols}==({0,-1,-2} if parts==(1,3,3) else {0,-1})
 if parts==(1,3,3):
  exceptional=[v for v in sols if v[b]==-2]
  assert len(exceptional)==1
  assert all(v==0 for u,v in exceptional[0].items() if u!=b)
 print(parts,'exact roots',len(sols),'complete finite-grid certificate; seconds',time.time()-start,flush=True)
print('133 exceptional fiber partial-HN Chern: (1-2x)*1, so dual gg c1=2,c2=0.')
