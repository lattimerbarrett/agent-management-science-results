"""Exact flag-Chern checks for uniform bundles of rank at most3 on P2."""
import sys
sys.path.insert(0,'workspace')
import sympy as s
from agent2_p2_chern_constraints import constraints
from agent1_chern_eliminate import eliminate

def check():
 for ranks in ((1,1),(1,2),(2,1)):
  eq,vs,_=constraints(ranks,(0,1));eq,vs,_=eliminate(eq,vs)
  a=vs[0]
  gb=s.groebner(eq,*vs,domain=s.QQ)
  assert list(gb)==[a*a-a]
 eq,vs,_=constraints((1,1,1),(0,1,2));eq,vs,_=eliminate(eq,vs)
 a,v=vs
 gb=s.groebner(eq,*vs,order='grevlex',domain=s.QQ)
 expected=[v**3-v,2*a*a-4*a+v*v-v,2*a*v+v*v-v]
 assert all(gb.reduce(e)[1]==0 for e in expected)
 assert set(s.solve(list(gb),vs))=={(0,0),(0,1),(1,-1),(2,0)}
 assert [p for p in s.solve(list(gb),vs) if p[0] and p[0]+p[1]]==[(2,0)]
 print('P2 rank<=3: two-block roots0,1; width3 sole nonconstant root(2,0).')
 return True
if __name__=='__main__':
 check()
