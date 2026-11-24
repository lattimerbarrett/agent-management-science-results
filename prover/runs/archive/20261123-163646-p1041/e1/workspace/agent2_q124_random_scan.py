import sys,itertools,time,json,random,collections
sys.path.insert(0,'workspace')
from a1_quadratic_image_api import image_on_D,small_coset_words
from pathlib import Path
random.seed(247124)
def span(bs):
 out=[0]
 for b in bs:out +=[x^b for x in out]
 return out
A=span([1<<i for i in range(6)]);B=span([1<<i for i in (0,6,7,8,9,10)]);q=set(A)^set(B)
hits=[];checked=0;skipped=0;stats=collections.Counter();t0=time.time()
for trial in range(2000):
 pb=[1<<i for i in range(6)]
 for _ in range(random.randrange(1,4)):pb[random.randrange(6)]^=random.randrange(4096)
 P=span(pb)
 if len(set(P))!=64:continue
 shift=0 if random.random()<.6 else random.randrange(4096)
 # Usually translate by a nearby A/B vector to preserve large intersections.
 if shift and random.random()<.7:shift=random.choice(A+B)
 p={x^shift for x in P};U=sorted(p|q)
 if len(U)>188:continue
 bas={}
 for b in pb:
  while b:
   lead=b.bit_length()-1
   if lead not in bas:bas[lead]=b;break
   b^=bas[lead]
 complement=[]
 for i in range(12):
  b=1<<i
  while b:
   lead=b.bit_length()-1
   if lead not in bas:bas[lead]=b;complement.append(1<<i);break
   b^=bas[lead]
 for di in range(64):
  if di<16:
   v=random.choice(span(complement)[1:]);db=pb+[v];ds=shift
  else:
   source=random.choice([pb,[1<<i for i in range(6)],[1<<i for i in (0,6,7,8,9,10)]])
   db=list(source)+[random.randrange(1,4096)];ds=random.choice([0,0,shift])
   for _ in range(random.randrange(1,3)):db[random.randrange(7)]^=random.randrange(4096)
  DD=span(db)
  if len(set(DD))!=128:continue
  D=[x^ds for x in DD];v=db[-1]
  outside=len(set(U)-set(D));desired={w:(w-128)//2-outside for w in [322,326,330,334]};good={w:e for w,e in desired.items() if 0<=e<=15}
  if not good:continue
  N=sum(1<<i for i,x in enumerate(D) if x in p and x in q)
  extras=image_on_D(U,D)
  if len(extras)>16:skipped+=1;continue
  found=[(e.bit_count(),e,g) for e,g in small_coset_words(N,extras)]
  checked+=1;stats[(len(extras),outside)]+=1
  for w,e in good.items():
   for ew,err,g in found:
    if ew==e:
     hit={'weight':w,'Pbasis':pb,'shift':shift,'Dbasis':db,'Dshift':ds,'error':hex(err),'image':hex(g)};hits.append(hit);print('HIT',hit,flush=True)
  if hits:break
 if trial%100==0:print('progress',trial,checked,'skip',skipped,'time',round(time.time()-t0,2),flush=True)
 if hits:break
print('DONE',checked,'skip',skipped,'hits',hits,'time',time.time()-t0,'stats',dict(stats),flush=True)
json.dump(hits,open('workspace/agent2_q124_random_hits.json','w'))
Path('workspace/agent2_q124_random_scan.py').write_text(Path('scratchpad.py').read_text())
