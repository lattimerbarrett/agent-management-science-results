"""Exact P4 three-degree checks in ranks <=6.
The edge-differential rank criterion removes every other composition.
All surviving numerical roots descend or peel a trivial extremal line.
"""
import sys,time,pickle
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from agent4_chow_two import *
from agent3_chgeneral import setup
from itertools import product

def equations3(parts):
 f=S.Integer(1);us=[]
 for i,r in enumerate(parts):
  g,vs=factor(r,i,2-i);f=S.expand(f*g);us+=vs
 out={}
 for (ct,ch,cx),c in S.Poly(f,t,h,x).terms():
  for (rh,rx),rc in redmon(ch,cx).items():
   key=(ct,rh,rx);out[key]=out.get(key,0)+rc*c
 return list(dict.fromkeys(S.expand(c) for (ct,ch,cx),c in out.items() if cx>0 and c!=0)),us

def complete(gb,vs):
 sols=S.solve_poly_system(list(gb),*vs)
 assert sols is not None
 coordinates=[sorted(set(v[j] for v in sols)) for j in range(len(vs))]
 for v,vals in zip(vs,coordinates):
  f=S.prod(v-a for a in vals)
  assert any(gb.reduce(S.expand(f**k))[1]==0 for k in range(1,9))
 found=[]
 for values in product(*coordinates):
  sub=dict(zip(vs,values))
  if all(e.subs(sub)==0 for e in gb):found.append(values)
 assert set(found)==set(sols)
 return [dict(zip(vs,sol)) for sol in sols]

def main():
 triples={r:[(a,b,r-a-b) for a in range(1,r) for b in range(1,r-a)
             if a*b>=3 and b*(r-a-b)>=3] for r in range(3,7)}
 assert triples=={3:[],4:[],5:[(1,3,1)],6:[(1,3,2),(1,4,1),(2,2,2),(2,3,1)]}
 for parts in [(1,3,1),(1,4,1),(1,3,2)]:
  eq,vs=equations3(parts);vs=list(reversed(vs))
  gb=S.groebner(eq,*vs)
  sols=complete(gb,vs)
  assert len(sols)==3
  for sol in sols:
   A=[sol[S.Symbol(f'u{i}_1_0')] for i in range(3)]
   if A[0]==0 or A[2]==0:continue
   assert parts==(1,3,2) and A==[-1,0,1]
   assert sol[S.Symbol('u2_2_0')]==sol[S.Symbol('u2_2_1')]==0
   # Dual-top rank2 has c1=-s,c2=0, so peel a bottom O(0).
  print(parts,': all 3 exact roots descend or peel bottom O.')
 eq,vs=setup((2,2,2));vs=list(reversed(vs))
 gb=S.groebner(eq,*vs,order='grevlex').fglm('lex')
 sols=complete(gb,vs)
 assert len(sols)==1 and all(v==0 for v in sols[0].values())
 # Recover all character variables and eliminations to verify c1 top=0.
 assert sols[0][S.Symbol('v0_1_0')]==0
 print('(2,2,2): unique exact root; top c1=0, hence descent.')
if __name__=='__main__':main()
