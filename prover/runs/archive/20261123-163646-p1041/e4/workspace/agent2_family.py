import itertools,pickle
D={}
for n in range(8):
 for r in range(n+1):
  N=1<<n
  if r==n: W=set(range(N+1))
  elif r==0:W={0,N}
  else:
   V=D[r-1,n-1];W={a+b for a in V for b in V}|{2*a for a in D[min(r,n-1),n-1]}
  # pairs affine min spaces
  d=n-r
  W|={2*(1<<d)-2*(1<<t) for t in range(max(0,2*d-n),d+1)}
  for t,p,q,z in itertools.product(range(d+1),repeat=4):
   blocks=(t,p-t,q-t,z-t,d-p-q+t,d-p-z+t,d-q-z+t)
   if min(blocks)>=0 and sum(blocks)<=n:
    W.add(3*(1<<d)-2*((1<<p)+(1<<q)+(1<<z))+4*(1<<t))
  W|={N-w for w in list(W)}
  D[r,n]=W
for r in range(1,7): print(r,sorted(D[r,7]))
import numpy as np
W=set()
for s in range(1,4):
 for p in sorted(D[s,7]):
  for q in sorted(D[7-s,7]):
   if p%2 or q%2 or p>64 or q>64: continue
   nx,mx,ny,my=128-p,p,128-q,q
   hits=np.zeros(8193,dtype=bool)
   ar=np.arange(-ny//2,ny//2+1)[:,None];br=np.arange(-my//2,my//2+1)[None,:]
   for u in range(nx//2+1):
    for v in range(-mx//2,mx//2+1):
     if abs(u+v)*(ny//2)+abs(u-v)*(my//2)<3400:continue
     vals=((u+v)*ar+(u-v)*br).ravel()+4096
     hits[vals]=True
   W.update(8192-2*(i-4096) for i in np.flatnonzero(hits))
 print('s',s,'W',len(W), 'missing low',len(set(range(308,1333,2))-W),flush=True)
missing=sorted(set(range(308,8193,2))-W)
print('missing',len(missing),missing)
assert missing == [310,316,322,326,328,330,332,334,340,342,348,354,356,358,360,364,370,372,388,390,396,402,406,412,418,420,426,454,460,466,486,490,498,522,546,742]
pickle.dump((D,W),open('workspace/agent2family.pkl','wb'))