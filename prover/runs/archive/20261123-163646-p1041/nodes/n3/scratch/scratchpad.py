import itertools,random,time,pickle
c=7;n=15;r=8;vs=[]
for sub in itertools.combinations(range(n),r):
 fixed=sum(1<<j for j in sub);free=((1<<n)-1)^fixed;v=0;t=free
 while True:
  v|=1<<(fixed|t)
  if not t:break
  t=(t-1)&free
 vs.append(v)
print('built',flush=True)
known={0,128,192,224,240,248,252,254,256,272,288,296,304,308,312,314,316,318,320}
t=time.time();ws=set()
for i in range(10000000):
 ids=random.sample(range(len(vs)),random.choice([4,5,6]));f=0
 for j in ids:f^=vs[j]
 w=f.bit_count()
 if w<=320:
  ws.add(w)
  if w not in known:
   print('NEW',w,[tuple(j+1 for j in sub) for sub in []],ids,flush=True);pickle.dump((ids,f),open('new%d.pkl'%w,'wb'));break
print(sorted(ws),time.time()-t)
