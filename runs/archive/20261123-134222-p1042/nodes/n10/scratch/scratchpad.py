import pickle,heapq,math,time
from functools import reduce

def eliminate(cols,nrows):
 cols=[dict(c) for c in cols]
 rows=[{} for _ in range(nrows)]
 for j,c in enumerate(cols):
  for i,v in c.items(): rows[i][j]=v
 heap=[]
 for j,c in enumerate(cols):
  if c: heapq.heappush(heap,(len(c),j))
 count=0
 while heap:
  _,j=heapq.heappop(heap);c=cols[j]
  units=[i for i,v in c.items() if abs(v)==1]
  if not units:continue
  i=min(units,key=lambda x:len(rows[x])); a=c[i]
  for jj,v in list(rows[i].items()):
   if jj==j:continue
   fac=v*a;cc=cols[jj]
   for ii,w in c.items():
    z=cc.get(ii,0)-fac*w
    if z:cc[ii]=z;rows[ii][jj]=z
    else:cc.pop(ii,None);rows[ii].pop(jj,None)
   if cc:heapq.heappush(heap,(len(cc),jj))
  for ii in list(c):rows[ii].pop(j,None)
  c.clear();count+=1
 return count,[c for c in cols if c]

if __name__=='__main__':
 for m in [9,10,11,12]:
  dims,mats=pickle.load(open(f'mats{m}.pkl','rb'));t=time.time()
  piv,rem=eliminate(mats[3],dims[3]); keys=sorted(set(i for c in rem for i in c))
  print(m,'units',piv,'residual shape',len(keys),len(rem),'gcd',reduce(math.gcd,(v for c in rem for v in c.values()),0),'sec',time.time()-t,flush=True)
  pickle.dump((piv,keys,rem),open(f'rem{m}.pkl','wb'))
