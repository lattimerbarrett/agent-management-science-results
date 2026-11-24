import sys,itertools,sympy as S
sys.path.insert(0,'workspace')
from agent4_chow_two import equations
for parts,expected in [((1,6),2),((2,5),2),((3,4),4)]:
 es,us=equations(parts)
 gb=S.groebner(es,*reversed(us),domain=S.QQ)
 roots=S.solve([p.as_expr() for p in gb.polys],us,dict=True)
 assert len(roots)==expected
 vals=[sorted({v[u] for v in roots}) for u in us]
 for u,vs in zip(us,vals):
  f=S.prod(u-v for v in vs)
  assert any(gb.reduce(S.expand(f**power))[1]==0 for power in range(1,9))
 good=[]
 for row in itertools.product(*vals):
  v=dict(zip(us,row))
  if all(S.expand(e.subs(v))==0 for e in es):good.append(row)
 assert set(good)=={tuple(v[u] for u in us) for v in roots}
 print(parts,expected,'roots, complete exact finite-grid check')
