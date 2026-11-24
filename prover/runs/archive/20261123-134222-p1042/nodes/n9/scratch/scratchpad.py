import itertools as it
from collections import Counter, deque

def check(m):
 k=m-5
 faces=[]
 # choices -1: empty, 0..3: row
 for a in it.product(range(-1,4), repeat=m):
  cnt=Counter(a)
  if cnt[0]>2 or cnt[1]>2 or cnt[2]>2 or cnt[3]>k:continue
  if cnt[-1]==m:continue
  faces.append(a)
 ids={a:i for i,a in enumerate(faces)}
 pairs={};critical=Counter()
 for a in faces:
  q=sum(x in (0,1,2) for x in a)
  p=next(j for j,x in enumerate(a) if x in (-1,3))
  if q==0 and a[p]==3 and a.count(3)==1:
   critical[0]+=1;continue
  if a[p]==-1 and a.count(3)==k:
   critical[q+k-1]+=1;continue
  b=list(a);b[p]=3 if a[p]==-1 else -1;b=tuple(b)
  assert b in ids
  pairs[ids[a]]=ids[b]
 assert all(pairs.get(j)==i for i,j in pairs.items())
 n=len(faces); out=[[] for _ in range(n)];ind=[0]*n
 for i,a in enumerate(faces):
  for j,x in enumerate(a):
   if x==-1:continue
   b=a[:j]+(-1,)+a[j+1:]
   if b not in ids:continue
   l=ids[b]
   s,t=(l,i) if pairs.get(i)==l else (i,l)
   out[s].append(t);ind[t]+=1
 que=deque(i for i in range(n) if ind[i]==0);visited=0
 while que:
  i=que.popleft();visited+=1
  for j in out[i]:
   ind[j]-=1
   if ind[j]==0:que.append(j)
 print('m=',m,'faces=',n,'matched pairs=',len(pairs)//2,'critical cells=',dict(sorted(critical.items())), 'acyclic=',visited==n,flush=True)
for m in [7,8]:check(m)
