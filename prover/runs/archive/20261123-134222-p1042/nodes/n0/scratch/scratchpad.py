import pickle,heapq
for m in [7,8]:
 dims,mats=pickle.load(open(f'mats{m}.pkl','rb')); cols=[dict(c) for c in mats[3]]
 rows=[{} for _ in range(dims[3])]
 for j,c in enumerate(cols):
  for i,v in c.items(): rows[i][j]=v
 heap=[]
 for j,c in enumerate(cols):
  if len(c): heapq.heappush(heap,(len(c),j))
 count=0
 while heap:
  _,j=heapq.heappop(heap);c=cols[j]
  units=[i for i,v in c.items() if abs(v)==1]
  if not units:continue
  i=min(units,key=lambda x:len(rows[x])); a=c[i]
  for jj,v in list(rows[i].items()):
   if jj==j:continue
   fac=v*a
   cc=cols[jj]
   for ii,w in c.items():
    z=cc.get(ii,0)-fac*w
    if z:cc[ii]=z;rows[ii][jj]=z
    else:cc.pop(ii,None);rows[ii].pop(jj,None)
   if cc:heapq.heappush(heap,(len(cc),jj))
  for ii in list(c): rows[ii].pop(j,None)
  c.clear();count+=1
 rem=[c for c in cols if c]
 print(m,count,len(rem),rem[:3],flush=True)
