import itertools,json,random,time,numpy as np,shutil
rng=random.Random(315);n=14;N=1<<n;ALL=(1<<N)-1;D7=sum(1<<x for x in range(N) if x.bit_count()<=7)
X=[sum(1<<x for x in range(N) if x>>i&1) for i in range(n)];LOW=[ALL^x for x in X]
def mob(a):
 for i in range(n):a^=(a&LOW[i])<<(1<<i)
 return a
def times(a,i):return (a&X[i])^((a&LOW[i])<<(1<<i))
def flat(mask):
 ps=[0]
 for i in range(14):
  if mask>>i&1:ps +=[x^(1<<i) for x in ps]
 return ps
records=[(int(w),ms,None) for w,ms in json.load(open('workspace/agent4_flat_seeds.json')).items()]
records.append((362,[3373,13010,13665,9585,7213],(1,2,4)))
records.extend((int(w),r['masks'],None) for w,r in json.load(open('workspace/a1_highresidue_seeds.json')).items())
pool=[]
for w,ms,shear in records:
 f=0
 for j,mask in enumerate(ms):
  for x in flat(mask):
   if shear and j==shear[0]:x^=((x>>shear[2])&1)<<shear[1]
   f^=1<<x
 assert f.bit_count()==w;pool.append((mob(f),w))
for fn in ['workspace/agent2_cubicshear_states.json','workspace/agent3_nonlinear_beam_states.json']:
 if __import__('os').path.exists(fn):
  for r in json.load(open(fn))[:200]:pool.append((int(r.get('anf_hex','0'),16) or mob(int(r['truth_hex'],16)),r['weight']))
combos={i:list(itertools.combinations([j for j in range(n) if j!=i],4)) for i in range(n)}
start=time.time();hits={};genuine=0;kept=0;seen=set();states=[];hist={};gcount={}
shutil.copyfile(__file__,'workspace/agent3_higher_shear_search.py')
for orbit in range(1000):
 a,w=rng.choice(pool)
 for _ in range(70):
  i,j=rng.sample(range(n),2);a^=times((a&X[i])>>(1<<i),j)
 for i in range(n):
  if rng.getrandbits(1):a^=(a&X[i])>>(1<<i)
 for i in range(n):
  der=(a&X[i])>>(1<<i);cache={}
  for I in combos[i]:
   if I[:2] not in cache:cache[I[:2]]=times(times(der,I[0]),I[1])
   diff=times(times(cache[I[:2]],I[2]),I[3])
   if not diff&~D7:continue
   genuine+=1;tr=diff&D7
   if not tr:continue
   cand=a^tr;f=mob(cand);wt=f.bit_count();hist[wt]=hist.get(wt,0)+1
   if wt in (322,326,330,334):
    assert cand==mob(f) and not cand&~D7
    arr=np.unpackbits(np.frombuffer(f.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
    for b in range(14):
     st=1<<b;bl=arr.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
    anf=list(map(int,np.flatnonzero(arr)));assert max(map(int.bit_count,anf))<=7
    hits[wt]={'weight':wt,'truth_hex':hex(f),'anf':anf,'shear':[i,*I]};print('VERIFIED HIT',wt,flush=True);json.dump(hits,open('workspace/agent3_higher_shear_hits.json','w'))
   if 312<=wt<=462 and wt%2==0 and cand not in seen:
    seen.add(cand);kept+=1
    if len(pool)<2000 or rng.randrange(1000)==0:
     if len(pool)>=2000:pool.pop(rng.randrange(len(pool)))
     pool.append((cand,wt));states.append({'weight':wt,'truth_hex':hex(f),'anf_hex':hex(cand)})
  if len(hits)==4:break
 if orbit%20==0:
  print('orbit',orbit,'genuine',genuine,'newlow',kept,'pool',len(pool),'min',min(hist),'secs',round(time.time()-start,1),flush=True)
  json.dump(states,open('workspace/agent3_higher_shear_states.json','w'));json.dump(hist,open('workspace/agent3_higher_shear_weight_hist.json','w'))
 if len(hits)==4 or time.time()-start>280:break
print('DONE',orbit,'genuine',genuine,'hits',list(hits),'seconds',time.time()-start,flush=True)
json.dump(states,open('workspace/agent3_higher_shear_states.json','w'));json.dump(hist,open('workspace/agent3_higher_shear_weight_hist.json','w'))
