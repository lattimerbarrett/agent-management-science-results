import numpy as np,itertools,pickle,json,random,time
from pathlib import Path
random.seed(289)
n=13;N=1<<n;ALL=(1<<N)-1
X=[sum(1<<x for x in range(N) if x>>i&1) for i in range(n)];LOW=[ALL^x for x in X];D6=sum(1<<x for x in range(N) if x.bit_count()<=6)
def mob(a):
 for i in range(n):a^=(a&LOW[i])<<(1<<i)
 return a
def times(a,i):return (a&X[i])^((a&LOW[i])<<(1<<i))
def pts(bs):
 out=[0]
 for b in bs:out +=[x^b for x in out]
 return out
A=range(7);B=[0,1,2,3,7,8,9];C=[4,5,6,7,8,9,10]
h=0
for bs in [A,B,C]:
 for x in pts([1<<i for i in bs]):h^=1<<x
assert h.bit_count()==324
seedrecords=json.load(open('workspace/agent2_h324_fullspan_seeds.json')); h=int(seedrecords[0]['truth_hex'],16); seed=mob(h)
cache='workspace/agent2_m13_moment5.pkl'
try:cols=pickle.load(open(cache,'rb'))
except FileNotFoundError:
 mons=[sum(1<<i for i in I) for d in range(6) for I in itertools.combinations(range(n),d)];points=np.arange(N,dtype=np.uint16);ev=np.empty((N,len(mons)),dtype=np.uint8)
 for j,mask in enumerate(mons):ev[:,j]=((points&mask)==mask)
 packed=np.packbits(ev,axis=1,bitorder='little');cols=[int.from_bytes(row.tobytes(),'little') for row in packed];del ev,packed
 pickle.dump(cols,open(cache,'wb'))
def closure(h):
 S=[];z=h
 while z:b=z&-z;S.append(b.bit_length()-1);z^=b
 piv={};rel={}
 for x in S:
  v=cols[x];g=1<<x
  while v:
   b=v.bit_length()-1
   if b not in piv:piv[b]=v;rel[b]=g;break
   v^=piv[b];g^=rel[b]
 for x in range(N):
  if h>>x&1:continue
  v=cols[x];g=1<<x
  while v:
   b=v.bit_length()-1
   if b not in piv:break
   v^=piv[b];g^=rel[b]
  if not v:return x,g
 return None
print('initialclosure',closure(h),flush=True)
a=seed;curh=h;seen=set();checked=0;different=0;accepted=0;hit=None;start=time.time()
for t in range(2000000):
 i,j,k=random.sample(range(n),3)
 if t%9==0:
  # Genuine nonlinear degree-truncating shear.
  diff=times(times((a&X[i])>>(1<<i),j),k)
  cand=a^(diff&D6)
  genuine=bool(diff&~D6)
 else:
  cand=a^times((a&X[i])>>(1<<i),j);genuine=False
 truth=mob(cand);w=truth.bit_count()
 energy=abs(w-328);oldenergy=abs(curh.bit_count()-328)
 if w>0 and (energy<=oldenergy or random.random()<__import__('math').exp((oldenergy-energy)/32)):
  a=cand;curh=truth;accepted+=1
  if genuine:different+=1
  if t%9==0 and w in (324,328,332) and truth not in seen:
   seen.add(truth);checked+=1
   result=closure(truth)
   if result:
    x,g=result;F=g|((g^truth)<<N);assert F.bit_count()==w+2
    assert not (mob(F&ALL)&~sum(1<<q for q in range(N) if q.bit_count()<=7))
    hit={'weight':w+2,'g':hex(g),'h':hex(truth),'truth_hex':hex(F),'outside':x};print('HIT',hit,flush=True);break
 if t and t%100000==0:print('progress',t,'unique',checked,'genuine',different,'sec',time.time()-start,flush=True)
 if t%200==0:
  # Occasional reset to another independently affine mixed seed.
  if random.random()<.05:
   curh=int(random.choice(seedrecords)['truth_hex'],16);a=mob(curh)
 if time.time()-start>115:break
print('DONE',t,'unique',checked,'genuine',different,'hit',bool(hit),'seconds',time.time()-start,flush=True)
json.dump(hit,open('workspace/agent2_h324_closure_hit.json','w'))

