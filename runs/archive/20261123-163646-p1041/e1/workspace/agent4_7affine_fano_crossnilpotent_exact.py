import itertools,time,numpy as np,collections,pickle
start=time.time();ALL=127
I=sum(1<<(j-1) for j in range(1,8) if j&1);PM=sum(1<<(j-1) for j in range(1,8) if j&2);QM=sum(1<<(j-1) for j in range(1,8) if j&4)
def insert(B,v):
 while v:
  p=v.bit_length()-1
  if p in B:v^=B[p]
  else:B[p]=v;return True
 return False
b={};insert(b,ALL);insert(b,I);free=[1<<j for j in range(7) if j not in b];RS=[]
for t in range(32):RS.append(sum(free[j] for j in range(5) if t>>j&1))
spaces={1};todo=[1]
while todo:
 s=todo.pop();pts=[v for v in range(32) if s>>v&1]
 for v in range(1,32):
  if s>>v&1:continue
  t=s|sum(1<<(v^u) for u in pts)
  if t not in spaces:spaces.add(t);todo.append(t)
assert len(spaces)==374
bases=[];H=[]
for s in sorted(spaces):
 b={}
 for v in range(1,32):
  if s>>v&1:insert(b,v)
 bs=list(b.values());bases.append(bs);rows=[RS[v] for v in bs]+[0]*(5-len(bs));h={127:1}
 for bb in rows:
  hh=collections.Counter()
  for old,c in h.items():
   for t in [ALL^bb,bb,ALL^I^bb,I^bb]:hh[old&t]+=c
  h=hh
 H.append([h.get(t,0) for t in range(128)])
ids=np.indices((64,64)).reshape(2,-1);B5=ids[0].astype(np.uint8);B6=ids[1].astype(np.uint8)
PAR=np.array([[(x&y).bit_count()%2 for y in range(128)] for x in range(128)],dtype=np.uint8)
K=np.zeros((4096,128),dtype=np.uint16)
for x5,x6,y5,y6 in itertools.product(range(2),repeat=4):
 c5=B5^(I if x5 else 0)^(PM if x6 else 0)^(0 if y5 else ALL)
 c6=B6^(I if x6 else 0)^(QM if x5 else 0)^(0 if y6 else ALL)
 K+=PAR[c5&c6]
W=np.asarray(H,dtype=np.uint16)@K.T
print('exactcases',W.size,'minmax',W.min(),W.max(),'foundevens',[w for w in [322,326,330,334] if np.any(W==w)],'sec',time.time()-start)
found={}
for target in [322,326,330,334]:
 wh=np.argwhere(W==target)
 if len(wh):
  i,j=map(int,wh[0]);rows=[RS[v] for v in bases[i]]+[0]*(5-len(bases[i]))+[int(B5[j]),int(B6[j])]
  shifts=[sum(1<<i for i,r in enumerate(rows) if r>>(j-1)&1) for j in range(1,8)]
  fs=[];f=0
  for j in range(1,8):
   pts=[]
   for x in range(128):
    y=(x if j&1 else 0)^((((x>>6)&1)<<5) if j&2 else 0)^((((x>>5)&1)<<6) if j&4 else 0)^shifts[j-1]
    pt=x+(y<<7);pts.append(pt);f^=1<<pt
   fs.append(pts)
  assert f.bit_count()==target
  found[target]=(rows,shifts,fs,hex(f))
pickle.dump(found,open('workspace/agent4_7affine_fano_crossnilpotent_hits.pkl','wb'))
print('COUNTS near',[(w,int(np.sum(W==w))) for w in range(300,401,2)])
open('workspace/agent4_7affine_fano_crossnilpotent_exact.py','w').write(open(__file__).read())
