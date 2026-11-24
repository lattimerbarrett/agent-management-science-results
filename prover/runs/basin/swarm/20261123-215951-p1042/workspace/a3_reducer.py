import heapq,time,pickle
from itertools import product
from collections import Counter

def faces_for(m):
 out=[]
 for x in product(range(5),repeat=m):
  c=Counter(x)
  if all(c[r]<=2 for r in [1,2,3]) and c[4]<=m-5:
   out.append(tuple(j*4+r-1 for j,r in enumerate(x) if r))
 return out

def reduce(faces,verbose=True):
 faces.sort(key=lambda f:(len(f),f));idx={f:i for i,f in enumerate(faces)}
 N=len(faces);bd=[{} for _ in faces];cb=[{} for _ in faces];alive=set(range(N));sz=[len(f) for f in faces]
 for j,f in enumerate(faces):
  for k in range(len(f)):
   i=idx[f[:k]+f[k+1:]];v=(-1)**k;bd[j][i]=v;cb[i][j]=v
 heap=[];serial=0
 def push(j):
  nonlocal serial
  if j in alive and bd[j]:
   cand=[(len(cb[i]),i) for i,v in bd[j].items() if abs(v)==1]
   if cand:
    deg,i=min(cand);heapq.heappush(heap,((len(bd[j])-1)*(deg-1),len(bd[j])+deg,serial,j,i));serial+=1
 for j in alive:push(j)
 count=0;t=time.time()
 while heap:
  _,_,_,j,i=heapq.heappop(heap)
  if j not in alive or i not in alive or abs(bd[j].get(i,0))!=1:continue
  a=bd[j][i];cols=list(cb[i]);affected=set()
  for k in cols:
   if k==j:continue
   mult=bd[k][i]*a
   for l,v in bd[j].items():
    z=bd[k].get(l,0)-mult*v
    if z:bd[k][l]=z;cb[l][k]=z
    else:bd[k].pop(l,None);cb[l].pop(k,None)
    affected.update(cb[l])
   affected.add(k)
  for l in list(bd[j]):cb[l].pop(j,None)
  for k in list(cb[j]):bd[k].pop(j,None);affected.add(k)
  for l in list(bd[i]):cb[l].pop(i,None)
  for k in list(cb[i]):bd[k].pop(i,None)
  bd[i].clear();cb[i].clear();bd[j].clear();cb[j].clear();alive.remove(i);alive.remove(j)
  for k in affected:push(k)
  count+=1
  if verbose and count%20000==0:print(count,'alive',len(alive),'nnz',sum(len(bd[k]) for k in alive),'heap',len(heap),'time',time.time()-t,flush=True)
  if len(heap)>2000000:
   heap=[]
   for k in alive:push(k)
 if verbose:print('DONE',count,Counter(sz[k] for k in alive),'coeffs',Counter(abs(v) for k in alive for v in bd[k].values()),flush=True)
 return faces,bd,alive
