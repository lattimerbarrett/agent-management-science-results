import itertools,time,pickle,json
from pathlib import Path
from sage.all import GF,matrix
from sage.coding.binary_code import weight_dist
F=GF(2**10,name='a');z=F.multiplicative_generator()**93
perm=[int((z*F.from_integer(x)).to_integer()) for x in range(1024)]
orbs=[];ids=[-1]*1024
for x in range(1024):
 if ids[x]>=0:continue
 O=[];y=x
 while ids[y]<0:ids[y]=len(orbs);O.append(y);y=perm[y]
 orbs.append(O)
assert len(orbs)==94 and all(len(O)==11 for O in orbs[1:])
rows=[1<<ids[x] for x in range(1024)]
for i in range(10):
 for x in range(1024):
  if x>>i&1:rows[x]^=rows[x^(1<<i)]
def kernel(r):
 bas={}
 for x,v in enumerate(rows):
  if x.bit_count()<=r:continue
  while v:
   p=v.bit_length()-1
   if p not in bas:bas[p]=v;break
   v^=bas[p]
 out=[]
 for f in range(94):
  if f in bas:continue
  v=1<<f
  for p in sorted(bas):
   if (v&bas[p]).bit_count()%2:v^=1<<p
  out.append(v)
 return out
results={};start=time.time()
for r in [3,4,5,6,7]:
 K=kernel(r);print('r',r,'dim',len(K),flush=True)
 results[r]={'K':K}
 if r>4:continue
 truth=[[int(v>>ids[x])&1 for x in range(1024)] for v in K]
 if len(K)<=31:
  wd=weight_dist(matrix(GF(2),truth));mi=min(i for i in range(1,1025) if wd[i]);results[r]['minimum']=mi;print('MIN',r,mi,flush=True)
 else:
  mi=1024;partial=[]
  for mask in range(1,1<<(len(K)-30)):
   v=0
   for i in range(len(K)-30):
    if mask>>i&1:v^=K[30+i]
   G=matrix(GF(2),truth[:30]+[[int(v>>ids[x])&1 for x in range(1024)]])
   wd=weight_dist(G);mm=min(i for i in range(1,1025) if wd[i]);mi=min(mi,mm);partial.append(mm)
   print('COVER',r,mask,'min',mm,'overall',mi,'sec',time.time()-start,flush=True)
  results[r]['minimum']=mi;results[r]['cover_minima']=partial
pickle.dump({'orbits':orbs,'ids':ids,'rows':rows,'results':results},open('workspace/agent2_C11_local_data.pkl','wb'))
print('DONE','minima',{r:x.get('minimum') for r,x in results.items()},'time',time.time()-start,flush=True)
Path('workspace/agent2_C11_local_distances.py').write_text(Path('scratchpad.py').read_text())
