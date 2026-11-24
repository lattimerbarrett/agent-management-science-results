from pathlib import Path
import sys
sys.path.insert(0,'workspace')
from rank2_words import red,inv,mul,apply,comp

def comm(u,v):return mul(u,v,inv(u),inv(v))
def auto_comm(A,Ai,B,Bi):return comp(comp(comp(A,B),Ai),Bi)
def T(n,i,u):return tuple(mul((j,),u) if j==i else (j,) for j in range(1,n+1))
def P(n,i,v):return tuple((j,) if j==i else mul(v,(j,),inv(v)) for j in range(1,n+1))
for n in range(3,7):
 for i in range(1,n+1):
  other=[j for j in range(1,n+1) if j!=i]
  for a in other:
   for b in other:
    if a==b:continue
    u=comm((a,),(b,))
    for c in other:
     for d in other:
      if c==d:continue
      v=comm((c,),(d,))
      Tu,Tui=T(n,i,u),T(n,i,inv(u))
      Tv,Tvi=T(n,i,v),T(n,i,inv(v))
      Pv,Pvi=P(n,i,v),P(n,i,inv(v))
      assert auto_comm(Tv,Tvi,Tu,Tui)==auto_comm(Pv,Pvi,Tu,Tui)==T(n,i,comm(v,u))
print('PASS all same-target tail-commutator identities for n=3..6')
