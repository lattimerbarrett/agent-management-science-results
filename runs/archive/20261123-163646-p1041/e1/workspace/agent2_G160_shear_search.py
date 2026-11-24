from pathlib import Path
import itertools,collections,json,time,random
n=12;ALL=(1<<4096)-1
masks=[sum(1<<i for i in [0,1,2,3,4,5]),sum(1<<i for i in [0,1,2,6,7,8]),sum(1<<i for i in [0,3,4,9,10,11])];shifts=[0,0,1<<5]
def spanmask(mask):return[x for x in range(4096) if x&~mask==0]
g=0
for mask,shift in zip(masks,shifts):
 for x in spanmask(mask):g^=1<<(x^shift)
assert g.bit_count()==160
# Mobius coefficients.
a=[(g>>x)&1 for x in range(4096)]
for i in range(12):
 for x in range(4096):
  if x>>i&1:a[x]^=a[x^(1<<i)]
assert max(x.bit_count() for x,v in enumerate(a) if v)==6
mons=[x for x,v in enumerate(a) if v];quads=[(1<<i)|(1<<j) for i in range(12) for j in range(i)]
rows={}
for j,Q in enumerate(quads):
 for M in mons:
  S=M|Q
  if S.bit_count()==8:rows[S]=rows.get(S,0)^(1<<j)
bas={}
for r in rows.values():
 while r:
  p=r.bit_length()-1
  if p not in bas:bas[p]=r;break
  r^=bas[p]
kernel=[]
for f in range(66):
 if f in bas:continue
 v=1<<f
 for p in sorted(bas):
  if (bas[p]&v).bit_count()%2:v^=1<<p
 assert all((r&v).bit_count()%2==0 for r in rows.values())
 kernel.append(v)
print('qkernel',len(kernel),flush=True)
X=[sum(1<<x for x in range(4096) if x>>i&1) for i in range(12)]
qb=[ALL]+X
for v in kernel:
 t=0
 for j,Q in enumerate(quads):
  if v>>j&1:
   i,k=[i for i in range(12) if Q>>i&1];t^=X[i]&X[k]
 qb.append(t)
# Store construction for reuse.
json.dump({'g':hex(g),'qwords':[hex(t) for t in qb],'masks':masks,'shifts':shifts},open('workspace/agent2_G160_shear_data.json','w'))
C=collections.Counter();seen=set();found=[];t0=time.time()
for mask,shift in zip(masks,shifts):
 P=spanmask(mask)
 for v in range(1,4096):
  if v&mask:continue
  H=[x^shift for x in P]+[x^v^shift for x in P];key=tuple(sorted(H))
  if key in seen:continue
  seen.add(key);support=[x for x in H if g>>x&1]
  if len(support)<57:continue
  ib={}
  for qi,q in enumerate(qb):
   z=sum(((q>>x)&1)<<j for j,x in enumerate(support));rel=1<<qi
   while z:
    p=z.bit_length()-1
    if p not in ib:ib[p]=(z,rel);break
    z^=ib[p][0];rel^=ib[p][1]
  C[(len(support),len(ib))]+=1
  if len(ib)>23:continue
  ib=list(ib.values());z=0;rel=0;pr=0
  for t in range(1<<len(ib)):
   gr=t^(t>>1)
   if t:
    i=(gr^pr).bit_length()-1;z^=ib[i][0];rel^=ib[i][1]
   pr=gr
   if z.bit_count() in [63,61,59,57]:
    hit={'weight':448-2*z.bit_count(),'H':H,'rel':rel,'I':z.bit_count()};found.append(hit);print('HIT',hit,flush=True);break
  if found:break
 if found:break
print('DONE',C,'hits',len(found),'seconds',time.time()-t0,flush=True)
json.dump(found,open('workspace/agent2_G160_shear_hits.json','w'))
Path('workspace/agent2_G160_shear_search.py').write_text(Path('scratchpad.py').read_text())
