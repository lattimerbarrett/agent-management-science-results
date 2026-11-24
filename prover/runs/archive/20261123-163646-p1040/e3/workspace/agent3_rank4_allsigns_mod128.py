import itertools,time,json,os,functools
import numpy as np
n=4;m=n-1;K=7;mod=2**K
signslist=[s for s in itertools.product([0,1],repeat=n) if any(s)];C=len(signslist)
I=np.tile(np.eye(m,dtype=np.int64),(C,1,1));identity=I.tobytes()
def mul(a,b):return np.matmul(a,b)%mod
def power(a,e):
 if e<0:return power(inv(a),-e)
 o=I.copy()
 while e:
  if e&1:o=mul(o,a)
  e//=2;a=mul(a,a)
 return o
@functools.lru_cache(None)
def invbytes(key):
 a=np.frombuffer(key,dtype=np.int64).reshape(C,m,m)
 return power(a,mod-1)
def inv(a):return invbytes(a.tobytes())
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
def fullmat(typ,i,j,k=None):
 out=[]
 for signs in signslist:
  elim=signs.index(1);coords=[s for s in range(n) if s!=elim]
  a=[[int(r==s) for s in range(n)] for r in range(n)]
  if typ=='K':a[i][i]=1-2*signs[j];a[i][j]=2*signs[i]
  else:a[i][j]=-2*signs[k];a[i][k]=2*signs[j]
  out.append([[(a[r][s]-signs[r]*a[elim][s])%mod for s in coords] for r in coords])
 return np.array(out,dtype=np.int64)
gens=[]
for i in range(n):
 for j in range(n):
  if i!=j:gens.append(fullmat('K',i,j))
 for j,k in itertools.combinations([s for s in range(n) if s!=i],2):gens.append(fullmat('M',i,j,k))
def val(a):
 x=((a-I)%mod).reshape(-1);v=K
 for z in x:
  z=int(z)
  if z:v=min(v,(z&-z).bit_length()-1)
 return v
def pivot(a):
 x=((a-I)%mod).reshape(-1)
 for v in range(1,K):
  nz=np.flatnonzero((x>>v)&1)
  if nz.size:return v,int(nz[0])
 return None
def reduce(a,basis):
 while True:
  p=pivot(a)
  if p is None or p not in basis:return a
  a=mul(a,basis[p])
def closure(seeds,label=''):
 basis={};queue=list(seeds);head=0;t=time.time()
 while head<len(queue):
  a=reduce(queue[head],basis);head+=1;p=pivot(a)
  if p is None:continue
  d=p[0];basis[p]=a
  if d+1<K:queue.append(mul(a,a))
  for b in gens:
   if d+val(b)<K:queue.append(comm(a,b))
  for q,b in list(basis.items()):
   if q!=p and d+q[0]<K:queue.append(comm(a,b))
  if len(basis)%50==0:print(label,len(basis),'queue',head,len(queue),'secs',round(time.time()-t,2),flush=True)
 print(label,'DONE',len(basis),'secs',round(time.time()-t,3),flush=True)
 return basis
seedgs=[fullmat('K',0,1),fullmat('K',0,2),fullmat('M',0,1,2),fullmat('K',1,0),fullmat('K',1,2),fullmat('M',1,0,2),fullmat('K',2,0),fullmat('K',2,1),fullmat('M',2,0,1)]
def W(i,j,k,l):return comm(comm(comm(seedgs[i],seedgs[j]),seedgs[k]),seedgs[l])
w=I.copy()
for inds,e in [((0,1,5,2),3),((0,1,1,1),-4),((0,2,5,1),2),((1,2,3,1),-2)]:w=mul(w,power(W(*inds),e))
print('seed val',val(w),flush=True)
b=None;results=[]
for c in range(1,6):
 seeds=gens if c==1 else [comm(x,y) for x in b.values() for y in gens if val(x)+val(y)<K]
 b=closure(seeds,'gamma%d'%c)
 r=reduce(w,b);print('seed remainder val',val(r),flush=True)
 results.append({'c':c,'log2order':len(b),'seed_nonzero':bool(np.any(r!=I))})
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent3_rank4_allsigns_mod128.py','w') as f:f.write(open(__file__).read())
with open('workspace/agent3_rank4_allsigns_mod128.json','w') as f:json.dump(results,f,indent=2)
