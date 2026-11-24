import itertools,random,collections,json,time
from pathlib import Path
random.seed(353)
def span(bs,sh=0):
 out=[sh]
 for b in bs:out +=[x^b for x in out]
 return set(out)
mons=[sum(1<<i for i in I) for k in range(4) for I in itertools.combinations(range(8),k)];cols=[sum((x&m==m)<<j for j,m in enumerate(mons)) for x in range(256)]
f24={x for x in range(64) if ((x&1)*((x>>1)&1))^(((x>>2)&1)*((x>>3)&1))}
assert len(f24)==24
stats=collections.Counter();hits=[];start=time.time()
def shortened(U):
 US=sorted(U);bas={};kern=[]
 for j,x in enumerate(US):
  v=cols[x];im=1<<j
  while v:
   p=v.bit_length()-1
   if p not in bas:bas[p]=(v,im);break
   w,z=bas[p];v^=w;im^=z
  if not v:kern.append(sum(1<<xx for jj,xx in enumerate(US) if im>>jj&1))
 return bas,kern
for trial in range(10000):
 bs=[random.randrange(1,64),random.randrange(1,64),64^random.randrange(64),128^random.randrange(64)];A=span(bs,random.randrange(64))
 if len(A)!=16:continue
 I=len(A&f24)
 if I%2==0:continue
 U=A|f24;bas,K=shortened(U);stats[(len(U),len(K))]+=1
 if len(K)>=4:
  hit={'U':sorted(U),'basis':[hex(v) for v in K],'kind':'min16second24','A':sorted(A)};hits.append(hit);print('HIT',len(U),len(K),flush=True);break
 # degree3 closure extra points add one new dimension.
 for x in range(256):
  if x in U:continue
  v=cols[x]
  while v:
   p=v.bit_length()-1
   if p not in bas:break
   v^=bas[p][0]
  if v==0:
   UU=U|{x};bb,KK=shortened(UU);stats[('extra',len(KK))]+=1
   if len(KK)>=4:
    hit={'U':sorted(UU),'basis':[hex(v) for v in KK],'kind':'plusclosure','A':sorted(A)};hits.append(hit);print('HITEXTRA',len(UU),len(KK),flush=True);break
 if hits:break
print('DONE',dict(stats),'hits',len(hits),'seconds',time.time()-start,flush=True)
json.dump(hits,open('workspace/agent2_tensor_oldD_hits.json','w'))
Path('workspace/agent2_tensor_oldD_search.py').write_text(Path('scratchpad.py').read_text())
