import itertools,json,random,time
S=json.load(open('workspace/agent4_flat_seeds.json'));N=1<<14;ALL=(1<<N)-1
X=[]
for i in range(14):
 block=(1<<(1<<i))-1;s=0
 for j in range(1<<i,N,2<<i):s |=block<<j
 X.append(s)
def pts(mask):
 p=[0]
 for i in range(14):
  if mask>>i&1:p +=[x^(1<<i) for x in p]
 return p
def bits(p):return sum(1<<x for x in p)
def anf(b):
 import numpy as np
 a=np.zeros(N,dtype=np.int8)
 while b:
  z=b&-b;a[z.bit_length()-1]=1;b ^=z
 h=1
 while h<N:
  aa=a.reshape(-1,2*h);aa[:,h:] ^=aa[:,:h];h*=2
 return [int(x) for x in np.flatnonzero(a)]
M={}
def monom(q):
 if q not in M:
  z=ALL
  for j in range(14):
   if q>>j&1:z &=X[j]
  M[q]=z
 return M[q]
found={};seeds=[]
for w,ms in S.items():
 b=0
 for m in ms:b ^=bits(pts(m))
 seeds.append(b)
target={322,326,330,334}
for restart,b in enumerate(seeds):
 top=[m for m in anf(b) if m.bit_count()==7]
 for i in range(14):
  dtop=[m^(1<<i) for m in top if m>>i&1]
  swap=((b&X[i])>>(1<<i))|((b&(ALL^X[i]))<<(1<<i))
  for j,k in itertools.combinations([j for j in range(14) if j!=i],2):
   q=(1<<j)|(1<<k);bb=b^((b^swap)&X[j]&X[k])
   for t in dtop:
    if not t&q:bb ^=monom(t|q)
   nw=bb.bit_count()
   if nw in target-found.keys():
    aa=anf(bb);assert max(m.bit_count() for m in aa)<=7
    found[nw]={'support':hex(bb),'anf':aa}
    json.dump(found,open('workspace/a1_truncation_seeds.json','w'));print('FOUND',nw,'seed',list(S)[restart],'i,j,k',i,j,k,flush=True)
 if restart%10==0:print('restart',restart,'found',list(found),flush=True)
print('done',found.keys())
open('workspace/a1_truncation_search.py','w').write(open(__file__).read())
random.seed(10234)
for restart in range(20):
 b=random.choice(seeds);top=[m for m in anf(b) if m.bit_count()==7];w=b.bit_count()
 goal=random.choice(sorted(target-found.keys())) if len(found)<4 else 322
 for step in range(10000):
  if step%25==0:
   ii,jj=random.sample(range(14),2)
   sw=((b&X[ii])>>(1<<ii))|((b&(ALL^X[ii]))<<(1<<ii))
   b ^= (b^sw)&X[jj]
   top=[m for m in anf(b) if m.bit_count()==7]
  i,j,k=random.sample(range(14),3);q=(1<<j)|(1<<k)
  swap=((b&X[i])>>(1<<i))|((b&(ALL^X[i]))<<(1<<i))
  bb=b^((b^swap)&X[j]&X[k])
  for m in top:
   if m>>i&1:
    t=m^(1<<i)
    if not t&q:bb ^=monom(t|q)
  nw=bb.bit_count();delta=abs(nw-goal)-abs(w-goal)
  temperature=2.5 if step%500<100 else .6
  import math
  if delta<=0 or random.random()<math.exp(-min(700,delta/temperature)):
   if bb!=b:
    b=bb;w=nw;top=[m for m in anf(b) if m.bit_count()==7]
  if nw in target-found.keys():
   aa=anf(bb);assert max(m.bit_count() for m in aa)<=7
   found[nw]={'support':hex(bb),'anf':aa}
   json.dump(found,open('workspace/a1_truncation_seeds.json','w'));print('FOUND WALK',nw,'restart',restart,'step',step,flush=True)
  if len(found)==4:break
 print('WALK',restart,'last',w,'top',len(top),'found',list(found),flush=True)
 if len(found)==4:break