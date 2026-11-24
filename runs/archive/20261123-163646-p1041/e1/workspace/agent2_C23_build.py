import itertools,pickle,time,sys
from pathlib import Path
from sage.all import GF,matrix
from sage.coding.binary_code import weight_dist
mod=(1<<11)|5
def mul(x,y):
 z=0
 while y:
  if y&1:z^=x
  y>>=1;x<<=1
  if x>>11:x^=mod
 return z
perm=[mul(x,322) for x in range(2048)]
orbs=[];ids=[-1]*2048
for x in range(2048):
 if ids[x]>=0:continue
 O=[];y=x
 while ids[y]<0:ids[y]=len(orbs);O.append(y);y=perm[y]
 orbs.append(O)
assert len(orbs)==90 and all(len(O)==23 for O in orbs[1:])
rows=[1<<ids[x] for x in range(2048)]
for i in range(11):
 for x in range(2048):
  if x>>i&1:rows[x]^=rows[x^(1<<i)]
def reduce_rows(R):
 bas={}
 for r in R:
  while r:
   p=r.bit_length()-1
   if p not in bas:bas[p]=r;break
   r^=bas[p]
 return bas
def ker(bas,n):
 out=[]
 for f in range(n):
  if f in bas:continue
  v=1<<f
  for p in sorted(bas):
   if (v&bas[p]).bit_count()%2:v^=1<<p
  out.append(v)
 return out
for r in (3,4,5,6,7):
 bas=reduce_rows([row for x,row in enumerate(rows) if x.bit_count()>r]);K=ker(bas,90)
 print('degree',r,'dim',len(K),flush=True)
 if len(K)<=30:
  truth=[]
  for v in K:truth.append([int(v>>ids[x])&1 for x in range(2048)])
  wd=weight_dist(matrix(GF(2),truth));print('smallweights',[(i,int(c)) for i,c in enumerate(wd) if c and i<=400],flush=True)
fullrows=[1<<(ids[x&2047]+90*(x>>11)) for x in range(16384)]
for i in range(14):
 for x in range(16384):
  if x>>i&1:fullrows[x]^=fullrows[x^(1<<i)]
H=list(reduce_rows([row for x,row in enumerate(fullrows) if x.bit_count()>7]).values());K=ker(reduce_rows(H),720)
print('FULLH',len(H),'K',len(K),flush=True)
pickle.dump({'orbits':orbs,'ids':ids,'H':H,'K':K},open('workspace/agent2_C23_data.pkl','wb'))
Path('workspace/agent2_C23_build.py').write_text(Path('scratchpad.py').read_text())
