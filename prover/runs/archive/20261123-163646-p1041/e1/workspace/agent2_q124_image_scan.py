import sys,itertools,time,json,random
sys.path.insert(0,'workspace')
from a1_quadratic_image_api import image_on_D,small_coset_words
from pathlib import Path
def span(bs):
 out=[0]
 for b in bs:out +=[x^b for x in out]
 return out
A=span([1<<i for i in range(6)]);B=span([1<<i for i in (0,6,7,8,9,10)]);q=set(A)^set(B)
assert len(q)==124
pb=[1<<i for i in range(5)]+[(1<<5)^(1<<6)]
P=span(pb);p=set(P);U=sorted(p|q)
print('q,pq,U',len(q),len(p&q),len(U),flush=True)
seen=set();checked=0;hits=[];t0=time.time()
for v in range(1,4096):
 if v in p:continue
 D=span(pb+[v]);key=tuple(sorted(D))
 if key in seen:continue
 seen.add(key)
 outside=len(set(U)-set(D));desired={w:(w-128)//2-outside for w in [322,326,330,334]};good={w:e for w,e in desired.items() if 0<=e<=15}
 if not good:continue
 N=sum(1<<i for i,x in enumerate(D) if x in p and x in q)
 extras=image_on_D(U,D);found=[(e.bit_count(),e,g) for e,g in small_coset_words(N,extras)]
 checked+=1
 print(checked,'v',v,'out',outside,'extra',len(extras),'low',[w for w,_,_ in found],flush=True)
 for w,e in good.items():
  for ew,err,g in found:
   if ew==e:hits.append({'weight':w,'Pbasis':pb,'Dextra':v,'error':hex(err),'image':hex(g)})
print('DONE',checked,'hits',hits,'time',time.time()-t0,flush=True)
json.dump(hits,open('workspace/agent2_q124_image_hits.json','w'))
Path('workspace/agent2_q124_image_scan.py').write_text(Path('scratchpad.py').read_text())
