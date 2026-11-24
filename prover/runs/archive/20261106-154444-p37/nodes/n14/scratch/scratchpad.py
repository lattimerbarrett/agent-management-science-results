from itertools import combinations
from math import comb,log2
for d in range(8,31):
 a=d//3;b=(d-a)//2;c=d-a-b;groups=[set(range(a)),set(range(a,a+b)),set(range(a+b,d))]
 m=sum(1 for T in combinations(range(1,d),d//2-1) if all((A:=set(T)|{0})&g and g-A for g in groups)) if d<=20 else None
 # inclusion-exclusion polynomial by require group splits and fixed0infirst
 def mul(p,q):
  r=[0]*(len(p)+len(q)-1)
  for i,x in enumerate(p):
   for j,y in enumerate(q):r[i+j]+=x*y
  return r
 p=[0]+[comb(a-1,i-1) for i in range(1,a)]+[0]
 for size in [b,c]:p=mul(p,[0]+[comb(size,i) for i in range(1,size)]+[0])
 mm=p[d//2];C=comb(d-2,(d-2)//2)
 print(d,(a,b,c),'rows',mm,'ratioC',round(mm/C,4),'vs1.5',mm>1.5*C,flush=True)
