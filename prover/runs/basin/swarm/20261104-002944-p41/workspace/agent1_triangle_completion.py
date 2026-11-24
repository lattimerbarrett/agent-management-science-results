from itertools import combinations
from collections import deque
import random,time,json

def complete_triangles(raw,n,seed=0):
 rng=random.Random(seed);bs=[1<<i for i in range(n)]
 def bits(f):return [b for b in bs if b&f]
 def tris(f):return [f^b for b in bits(f)]
 FS={sum(1<<v for v in f) for f in raw}
 T={t for f in FS for t in tris(f)}
 E={sum(e) for f in FS for e in combinations(bits(f),2)}
 co={};C=[];Q=deque();order=[]
 def insert_triangle(t):
  for b in bs:
   if t&b:continue
   f=t|b;c=co.get(f,0)+1
   if c==4:del co[f]
   else:
    co[f]=c
    if c==2:C.append(f)
    elif c==3:Q.append(f)
 for t in T:insert_triangle(t)
 def addf(f):
  order.append(f)
  for t in tris(f):
   if t in T:continue
   T.add(t);E.update(sum(e) for e in combinations(bits(t),2));insert_triangle(t)
 while True:
  while Q:
   f=Q.popleft()
   if co.get(f)==3:addf(f)
  if len(T)==n*(n-1)*(n-2)//6:return True,len(E),len(T),order
  while C:
   j=rng.randrange(len(C));C[j],C[-1]=C[-1],C[j];f=C.pop()
   if co.get(f)!=2:continue
   rr=[t for t in tris(f) if t in T]
   shared=rr[0]&rr[1];opposite=f^shared
   if opposite not in E:break
  else:return False,len(E),len(T),order
  addf(f)

if __name__=='__main__':
 raw=json.load(open('workspace/agent1_600cell.json'));tm=time.time()
 for trial in range(3):
  good,e,t,order=complete_triangles(raw,120,trial)
  print('600cell trial',trial,'complete',good,'edges',e,'triangles',t,'nontrivialsteps',len(order),'elapsed',time.time()-tm,flush=True)
  if not good:
   json.dump(order,open('workspace/agent1_600cell_stall.json','w'));break
