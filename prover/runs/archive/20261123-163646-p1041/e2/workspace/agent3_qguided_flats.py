import numpy as np,random,time,math,json,pathlib,sys
sys.path.insert(0,'workspace')
from agent1_checked_grid import degree
rng=random.Random(11829);N=1<<15;es=1<<np.arange(15,dtype=np.int32);xall=np.arange(N,dtype=np.int32)
sel=[np.flatnonzero((np.arange(128)>>j)&1) for j in range(7)]
missing=[258,260,262,264,266,268,270,274,276,278,280,282,284,286,290,292,294,298,300,302,306,310,322,326,330,334]
targets=[322,326,330,334]
def span(b):
 out=[0]
 for x in b:out += [v^x for v in out]
 return np.array(out,dtype=np.int32)
def Kpar(f):return np.array([int(f[(xall&e)==0]@f[xall[(xall&e)==0]^e])%2 for e in es],dtype=np.uint8)
def badfun(w,k):
 q=(w//2)&1
 return int(np.count_nonzero(k^q))+(1-q)
start=time.time();trials=0;bestfq=10000;hist={};hit=None;minbad=20
for restart in range(1000):
 count=[5,6,7,8,10,12][restart%6]
 bs=[[1<<i for i in range(7)], [1<<i for i in range(8,15)], [1<<7]+[1<<i for i in range(9,15)],[(1<<7)^(1<<8)]+[1<<i for i in range(9,15)]]
 for j in range(count-4):
  b=[1,1<<7]
  while len(b)<7:
   v=rng.randrange(1,N)
   if v not in span(b):b.append(v)
  bs.append(b)
 offs=[0]*count;pts=[span(b) for b in bs]
 f=np.zeros(N,dtype=np.uint8)
 for p in pts:f[p]^=1
 w=int(f.sum());k=Kpar(f);target=targets[restart%4];bad=badfun(w,k);score=abs(w-target)+12*bad
 for step in range(30000):
  trials+=1;j=rng.randrange(count);old=pts[j];basis=bs[j]
  if rng.random()<0.97:
   q=rng.randrange(7);delta=1<<rng.randrange(15)
   if rng.random()<0.15:delta^=1<<rng.randrange(15)
   if delta in (old^offs[j]):continue
   inds=sel[q];newhalf=old[inds]^delta;toggle=np.concatenate((old[inds],newhalf))
   newp=old.copy();newp[inds]=newhalf;newb=basis.copy();newb[q]^=delta;newo=offs[j]
  else:
   delta=1<<rng.randrange(15)
   if delta in (old^offs[j]):continue
   newp=old^delta;toggle=np.concatenate((old,newp));newb=basis;newo=offs[j]^delta
  nw=w+len(toggle)-2*int(f[toggle].sum())
  dk=(f[toggle[:,None]^es].sum(axis=0)&1).astype(np.uint8);nk=k^dk
  nb=badfun(nw,nk);ns=abs(nw-target)+12*nb
  # periodically permit leaving a low-weight/full-Q basin
  phase=step%6000;temp=4 if phase<3500 else (14 if phase<5000 else 28)
  if ns<=score or rng.random()<math.exp((score-ns)/temp):
   f[toggle]^=1;pts[j]=newp;bs[j]=newb;offs[j]=newo;w=nw;k=nk;bad=nb;score=ns
   if bad==0:
    hist[w]=hist.get(w,0)+1;bestfq=min(bestfq,w)
   if w in missing:
    assert w==int(f.sum());assert np.array_equal(k,Kpar(f));assert degree(f)<=8
    hit={'weight':w,'support':np.flatnonzero(f).tolist(),'basis':bs,'offsets':offs,'K':k.tolist(),'bad':bad}
    print('FOUND',w,'bad',bad,'trial',trials,flush=True);break
  if trials%100000==0:
   assert w==int(f.sum()) and np.array_equal(k,Kpar(f))
  if time.time()-start>165:break
 if hit or time.time()-start>165:break
print('elapsed',time.time()-start,'trials',trials,'bestfullq',bestfq,'smallhist',{w:n for w,n in hist.items() if w<400},'hit',bool(hit))
pathlib.Path('workspace/agent3_qguided_flats.json').write_text(json.dumps({'trials':trials,'bestfullq':bestfq,'hist':hist,'hit':hit}))
pathlib.Path('workspace/agent3_qguided_flats.py').write_text(pathlib.Path(__file__).read_text())
