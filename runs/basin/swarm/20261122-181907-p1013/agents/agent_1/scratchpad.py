from functools import lru_cache
from itertools import combinations,combinations_with_replacement

def embeds_power(k,p,caps,removed=()):
 removed=set(removed)
 @lru_cache(None)
 def f(i,last,sizes):
  if i==k:return ()
  if i in removed:
   ans=f(i+1,last,sizes)
   return (None,)+ans if ans is not None else None
  seen=set()
  for c,cap in enumerate(caps):
   state=(cap,last[c],sizes[c])
   if state in seen:continue
   seen.add(state)
   ns=sizes[c]+1 if i-last[c]<=p else 1
   if ns>cap:continue
   ll=list(last);ss=list(sizes);ll[c]=i;ss[c]=ns
   ans=f(i+1,tuple(ll),tuple(ss))
   if ans is not None:return (c,)+ans
  return None
 return f(0,(-k,)*len(caps),(0,)*len(caps))

def partvec(total,r,low=0):
 if r==0:
  if total==0:yield ()
  return
 for i in range(low,total+1):
  for t in partvec(total-i,r-1,i):yield (i,)+t

for r in range(2,7):
 for k in range(r+2, 3*r+3):
  print('r',r,'path length',k, 'min defect degrees',end=' ')
  for total in range(r+1):
   free=[]
   for ds in partvec(total,r):
    if embeds_power(k,r,tuple(d+1 for d in ds)) is None:free.append(ds)
   if not free:break
   print(total,free,end='; ')
  print()
