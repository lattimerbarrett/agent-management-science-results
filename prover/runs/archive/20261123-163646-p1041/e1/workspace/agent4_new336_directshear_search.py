import time,itertools,random,pickle,collections,json,numpy as np
start=time.time();random.seed(444404);n=14;N=1<<n;ALL=(1<<N)-1
X=[sum(1<<j for j in range(N) if j>>i&1) for i in range(n)];LOW=sum(1<<j for j in range(N) if j.bit_count()<=7)
def mob(f):
 for i in range(n):f^=(f&(ALL^X[i]))<<(1<<i)
 return f
def mul(f,i):return (f&X[i])^((f&(ALL^X[i]))<<(1<<i))
def signature(f):
 a=1-2*np.unpackbits(np.frombuffer(f.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').astype(np.int32)
 for h in [1<<i for i in range(14)]:
  b=a.reshape(-1,2*h);u=b[:,:h].copy();v=b[:,h:].copy();b[:,:h]=u+v;b[:,h:]=u-v
 return tuple(zip(*np.unique(np.abs(a),return_counts=True)))
D=json.load(open('workspace/a1_fiber3cycle_new_orbits.json'));pool={};seen=set();sigs=set()
for rec in D:
 f=int(rec['truth_hex'],16);a=mob(f);w=f.bit_count();assert w==rec['weight'] and a&~LOW==0
 pool.setdefault(w,[]).append(a);seen.add(a);sigs.add(signature(f))
print('START',[(w,len(v)) for w,v in pool.items()],flush=True)
found={};tested=0;wtstats=collections.Counter()
for orbit in range(2000):
 ws=list(pool);bw=random.choices(ws,weights=[2**((400-w)/20) for w in ws])[0];a=random.choice(pool[bw])
 for _ in range(random.randrange(18)):
  i,j=random.sample(range(n),2);di=(a&X[i])>>(1<<i);a^=di if random.random()<.1 else mul(di,j)
 for i in range(n):
  di=(a&X[i])>>(1<<i);others=[j for j in range(n) if j!=i]
  for r in [2,3]:
   for S in itertools.combinations(others,r):
    v=di
    for j in S:v=mul(v,j)
    b=a^v
    if b&~LOW==0:continue
    b&=LOW;f=mob(b);w=f.bit_count();tested+=1
    if w<=400:wtstats[w]+=1
    if w in [322,326,330,334] and w not in found:
     assert mob(f)==b and b&~LOW==0
     found[w]={'truth_hex':hex(f),'anf_hex':hex(b)};pickle.dump(found,open('workspace/agent4_new336_directshear_hits.pkl','wb'));print('HIT',w,'orbit',orbit,'tested',tested,'sec',time.time()-start,flush=True)
    if 300<=w<=400 and b not in seen and random.random()<(.01 if w<=350 else .001):
     seen.add(b);sig=signature(f)
     if sig not in sigs:
      sigs.add(sig);pool.setdefault(w,[]).append(b)
 if orbit%100==0:print('orbit',orbit,'tested',tested,'found',found.keys(),'pool',[(w,len(v)) for w,v in sorted(pool.items())],'sec',time.time()-start,flush=True)
 if len(found)==4:break
pickle.dump(pool,open('workspace/agent4_new336_directshear_pool.pkl','wb'))
print('DONE',tested,found.keys(),wtstats,time.time()-start)
open('workspace/agent4_new336_directshear_search.py','w').write(open(__file__).read())
