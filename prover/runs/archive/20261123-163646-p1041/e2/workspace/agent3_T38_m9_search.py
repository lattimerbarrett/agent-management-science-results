import numpy as np,random,time,math,json,pathlib,sys
sys.path.insert(0,'workspace')
from agent3_graph_lifts import veronese
rng=random.Random(7431);d=9;N=1<<d;Kdim=4;size=16;sel=[np.flatnonzero((np.arange(size)>>j)&1) for j in range(Kdim)]
vs=veronese(d,2)
def span(b):
 out=[0]
 for x in b:out += [v^x for v in out]
 return np.array(out,dtype=np.int32)
def nulldim(S):
 b={}
 for p in S:
  x=vs[p]
  while x:
   j=x.bit_length()-1
   if j not in b:b[j]=x;break
   x^=b[j]
 return len(S)-len(b)
start=time.time();trials=0;seen=set();stats={};interesting=[]
for restart in range(10000):
 count=[4,5,6,8,10,12,16,20][restart%8]
 bs=[[1<<i for i in range(4)] for j in range(count)];offs=[0]*count;pts=[span(b) for b in bs]
 f=np.zeros(N,dtype=np.uint8)
 for p in pts:f[p]^=1
 w=int(f.sum());score=abs(w-38)
 for step in range(25000):
  trials+=1;j=rng.randrange(count);old=pts[j];basis=bs[j]
  if rng.random()<.9:
   q=rng.randrange(4);delta=1<<rng.randrange(d)
   if rng.random()<.2:delta^=1<<rng.randrange(d)
   if delta in (old^offs[j]):continue
   inds=sel[q];newhalf=old[inds]^delta;toggle=np.concatenate((old[inds],newhalf));newp=old.copy();newp[inds]=newhalf;newb=basis.copy();newb[q]^=delta;newo=offs[j]
  else:
   delta=1<<rng.randrange(d)
   if delta in (old^offs[j]):continue
   newp=old^delta;toggle=np.concatenate((old,newp));newb=basis;newo=offs[j]^delta
  nw=w+len(toggle)-2*int(f[toggle].sum());ns=abs(nw-38)
  phase=step%5000;temp=1.1 if phase<4000 else 5.
  if ns<=score or rng.random()<math.exp((score-ns)/temp):
   f[toggle]^=1;pts[j]=newp;bs[j]=newb;offs[j]=newo;w=nw;score=ns
   if w==38:
    key=np.packbits(f).tobytes()
    if key not in seen:
     seen.add(key);S=np.flatnonzero(f).tolist();nd=nulldim(S);stats[nd]=stats.get(nd,0)+1
     if nd>=13:
      interesting.append({'support':S,'kernel_dim':nd,'basis':bs.copy(),'offsets':offs.copy()});print('INTERESTING',nd,'at',trials,flush=True)
      if len(interesting)>=20:break
  if time.time()-start>110:break
 if len(interesting)>=20 or time.time()-start>110:break
print('trials',trials,'time',time.time()-start,'unique38',len(seen),'Kstats',stats,'interesting',len(interesting))
pathlib.Path('workspace/agent3_T38_m9_seeds.json').write_text(json.dumps({'trials':trials,'unique':len(seen),'stats':stats,'seeds':interesting}))
pathlib.Path('workspace/agent3_T38_m9_search.py').write_text(pathlib.Path(__file__).read_text())
