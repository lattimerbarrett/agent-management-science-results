import itertools,json,pathlib,time,collections,random,sys
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese
rng=random.Random(381312);n=78;ALL=(1<<n)-1

def bas(rows):
 D={}
 for z in rows:
  while z:
   p=z.bit_length()-1
   if p in D:z^=D[p]
   else:D[p]=z;break
 return D

def solve(rows,bs=None):
 if bs is None:bs=[0]*len(rows)
 D={};rhs={}
 for z,b in zip(rows,bs):
  while z:
   p=z.bit_length()-1
   if p in D:z^=D[p];b^=rhs[p]
   else:D[p]=z;rhs[p]=b;break
  if z==0 and b:return None
 def back(z):
  for p in sorted(D):
   if ((D[p]&z).bit_count()&1)!=rhs[p]:z^=1<<p
  return z
 part=back(0);free=[i for i in range(n) if i not in D]
 # homogeneous solve removes affine particular
 ker=[back(1<<i)^part for i in free]
 return part,ker,D

def square(C):return list({a&b&c for i,a in enumerate(C) for j,b in enumerate(C[:i+1]) for c in C[:j+1]})
def patterns(C):return [sum(((r>>i)&1)<<j for j,r in enumerate(C)) for i in range(n)]
def independent(C,r):
 D=bas(C)
 while r:
  p=r.bit_length()-1
  if p in D:r^=D[p]
  else:return True
 return False

from agent1_checked_grid import witnesses,truth_table
import numpy as np
a,b,t=witnesses(5)[78];S=np.flatnonzero(truth_table(a,b,t,5)).tolist()
C=[ALL]+[sum(((p>>j)&1)<<i for i,p in enumerate(S)) for j in range(10)]
assert len(set(patterns(C)))==78
while True:
 _,ker,_=solve(square(C));extra=next((r for r in ker if independent(C,r)),None)
 if extra is None:break
 C.append(extra)
assert len(C)==13
print('initial',len(C),flush=True)
def drop(C):
 k=len(C);u=rng.randrange(1,1<<(k-1));pivot=u.bit_length()-1;rr=C[pivot+1]
 return [ALL]+[r^(rr if u>>j&1 else 0) for j,r in enumerate(C[1:]) if j!=pivot]
start=time.time();steps=0;accepted=0;best=len(C);firsthist=collections.Counter();lasthist=collections.Counter();blocked=0;hits=[]
while time.time()-start<115:
 steps+=1;k=len(C);D=drop(drop(C));sq=square(D)
 if max(collections.Counter(patterns(D)).values())>4:blocked+=1;continue
 _,firstker,_=solve(sq);firsthist[len(firstker)]+=1
 if len(firstker)==k:continue
 for attempt in range(6):
  r=0
  for b in firstker:
   if rng.getrandbits(1):r^=b
  if independent(D,r) and max(collections.Counter(patterns(D+[r])).values())<=2:break
 else:blocked+=1;continue
 D.append(r);pat=patterns(D);groups={}
 for i,a in enumerate(pat):groups.setdefault(a,[]).append(i)
 dup=[(1<<a[0])^(1<<a[1]) for a in groups.values() if len(a)==2]
 sq=square(D);sol=solve(sq+dup,[0]*len(sq)+[1]*len(dup))
 if sol is None:blocked+=1;continue
 part,ker,_=sol
 for attempt in range(5):
  r=part
  for b in ker:
   if rng.getrandbits(1):r^=b
  if independent(D,r):break
 else:blocked+=1;continue
 C=D+[r];accepted+=1
 _,K,_=solve(square(C));lasthist[len(K)]+=1
 while len(K)>len(C):
  extra=next((r for r in K if independent(C,r)),None)
  if extra is None:break
  C.append(extra);_,K,_=solve(square(C))
 if len(C)>best:
  best=len(C);print('NEW',best,steps,time.time()-start,flush=True);hits.append(C.copy())
  if best>=14:break
 if accepted%1000==0:assert len(set(patterns(C)))==78 and len(bas(C))==len(C)
print('steps',steps,'accepted',accepted,'best',best,'first',dict(firsthist),'last',dict(lasthist),'blocked',blocked,flush=True)
pathlib.Path('workspace/agent3_S78_grassmann.json').write_text(json.dumps({'steps':steps,'accepted':accepted,'best':best,'firsthist':dict(firsthist),'lasthist':dict(lasthist),'blocked':blocked,'hits':hits,'rows':C},indent=2))
