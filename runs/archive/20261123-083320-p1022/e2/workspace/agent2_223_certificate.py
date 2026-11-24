"""Exact rank7 P4 width-three composition (2,2,3).
Regenerates all equations and QQ Groebner computation; no stored answer
or pickle required. Takes about one minute on the team's interpreter.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from agent3_chgeneral import setup
import sympy as S
from itertools import product

def main():
 eq,vs=setup((2,2,3));vs=list(reversed(vs))
 gb=S.groebner(eq,*vs,order='grevlex').fglm('lex')
 a,b,c,d,e=S.symbols('v0_1_0 v0_2_0 v0_2_1 v1_1_0 v1_2_0')
 # These exact ideal membership identities force every solution into
 # first c1 zero OR top rank2 c1=-2s,c2=0.
 for f in [d+2*e,d*(d+1),a*d,a*a+2*a+6*c,a*a-2*b,a*a*(a+2)]:
  assert gb.reduce(f)[1]==0
 sols=S.solve_poly_system(list(gb),*vs)
 assert set(sols)=={tuple(dict(zip([a,b,c,d,e],v))[u] for u in vs)
                    for v in [(0,0,0,0,0),(0,0,0,-1,S.Rational(1,2)),(-2,2,0,0,0)]}
 coordinates=[sorted(set(v[j] for v in sols)) for j in range(len(vs))]
 for v,vals in zip(vs,coordinates):
  f=S.prod(v-z for z in vals)
  assert any(gb.reduce(S.expand(f**k))[1]==0 for k in range(1,9))
 found=[]
 for values in product(*coordinates):
  ss=dict(zip(vs,values))
  if all(p.subs(ss)==0 for p in gb):found.append(values)
 assert set(found)==set(sols)
 for values in sols:
  ss=dict(zip(vs,values))
  assert all(f.subs(ss)==0 for f in eq)
  if ss[a]==0:continue
  assert ss[a]==-2 and ss[b]==2 and ss[c]==0
  # c2(F1)=((a²/2)-b)*s²-c*t =0.
  assert ss[a]**2/2-ss[b]==0 and ss[c]==0
 print('(2,2,3): all 3 complex roots descend or peel top O(2).')
 print('Residual multiplicities (1,2,3) have first-edge product 2 < 3.')
if __name__=='__main__':main()
