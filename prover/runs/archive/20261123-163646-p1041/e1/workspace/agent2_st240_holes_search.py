import sys,random,time,json,itertools,collections
from pathlib import Path
sys.path.insert(0,'workspace')
from agent2_st240_api import H,HS,qb,qp,decode,cols,span,insert
random.seed(300);J=list(range(8));JS=set(J);HJ=HS|JS;hlen=len(H);base=[1<<i for i in range(7)];baseB=[1<<i for i in [0,1,2,7,8,9,10]]
def joint_image(U):
 bas={};eb={};extras=[]
 for x in U-HJ:
  v=cols[x]
  while v:
   p=v.bit_length()-1
   if p not in bas:bas[p]=(v,0);break
   v^=bas[p][0]
 for j,x in enumerate(H+J):
  v=cols[x];im=1<<j
  while v:
   p=v.bit_length()-1
   if p not in bas:bas[p]=(v,im);break
   a,b=bas[p];v^=a;im^=b
  if v:continue
  for p in qp:
   if im>>p&1:im^=qb[p]
  if insert(eb,im):extras.append(im)
 return extras
def randsub(vs,dim):
 while True:
  ps=span([random.choice(vs) for _ in range(dim)])
  if len(ps)==1<<dim:return [x for x in ps] # Not basis; unused
hits=[];skipped=0;checked=0;t0=time.time();cnt=collections.Counter();HM=(1<<hlen)-1
for trial in range(1000):
 # Random 6-flat contained in axis A (random hyperplane).
 while True:
  pb=[random.randrange(1,128) for _ in range(6)]
  p=span(pb,random.randrange(128))
  if len(p)==64:break
 source=random.choice([base,baseB]);sourcepts=list(span(source))
 qb5=[random.choice(sourcepts) for _ in range(5)]
 qbs=qb5+[(1<<11)^random.randrange(1<<11)];q=span(qbs,random.choice(sourcepts))
 if len(q)!=64:continue
 U=p|q;outU=len(U-HS)
 N=sum(1<<i for i,x in enumerate(H) if x in p and x in q)
 extra=joint_image(U);cnt[len(extra)]+=1
 if len(extra)>17:skipped+=1;continue
 im=0;prev=0
 for s in range(1<<len(extra)):
  gr=s^(s>>1)
  if s:im^=extra[(gr^prev).bit_length()-1]
  prev=gr;outside=im>>hlen;outsidewt=sum((outside>>j)&1 for j,x in enumerate(J) if x not in U)
  # J points already in U cost no outside penalty.
  target_errors={w:(w-240)//2-outU-2*outsidewt for w in [322,326,330,334]}
  if not any(0<=e<=15 for e in target_errors.values()):continue
  err=decode((im&HM)^N)
  if err is None:continue
  for w,e in target_errors.items():
   if err.bit_count()==e:
    hit={'weight':w,'pb':pb,'p':list(p),'qbs':qbs,'q':list(q),'joint':hex(im),'error':hex(err),'outU':outU,'outsidewt':outsidewt};hits.append(hit);print('HIT',hit,flush=True);break
  if hits:break
 checked+=1
 if hits:break
 if trial%100==0:print('progress',trial,checked,'skip',skipped,'dims',dict(cnt),'sec',time.time()-t0,flush=True)
 if time.time()-t0>115:break
print('DONE',checked,'skip',skipped,'dims',dict(cnt),'hits',len(hits),'seconds',time.time()-t0,flush=True)
json.dump(hits,open('workspace/agent2_st240_holes_hits.json','w'))
Path('workspace/agent2_st240_holes_search.py').write_text(Path('scratchpad.py').read_text())
