import heapq,time
from collections import Counter
from itertools import combinations,product
def reduce_bd(bd,sz,verbose=True):
 N=len(bd); cb=[{} for _ in bd]; alive=set(range(N))
 for j,col in enumerate(bd):
  for i,v in col.items(): cb[i][j]=v
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
 return bd,alive


def fiber_complex(m):
 r=m-5;gens=[];sizes=[]
 for k in range(5):
  for cols in combinations(range(m),k):
   S=[x for x in range(m) if x not in cols];p=S[0]
   for colors in product(range(3),repeat=k):
    if any(colors.count(c)>2 for c in range(3)):continue
    A=tuple(zip(cols,colors))
    for T in combinations(S[1:],r):gens.append((A,T));sizes.append(k)
 idx={g:i for i,g in enumerate(gens)};bd=[]
 for A,T in gens:
  out={};cols=[x[0] for x in A];p=next(x for x in range(m) if x not in cols)
  for a,(j,c) in enumerate(A):
   A1=A[:a]+A[a+1:]
   if j>p:out[idx[A1,T]]=(-1)**a
   else:
    U=(p,)+T
    for b in range(len(U)):
     T1=U[:b]+U[b+1:];out[idx[A1,T1]]=(-1)**(a+b)
  bd.append(out)
 return gens,bd,sizes
