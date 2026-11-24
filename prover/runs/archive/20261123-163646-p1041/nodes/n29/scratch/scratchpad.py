import random,time,math,json,itertools,numpy as np
n=14;NN=1<<n;ALL=(1<<NN)-1
masks=[]
for i in range(n):
 block=(1<<(1<<i))-1;v=0
 for j in range(1<<i,NN,1<<(i+1)):v|=block<<j
 masks.append(v)
# Four heavily overlapping coordinate 7-flats forming an aperiodic weight308 seed.
ns=[1,0,0,3,0,0,0,2,0,0,1,1,4,1,0,0];fm=[0]*4;j=0
for mask,num in enumerate(ns):
 for _ in range(num):
  for i in range(4):
   if mask>>i&1:fm[i]|=1<<j
  j+=1
seed=[]
for free in fm:
 v=0;x=free
 while True:
  v|=1<<x
  if x==0:break
  x=(x-1)&free
 seed.append(v)
minimum=(1<<128)-1
found={};targets=[310,322,326,330,334];start=time.time();best={t:999 for t in targets}
for trial in range(1000):
 target=310;terms=seed[:];f=0
 for w in terms:f^=w
 for k in range(random.choice([1,2,3])):terms.extend([minimum,minimum])
 for step in range(6000):
  j=random.randrange(len(terms));old=terms[j];a,b=random.sample(range(n),2)
  ctrl=masks[a] if random.randrange(2) else ALL^masks[a]
  moving=old&ctrl;stay=old^moving
  # reversible controlled bit flip of coordinate b
  sh=1<<b;new=stay|((moving & masks[b])>>sh)|((moving & (ALL^masks[b]))<<sh)
  diff=old^new
  if not diff:continue
  ff=f^diff;w=ff.bit_count()
  if w in targets and w not in found:
   witness=terms[:];witness[j]=new
   arr=np.fromiter(((ff>>i)&1 for i in range(NN)),dtype=np.uint8,count=NN)
   anf=arr.copy()
   for z in range(n):
    z1=anf.reshape(-1,1<<(z+1));z1[:,1<<z:]^=z1[:,:1<<z]
   deg=max(i.bit_count() for i in np.flatnonzero(anf))
   assert deg<=7 and int(arr.sum())==w and all(t.bit_count()==128 for t in witness)
   found[w]={'weight':w,'degree':deg,'support':np.flatnonzero(arr).tolist(),'flats':[[i for i in range(NN) if t>>i&1] for t in witness]}
   json.dump(found,open('affine_flat_target_witnesses.json','w'))
   print('FOUND AND VERIFIED',w,'degree',deg,'terms',len(terms),'elapsed',time.time()-start,flush=True)
  e=abs(f.bit_count()-target);ee=abs(w-target)
  temp=[24,16,8,3][(step//1500)%4]
  if ee<=e or random.random()<math.exp((e-ee)/temp):terms[j]=new;f=ff
  best[target]=min(best[target],ee)
 if trial%50==0:print('progress',trial,'best',best,'elapsed',round(time.time()-start,1),flush=True)
 if len(found)==len(targets):break
print('done found',list(found),'best',best)