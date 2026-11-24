import sys,json,random,numpy as np,time,collections
from pathlib import Path
sys.path.insert(0,'workspace')
from a1_cubic_closure_api import closure_kernel,cols
random.seed(385)
seed=int(json.load(open('workspace/agent3_h316_h320_m13.json'))['320']['truth_hex'],16);assert seed.bit_count()==320
h=seed;S=[x for x in range(8192) if h>>x&1];pool=[seed];seen=set();stats=collections.Counter();hit=None;start=time.time();records=[]
def periods(h):
 B=np.unpackbits(np.frombuffer(h.to_bytes(1024,'little'),dtype=np.uint8),bitorder='little');P=np.flatnonzero(B).astype(np.uint16);C=np.bincount(np.bitwise_xor(P[:,None],P[None,:]).ravel(),minlength=8192);C[0]=0
 return list(np.where(C==320)[0])
for trial in range(1000000):
 if trial%1000==0:
  h=random.choice(pool);S=[x for x in range(8192) if h>>x&1]
 sample=random.sample(S,9);offset=sample[0];bas={};directions=[]
 for x in sample[1:]:
  x^=offset
  while x:
   p=x.bit_length()-1
   if p not in bas:bas[p]=x;directions.append(x);break
   x^=bas[p]
 if len(directions)!=8:continue
 H=[offset]
 for d in directions:H +=[x^d for x in H]
 mask=sum(1<<x for x in H);I=(h&mask).bit_count();stats[I]+=1
 if I!=128:continue
 cand=h^mask
 if cand in seen:continue
 seen.add(cand);per=periods(cand)
 if per:continue
 ss=[x for x in range(8192) if cand>>x&1];E,K,b5=closure_kernel(ss);stats[('aper',len(E),len(K),any(k.bit_count()%2 for k in K))]+=1
 records.append({'truth_hex':hex(cand),'weight':320,'period_dim':0,'E':E,'K':K})
 if len(pool)<100:pool.append(cand)
 if any(k.bit_count()%2 for k in K):
  assert len(K)<=25;z=0;T=None
  for j in range(1<<len(K)):
   if j:z^=K[(j&-j).bit_length()-1]
   if z.bit_count() in (1,3,5,7):T=[E[i] for i in range(len(E)) if z>>i&1];break
  if T:
   moment=0
   for x in T:moment^=cols[x]
   c=0
   while moment:
    p=moment.bit_length()-1;v,im=b5[p];moment^=v;c^=im
   g=sum(1<<x for j,x in enumerate(ss) if c>>j&1)|sum(1<<x for x in T);F=g|((g^cand)<<8192);w=F.bit_count();assert w==320+2*len(T)
   ar=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
   for bit in range(14):a=ar.reshape(-1,2*(1<<bit));a[:,1<<bit:]^=a[:,:1<<bit]
   deg=max(int(x).bit_count() for x in np.flatnonzero(ar));assert deg<=7
   hit={'weight':w,'truth_hex':hex(F),'degree':deg};print('HIT',hit,flush=True);break
 if trial%10000==0:print('progress',trial,'switches',len(seen),'aper',len(records),'pool',len(pool),'seconds',time.time()-start,flush=True)
 if time.time()-start>115:break
print('DONE',trial,'switches',len(seen),'aperiodic',len(records),'tracehist',{str(k):v for k,v in stats.items() if not isinstance(k,int)},'maxI',max(k for k in stats if isinstance(k,int)),'hit',bool(hit),'sec',time.time()-start,flush=True)
json.dump(hit,open('workspace/agent2_boundary_switch_hit.json','w'));json.dump(records,open('workspace/agent2_boundary_switch_states.json','w'))
Path('workspace/agent2_boundary_switch_search.py').write_text(Path('scratchpad.py').read_text())
