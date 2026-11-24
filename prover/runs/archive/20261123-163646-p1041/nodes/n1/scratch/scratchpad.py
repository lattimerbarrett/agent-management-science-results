import itertools,random,time,pickle
c=7
for n in [14,15,16]:
 r=n-c;vs=[]
 for sub in itertools.combinations(range(n),c):
  free=sum(1<<j for j in sub);fixed=((1<<n)-1)^free;v=0;t=free
  while True:
   v|=1<<(fixed|t)
   if t==0:break
   t=(t-1)&free
  vs.append(v)
 ws=set();ex={};t=time.time()
 for i in range(5000000):
  f=0;inds=random.sample(range(len(vs)),random.choice([4,5,6]))
  for j in inds:f^=vs[j]
  w=f.bit_count()
  if w<=384:ws.add(w);ex[w]=inds
 print(n,sorted(ws),time.time()-t,flush=True)
 pickle.dump((ws,ex),open('randomn%d.pkl'%n,'wb'))
