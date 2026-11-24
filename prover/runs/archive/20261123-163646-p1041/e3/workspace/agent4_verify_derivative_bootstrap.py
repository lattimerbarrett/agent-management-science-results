from fractions import Fraction
from math import comb
from itertools import combinations
W=(322,326,330,334)
for w in W:
 upper=Fraction(w)-2*comb(w,2)*Fraction(15,16383)+4*comb(w,3)*Fraction(210,16383*16382)
 assert upper<256
 for k in(3,4):
  mean=128+Fraction(1<<(k-1),(1<<k)-1)*(w-128)
  assert mean<256
  print('w,k,parentmean',w,k,mean)
 assert Fraction(2*w+128,3)<268
for k in(2,3,4):assert (1<<k)*167<96*((1<<(k+1))-1)
def rank(rows):
 d={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in d:x^=d[j]
   else:d[j]=x;break
 return len(d)
for k in(2,3,4):
 n=k+1;vectors=set()
 for ell in range(1,1<<n):
  b=[]
  for x in range(1,1<<n):
   if (x&ell).bit_count()%2==0 and rank(b+[x])>len(b):b.append(x)
  assert len(b)==k
  v=0
  for i,J in enumerate(combinations(range(n),k)):
   rows=[sum(((x>>j)&1)<<t for t,j in enumerate(J)) for x in b]
   v|=int(rank(rows)==k)<<i
  vectors.add(v)
 assert vectors==set(range(1,1<<n))
 for v in range(1,1<<k):assert sum((v&ell).bit_count()%2 for ell in range(1,1<<k))==1<<(k-1)
print('PASS derivative bootstrap: exact Bonferroni/parent bounds, coefficient minima,')
print('all exterior decomposability cases and all moment-functional average counts.')
