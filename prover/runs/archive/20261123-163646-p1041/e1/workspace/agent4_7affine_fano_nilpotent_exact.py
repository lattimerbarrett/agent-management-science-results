import itertools,time,numpy as np,collections,pickle,json
start=time.time();ALL=127
LS=[sum(1<<(j-1) for j in range(1,8) if (j&1)),sum(1<<(j-1) for j in range(1,8) if ((j^(j>>1))&1)),sum(1<<(j-1) for j in range(1,8) if ((j^(j>>2))&1))]
QM=sum(1<<(j-1) for j in range(1,8) if j&4)
def insert(B,v):
 while v:
  p=v.bit_length()-1
  if p in B:v^=B[p]
  else:B[p]=v;return True
 return False
def reps(l):
 b={};insert(b,ALL);insert(b,l);piv=set(b);free=[1<<i for i in range(7) if i not in piv]
 rs=[]
 for t in range(32):
  v=0
  for i,u in enumerate(free):
   if t>>i&1:v^=u
  rs.append(v)
 return rs
RS=list(map(reps,LS))
spaces={1};todo=[1]
while todo:
 s=todo.pop();pts=[v for v in range(32) if s>>v&1]
 for v in range(1,32):
  if s>>v&1:continue
  t=s|sum(1<<(v^u) for u in pts)
  if t not in spaces:spaces.add(t);todo.append(t)
assert len(spaces)==374
bases=[]
for s in sorted(spaces):
 b={}
 for v in range(1,32):
  if s>>v&1:insert(b,v)
 if len(b)<=4:bases.append(list(b.values()))
def patterns(l,b):return [ALL^b,b,ALL^l^b,l^b]
H=[]
for bs in bases:
 rows=[RS[0][v] for v in bs]+[0]*(4-len(bs));h={127:1}
 for b in rows:
  hh=collections.Counter()
  for old,c in h.items():
   for t in patterns(LS[0],b):hh[old&t]+=c
  h=hh
 H.append([h.get(t,0) for t in range(128)])
ids=np.indices((32,32,32)).reshape(3,-1)
B0=np.array(RS[0],dtype=np.uint8)[ids[0]];B5=np.array(RS[1],dtype=np.uint8)[ids[1]];B6=np.array(RS[2],dtype=np.uint8)[ids[2]]
PAR=np.array([[(x&y).bit_count()%2 for y in range(128)] for x in range(128)],dtype=np.uint8)
K=np.zeros((32768,128),dtype=np.uint16)
for x0,x5,x6,y0,y5,y6 in itertools.product(range(2),repeat=6):
 c0=B0^(LS[0] if x0 else 0)^(0 if y0 else ALL)
 c5=B5^(LS[1] if x5 else 0)^(QM if x0 else 0)^(0 if y5 else ALL)
 c6=B6^(LS[2] if x6 else 0)^(0 if y6 else ALL)
 K+=PAR[c0&c5&c6]
W=np.asarray(H,dtype=np.uint16)@K.T
print('exactcases',W.size,'minmax',W.min(),W.max(),'foundevens',[w for w in [322,326,330,334] if np.any(W==w)],'sec',time.time()-start)
found={}
for target in [322,326,330,334]:
 wh=np.argwhere(W==target)
 if len(wh):
  i,j=map(int,wh[0]);rows=[RS[0][v] for v in bases[i]]+[0]*(4-len(bases[i]))+[RS[0][ids[0,j]],RS[1][ids[1,j]],RS[2][ids[2,j]]]
  shifts=[sum(1<<i for i,r in enumerate(rows) if r>>(j-1)&1) for j in range(1,8)]
  fs=[];f=0
  for j in range(1,8):
   pts=[]
   for x in range(128):
    y=(x if j&1 else 0)^((x&32) if j&2 else 0)^(((x&64)^(((x>>4)&1)<<5)) if j&4 else 0)^shifts[j-1]
    pt=x+(y<<7);pts.append(pt);f^=1<<pt
   fs.append(pts)
  assert f.bit_count()==target
  found[target]=(rows,shifts,fs,hex(f))
pickle.dump(found,open('workspace/agent4_7affine_fano_nilpotent_hits.pkl','wb'))
print('COUNTS near',[(w,int(np.sum(W==w))) for w in range(300,353,2)])
open('workspace/agent4_7affine_fano_nilpotent_exact.py','w').write(open(__file__).read())
