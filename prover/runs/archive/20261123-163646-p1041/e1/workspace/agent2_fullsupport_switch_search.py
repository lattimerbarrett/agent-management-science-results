import sys,json,pickle,numpy as np,random,time,collections
from pathlib import Path
sys.path.insert(0,'workspace')
cols=pickle.load(open('workspace/a1_cols13_degree5.pkl','rb'))
random.seed(392);N=16384;known=collections.defaultdict(set)
def fp(f):
 a=1-2*np.unpackbits(np.frombuffer(f.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').astype(np.int32)
 for i in range(14):
  z=a.reshape(-1,2*(1<<i));t=z[:,:1<<i].copy();z[:,:1<<i]=t+z[:,1<<i:];z[:,1<<i:]=t-z[:,1<<i:]
 v,c=np.unique(np.abs(a),return_counts=True);return tuple(zip(map(int,v),map(int,c)))
seeds=json.load(open('workspace/agent4_flat_seeds.json'));bases=[]
for w,masks in seeds.items():
 f=0
 for mask in masks:
  for x in range(N):
   if x&~mask==0:f^=1<<x
 known[int(w)].add(fp(f))
 if int(w) in (314,318,338,342,346,350,354,358,366,370,374,378):bases.append((int(w),f))
for filename in ['workspace/agent2_cubicshear_novel_orbits.json','workspace/agent3_quartic_highqrank_verified.json','workspace/agent3_qrank_guided_novel_orbits.json']:
 for s in json.load(open(filename)):
  f=int(s['truth_hex'],16);known[s['weight']].add(fp(f))
  if filename.endswith('qrank_guided_novel_orbits.json'):bases.append((s['weight'],f))
emb=[]
for p in range(14):
 t=np.arange(8192,dtype=np.uint16);emb.append((t&((1<<p)-1))|((t>>p)<<(p+1)))
records=[];stats=collections.Counter();start=time.time()
for bi,(w,f) in enumerate(bases):
 fb=np.unpackbits(np.frombuffer(f.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little')
 for i in range(14):
  dx=fb[emb[i]]^fb[emb[i]^(1<<i)];SS=np.flatnonzero(dx).tolist();bas={};kern=[]
  for j,x in enumerate(SS):
   v=cols[x];rel=1<<j
   while v:
    p=v.bit_length()-1
    if p not in bas:bas[p]=(v,rel);break
    a,b=bas[p];v^=a;rel^=b
   if not v:kern.append(rel)
  stats[(w,len(kern))]+=1
  # Exact full-support switch basis embedded in both i-fibers.
  toggle=[(1<<int(emb[i][x]))|(1<<int(emb[i][x]^(1<<i))) for x in SS]
  K=[]
  for rel in kern:
   z=0
   while rel:
    b=rel&-rel;z^=toggle[b.bit_length()-1];rel^=b
   K.append(z)
  for trial in range(300):
   g=0
   for b in K:
    if random.getrandbits(1):g^=b
   cand=f^g;assert cand.bit_count()==w;sig=fp(cand)
   if sig not in known[w]:
    known[w].add(sig);records.append({'weight':w,'truth_hex':hex(cand),'source':bi,'coordinate':i,'kernel_dim':len(K)});print('NEWORBIT',w,'n',len(records),'Kdim',len(K),'seconds',time.time()-start,flush=True)
  if time.time()-start>110:break
 if time.time()-start>110:break
 print('progress',bi,w,'new',len(records),'sec',time.time()-start,flush=True)
print('DONE','stats',dict(stats),'new',len(records),'newweights',dict(collections.Counter(s['weight'] for s in records)),'seconds',time.time()-start,flush=True)
json.dump(records,open('workspace/agent2_fullsupport_switch_new_orbits.json','w'))
Path('workspace/agent2_fullsupport_switch_search.py').write_text(Path('scratchpad.py').read_text())
