from fractions import Fraction as F
from math import comb,factorial
from functools import lru_cache
from agent1_cycle_counter import star,triangle
@lru_cache(None)
def cross(a,b,pa,pb):
 return sum((F(comb(a-pa,k-pa)*comb(b-pb,k-pb)*factorial(k)*factorial(k-1),2) for k in range(max(1,pa,pb),min(a,b)+1)),F(0))
def pol(components):
 coeff={(0,0):1};cy=0
 for _,a,c in components:
  cy+=c;new={}
  for (p,e),v in coeff.items():
   for (q,f),w in a.items():new[p+q,e+f]=new.get((p+q,e+f),0)+v*w
  coeff=new
 return coeff,cy
def count(a,b,compA,compB):
 A,ca=pol(compA);B,cb=pol(compB)
 ans=F(ca+cb)-F(a*b,2)
 for (pa,ea),va in A.items():
  for (pb,eb),vb in B.items():ans+=va*vb*2**(pa+pb)*cross(a-ea,b-eb,pa,pb)
 assert ans.denominator==1
 return int(ans)
if __name__=='__main__':
 for m in [4,5,10,20,50,100,150,200,500,1000]:
  if m<4:continue
  cc=count(m+1,m,[star(4)],[])
  vals=[count(m+1,m,[x],[y]) for x in [star(3),triangle()] for y in [star(3),triangle()]]
  if m>=150:assert cc>max(vals)
  print('m',m,'competitor beats all',cc>max(vals),'relative gains',[float(F(cc,v)-1) for v in vals])
