import itertools,random,time,pickle
c=7;n=14;vs=[]
for sub in itertools.combinations(range(n),c):
 fixed=sum(1<<j for j in sub);free=((1<<n)-1)^fixed;v=0;t=free
 while True:
  v|=1<<(fixed|t)
  if not t:break
  t=(t-1)&free
 vs.append(v)
while True:
 f=0
 for v in random.sample(vs,5):f^=v
 if f.bit_count()==338:break
seen=set();t=time.time();prev=-1
for step in range(30000):
 opts=[]
 for j,v in enumerate(vs):
  if j==prev:continue
  w=(f^v).bit_count()
  if 256<=w<=384:opts.append((j,w))
 if not opts:
  prev=-1
  continue
 # bias to a broad low-weight distribution
 j,w=random.choices(opts,[2 if w%4==2 else 1 for j,w in opts])[0]
 f^=vs[j];prev=j
 if w not in seen:
  seen.add(w);print(step,sorted(seen),flush=True)
 if w in [322,326,330,334]:
  print('FOUND',w,flush=True);pickle.dump(f,open('found%d.pkl'%w,'wb'))
 if step%1000==0:print('time',step,time.time()-t,flush=True)
