import numpy as np,random,time,math,json,pathlib,sys
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese
rng=random.Random(499156);d=12;N=1<<d;fd=6;size=64;sel=[np.flatnonzero((np.arange(size)>>j)&1) for j in range(fd)];vs=veronese(d,4)
def span(b):
 out=[0]
 for x in b:out += [v^x for v in out]
 return np.array(out,dtype=np.int32)
def nulldim(S):
 b={}
 for p in S:
  x=vs[int(p)]
  while x:
   j=x.bit_length()-1
   if j not in b:b[j]=x;break
   x^=b[j]
 return len(S)-len(b)
st=time.time();trials=0;cache={};stats={};interesting=[];best=0
for restart in range(10000):
 count=[5,6,8,10,12,15,18,20][restart%8];bs=[[1<<i for i in range(fd)] for j in range(count)];offs=[0]*count;pts=[span(b) for b in bs];f=np.zeros(N,dtype=np.uint8)
 for p in pts:f[p]^=1
 w=int(f.sum());score=abs(w-156)
 for step in range(25000):
  trials+=1;j=rng.randrange(count);old=pts[j];basis=bs[j]
  if rng.random()<.92:
   q=rng.randrange(fd);delta=1<<rng.randrange(d)
   if rng.random()<.2:delta^=1<<rng.randrange(d)
   if delta in (old^offs[j]):continue
   inds=sel[q];newhalf=old[inds]^delta;toggle=np.concatenate((old[inds],newhalf));newp=old.copy();newp[inds]=newhalf;newb=basis.copy();newb[q]^=delta;newo=offs[j]
  else:
   delta=1<<rng.randrange(d)
   if delta in (old^offs[j]):continue
   newp=old^delta;toggle=np.concatenate((old,newp));newb=basis;newo=offs[j]^delta
  nw=w+len(toggle)-2*int(f[toggle].sum());ns=abs(nw-156);nd=None
  if nw==156:
   f[toggle]^=1;key=np.packbits(f).tobytes();nd=cache.get(key)
   if nd is None:
    S=np.flatnonzero(f);nd=nulldim(S);cache[key]=nd;stats[nd]=stats.get(nd,0)+1
    if nd>best:best=nd;print('NEWBEST',best,'trials',trials,'stats',stats,'sec',time.time()-st,flush=True)
    if nd>=15:
     interesting.append({'support':S.tolist(),'Kdim':nd,'basis':bs,'offsets':offs});print('FOUND',nd,flush=True)
   f[toggle]^=1;ns=2*max(0,14-nd)
  temp=1.2 if step%5000<4000 else 5.
  if ns<=score or rng.random()<math.exp((score-ns)/temp):
   f[toggle]^=1;pts[j]=newp;bs[j]=newb;offs[j]=newo;w=nw;score=ns
  if interesting or time.time()-st>110:break
 if interesting or time.time()-st>110:break
R={'trials':trials,'seconds':time.time()-st,'unique156':len(cache),'Kstats':stats,'found':interesting};print('DONE',R if not interesting else {k:v for k,v in R.items() if k!='found'},flush=True)
pathlib.Path('workspace/agent4_h156_K15_search.json').write_text(json.dumps(R))
