from fractions import Fraction as F
from functools import lru_cache
from math import factorial,log
import numpy as np
for r in range(3,21):
 cov=F(r-2,r*r)
 color_penalty=-F(1,2)/cov
 factorial_penalty=F(r,2)
 assert color_penalty+factorial_penalty==-F(r,r-2)
print('Exact uniform-saddle quadratic coefficients PASS r3..20')

def ham(parts):
 r=len(parts);n=sum(parts)
 @lru_cache(None)
 def f(counts,last,first):
  if not any(counts):return int(last!=first)
  ans=0
  for j,c in enumerate(counts):
   if c and j!=last:
    cc=list(counts);cc[j]-=1;ans+=f(tuple(cc),j,first)
  return ans
 words=0
 for j,c in enumerate(parts):
  if c:
   cc=list(parts);cc[j]-=1;words+=f(tuple(cc),j,j)
 num=words
 for c in parts:num*=factorial(c)
 assert num%(2*n)==0
 return num//(2*n)
for r,ms in [(3,[4,8,16]),(4,[4,8])]:
 for m in ms:
  aa=[m]*r;bb=aa[:];bb[0]+=1;bb[1]-=1
  H0,H1=ham(aa),ham(bb)
  val=r*m*log(H1/H0)
  print('Hamilton imbalance check',r,m,val,'target',-2*r/(r-2))
  assert H1<H0
print('Exact Hamilton DP checks PASS')
