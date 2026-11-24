"""All two-block Chern-HN possibilities in ranks<=7 on P4.
Computes exact rational ideals; not merely finite sampling.
"""
import sympy as s
from agent4_chern_elimination import eliminate

def solutions(ranks):
 eq,vs,sub=eliminate(ranks)
 if not vs:
  assert not eq
  raw=[{}]
 else:
  gb=s.groebner(eq,*vs,order='grevlex')
  raw=s.solve(list(gb),vs,dict=True)
 out=[]
 for so in raw:
  # Sequential elimination expressions may refer to subsequently eliminated vars.
  full=dict(so)
  for v,val in reversed(list(sub.items())):
   full[v]=s.simplify(val.subs(full))
  for _ in range(len(full)):
   full={v:s.simplify(val.subs(full)) for v,val in full.items()}
  assert all(not val.free_symbols for val in full.values())
  fibre=tuple(full.get(s.Symbol('c0_%d0'%j),s.Integer(0)) for j in (1,2,3))
  out.append(fibre)
 return sorted(set(out))

def check():
 table={}
 for r in range(2,8):
  for high in range(1,r):
   low=r-high
   got=solutions((low,high))
   expected=[(0,0,0)]
   if high>=3:expected.append((1,0,0))
   if low>=3:expected.append((1,1,1))
   if low>=3 and high>=3:expected.append((2,2,0))
   assert got==expected,((low,high),got,expected)
   table[(low,high)]=got
   print((low,high),'low-block fibre (c1,c2,c3):',got)
 return table
if __name__=='__main__':check()
