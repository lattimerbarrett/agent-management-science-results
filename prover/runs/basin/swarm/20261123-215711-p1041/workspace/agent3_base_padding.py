import numpy as np,itertools,json,random
# Exhaustive explicit construction, not membership assumptions.
subs=list(itertools.combinations(range(14),7))
xs=np.arange(16384,dtype=np.uint16)
maps=np.zeros((len(subs),16384),dtype=np.uint8)
for j,s in enumerate(subs):
 for k,i in enumerate(s):maps[j]|=((xs>>i)&1).astype(np.uint8)<<k
N=len(subs); offsets=np.arange(N,dtype=np.int32)[:,None]*128
full=(1<<14)-1; A=(1<<7)-1
seen=set();covered=0;cert={}; cases=[]
for a in range(8):
 B=((1<<a)-1)|(((1<<(7-a))-1)<<7)
 groups=[[i for i in range(14) if mask>>i&1] for mask in [A&B,A&~B,B&~A,full&~(A|B)]]
 for ds in itertools.product(*[range(len(g)+1) for g in groups]):
  if sum(ds)!=7:continue
  C=sum(1<<i for g,d in zip(groups,ds) for i in g[:d]);cases.append((A,B,C))
random.Random(1).shuffle(cases)
for ci,masks in enumerate(cases):
 s=np.zeros(16384,dtype=bool)
 for M in masks:s^=(xs & (full^M))==0
 support=np.flatnonzero(s);projected=maps[:,support]
 ns=np.bincount((projected+offsets).ravel(),minlength=N*128).reshape(N,128)
 hs=np.asarray([np.bincount(row,minlength=129) for row in ns],dtype=np.uint8)
 uniq,idx=np.unique(hs,axis=0,return_index=True)
 for h,mi in zip(uniq,idx):
  key=h.tobytes()
  if key in seen:continue
  seen.add(key);dp=1;base=0
  for n,c in enumerate(h):
   c=int(c)
   if not c:continue
   base+=c*min(n,128-n);v=abs(128-2*n);k=1
   while c:
    z=min(k,c);dp|=dp<<(z*v);c-=z;k*=2
  bits=dp<<base;new=bits&~covered
  low=new&((1<<1001)-1)
  while low:
   b=low&-low;w=b.bit_length()-1;cert[w]=[list(masks),int(mi),[(i,int(c)) for i,c in enumerate(h) if c]];low^=b
  covered|=bits
missing=[w for w in range(336,8193,2) if not(covered>>w&1)]
assert missing==[358,362],missing
# 358 and362 are separate affine-threeflat constructions.
print(len(cases),len(seen),missing)
json.dump(cert,open('workspace/agent3_padding_cert.json','w'))
open('workspace/agent3_padding_bits.txt','w').write(str(covered))
