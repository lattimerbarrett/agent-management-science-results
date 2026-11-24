import itertools,random,time,pickle
for c in [4,5,6,7]:
 n=2*c;r=c;vs=[]
 for sub in itertools.combinations(range(n),r):
  fixed=sum(1<<j for j in sub);free=((1<<n)-1)^fixed;v=0;t=free
  while True:
   v|=1<<(fixed|t)
   if t==0:break
   t=(t-1)&free
  vs.append(v)
 ws=set();t=time.time()
 for i in range(3000000):
  f=0
  for v in random.sample(vs,random.choice([4,5,6,7,8])):f^=v
  w=f.bit_count()
  if w<=3*2**c:ws.add(w)
 print(c,sorted(ws),time.time()-t,flush=True)
 pickle.dump(ws,open('random%d.pkl'%c,'wb'))
