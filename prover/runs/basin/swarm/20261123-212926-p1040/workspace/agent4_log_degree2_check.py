from fractions import Fraction as F
from itertools import permutations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from agent4_exact_mccool import br,add

def polyadd(a,b,s=1):return add(a,b,s)
def mul(a,b):
 c={}
 for w,v in a.items():
  for z,t in b.items():c[w+z]=c.get(w+z,0)+v*t
 return {w:v for w,v in c.items() if v}
def bracket(a,b):return add(mul(a,b),mul(b,a),-1)
def K(i,j):return {(i,(j,i)):1,(i,(i,j)):-1}
def T(i,j,k):return {(i,(j,k)):1,(i,(k,j)):-1}
for i,j,k in permutations(range(3)):
 Xi={(i,):1};Xj={(j,):1};Xk={(k,):1};C=bracket(Xj,Xk)
 expect=add(bracket(add(Xj,Xk,1),C),bracket(C,Xi),1)
 expect={(i,w):v for w,v in expect.items()}
 actual=add(br(add(K(k,j),K(j,k),1),T(i,j,k)),br(K(i,j),K(i,k)),-1)
 assert actual==expect,(i,j,k)
print('All six logarithmic degree-two identities verified exactly.')
