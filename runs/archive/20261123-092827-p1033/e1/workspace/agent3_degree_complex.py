from itertools import combinations
from math import comb

def rank2(cols):
 basis={}
 for c in cols:
  while c:
   k=c.bit_length()-1
   if k in basis:c^=basis[k]
   else:basis[k]=c;break
 return len(basis)

def homology(n,D):
 E=list(combinations(range(n),2));N=len(E)
 faces=[[] for _ in range(N+1)]
 for mask in range(1<<N):
  deg=[0]*n
  for i,(a,b) in enumerate(E):
   if mask>>i&1:deg[a]+=1;deg[b]+=1
  if all(not(mask>>i&1) or deg[a]+deg[b]-2<=D for i,(a,b) in enumerate(E)):
   faces[mask.bit_count()].append(mask)
 rs=[0]*(N+2)
 for k in range(1,N+1):
  if not faces[k]:continue
  lookup={x:i for i,x in enumerate(faces[k-1])}
  cols=[]
  for x in faces[k]:
   y=x;col=0
   while y:
    b=y&-y;y-=b;col^=1<<lookup[x^b]
   cols.append(col)
  rs[k]=rank2(cols)
 hs=[(k-1,len(faces[k])-rs[k]-rs[k+1]) for k in range(1,N+1) if len(faces[k])-rs[k]-rs[k+1]]
 return hs,[len(x) for x in faces if x]
for n in range(3,7):
 for D in (0,1,2,3,4):
  hs,fs=homology(n,D)
  print('n',n,'D',D,'tau',n-1,'Htilde',hs,'faces',fs,flush=True)
