import itertools,functools,numpy as np,pickle,time,random
random.seed(1)
def coords(n):
 full=(1<<(1<<n))-1;co=[]
 for i in range(n):
  b=(1<<(1<<i))-1;z=0
  for j in range(1<<i,1<<n,2<<i):z|=b<<j
  co.append(z)
 return full,co
full,co=coords(8)
faces=[]
for ss in itertools.combinations(range(8),4):
 mask=sum(1<<i for i in ss)
 for val in range(16):
  v=full;pat=sum((val>>j&1)<<i for j,i in enumerate(ss))
  for i in ss:v &= co[i] if pat>>i&1 else full^co[i]
  faces.append((v,(mask,pat)))
A=faces[0][0];Acert=faces[0][1];patterns={};t=time.time()
for B,Bc in faces:
 ab=(A&B).bit_count()
 for C,Cc in faces:
  ac=(A&C).bit_count();bc=(B&C).bit_count();abc=(A&B&C).bit_count()
  n=(16-ab-ac+abc,16-ab-bc+abc,ab-abc,16-ac-bc+abc,ac-abc,bc-abc,abc)
  patterns.setdefault(n,(Acert,Bc,Cc))
print('Apatterns',len(patterns),'secs',time.time()-t,flush=True)
# load all homogeneous cubic vectors on 6 vars with low wt
full,co=coords(6)
G=[functools.reduce(int.__and__,(co[i] for i in ss),full) for ss in itertools.combinations(range(6),3)]
words=[];v=0
for s in range(1<<20):
 if s:v^=G[(s&-s).bit_length()-1]
 if 0<v.bit_count()<=20:words.append(v)
print('poolB',len(words),flush=True)
P=np.array(list(patterns),dtype=np.int32);pc=list(patterns);found={};t=time.time()
missing={322,326,330,334}
for batch in range(1000):
 btrips=[random.sample(words,3) for _ in range(10000)]
 W=np.array([[( (x if k&1 else 0)^(y if k&2 else 0)^(z if k&4 else 0)).bit_count() for k in range(1,8)] for x,y,z in btrips],dtype=np.int32).T
 out=P@W
 for target in list(missing):
  ii,jj=np.where(out==target)
  if len(ii):
   i=int(ii[0]);j=int(jj[0]);found[target]=(patterns[pc[i]],btrips[j]);missing.remove(target)
   print('FOUND',target,found[target],flush=True)
 if not missing:break
 if batch%100==0:print(batch,'missing',missing,'secs',time.time()-t,flush=True)
with open('rank3evenTensor.pkl','wb') as f:pickle.dump(found,f)
print('done',missing)
