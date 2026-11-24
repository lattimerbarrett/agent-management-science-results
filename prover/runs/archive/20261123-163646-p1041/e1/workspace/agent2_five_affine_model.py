"""Necessary affine-flat intersection model. Run with Python + z3.
Use minimality for all n, together
with classical KT normal forms below 2d: weights <192,224,240
can be represented with <=1,2,3 minimum words, respectively.
This proves a restricted representation obstruction, not nonexistence in RM.
"""
from z3 import *
import itertools,time
TARGETS=(322,326,330,334)
def triple_weights():
 W={384}
 for t in range(8):
  for a,b,c in itertools.product(range(t,8),repeat=3):
   if max(a+b,a+c,b+c)<=7+t:W.add(384-2*((1<<a)+(1<<b)+(1<<c))+4*(1<<t))
 for a,b,c in itertools.product(range(7),repeat=3):
  if max(a+b,a+c,b+c)-min(a,b,c)<=6:W.add(384-2*((1<<a)+(1<<b)+(1<<c)))
 for a,b in itertools.product(range(7),repeat=2):W.add(384-2*((1<<a)+(1<<b)))
 for a in range(8):W.add(384-2*(1<<a))
 return W
def check(n):
 H=1<<n; count=2*H
 D={0:IntVal(15)}|{S:Int('d%d_%d'%(n,S)) for S in range(1,count)}
 V={S:Int('v%d_%d'%(n,S)) for S in range(1,H)}
 s=Solver();s.set(timeout=120000)
 for S in range(1,count):
  upper=14 if S==H else (7 if S&H else 8)
  s.add(D[S]>=0,D[S]<=upper)
 singles=[1<<i for i in range(n)]
 for S in singles:s.add(D[S]==8,D[S|H]==7)
 # Weight 2 mod4 forces a pair meeting in a single affine point.
 s.add(D[H]==14,D[3]==1,D[3|H]==0)
 for A in range(count):
  for B in range(count):
   if A&B==A:s.add(D[B]<=D[A])
   s.add(D[A|B]+D[A&B]>=D[A]+D[B])
 # Dual Ingleton inequality for intersections of vector subspaces.
 for A,B,C,E in itertools.permutations(singles+[H],4):
  s.add(D[A|B]+D[A|C]+D[A|E]+D[B|C]+D[B|E]<=D[A]+D[B]+D[C|E]+D[A|B|C]+D[A|B|E])
 for S in range(1,H):
  s.add(Or(And(V[S]==0,D[S]==D[S|H]),*[And(V[S]==(1<<j),D[S]==j+1,D[S|H]==j) for j in range(8)]))
 def wt(T):return Sum([(-2)**(S.bit_count()-1)*V[S] for S in range(1,H) if S&T==S])
 if n>=4:
  W3=triple_weights()
  for T in range(1,H-1):
   k=T.bit_count();z=wt(T)
   if k==2:s.add(z>=192)
   elif k==3:s.add(Or(*[z==w for w in W3 if w>=224]))
   elif k==4:s.add(z>=240,*[z!=w for w in TARGETS])
 if n==5:
  # If all six endpoint pair intersections have size <=8, P<=145,
  # so Bonferroni gives weight>=640-290=350. Normalize the largest.
  s.add(V[5]>=16,V[5]>=V[9],V[9]>=V[17],V[5]>=V[6],V[5]>=V[10],V[5]>=V[18])
 w=wt(H-1);s.add(Or(*[w==t for t in TARGETS]))
 t=time.time();r=s.check();print(n,r,round(time.time()-t,3),flush=True)
 assert r==unsat
if __name__=='__main__':
 print('necessary triple weights:',sorted(triple_weights()))
 for n in (3,4,5):check(n)
