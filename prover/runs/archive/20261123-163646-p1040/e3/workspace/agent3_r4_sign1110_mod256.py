import itertools,time,json,os
n=4;m=n-1;K=8;mod=2**K
signs=[1,1,1,0];elim=signs.index(1);coords=[i for i in range(n) if i!=elim]
I=tuple(int(i==j) for i in range(m) for j in range(m))
def mul(a,b):return tuple(sum(a[i*m+k]*b[k*m+j] for k in range(m))%mod for i in range(m) for j in range(m))
def power(a,e):
 if e<0:return power(inv(a),-e)
 o=I
 while e:
  if e&1:o=mul(o,a)
  e//=2;a=mul(a,a)
 return o
def inv(a):
 # finite2 group exponent divides2^K for level2 matrices
 return power(a,mod-1)
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
def fullmat(typ,i,j,k=None):
 a=[[int(r==s) for s in range(n)] for r in range(n)]
 if typ=='K':a[i][i]=1-2*signs[j];a[i][j]=2*signs[i]
 else:a[i][j]=-2*signs[k];a[i][k]=2*signs[j]
 return tuple((a[r][s]-signs[r]*a[elim][s])%mod for r in coords for s in coords)
gens=[]
for i in range(n):
 for j in range(n):
  if i!=j:gens.append(fullmat('K',i,j))
 for j,k in itertools.combinations([s for s in range(n) if s!=i],2):gens.append(fullmat('M',i,j,k))
def val(a):
 return min([((x-y)%mod & -((x-y)%mod)).bit_length()-1 for x,y in zip(a,I) if x!=y] or [K])
def pivot(a):
 v=val(a)
 if v==K:return None
 return v,next(i for i,(x,y) in enumerate(zip(a,I)) if ((x-y)>>v)&1)
def reduce(a,basis):
 while a!=I:
  p=pivot(a)
  if p not in basis:return a
  a=mul(a,basis[p])
 return a
def closure(seeds,label=''):
 basis={};queue=list(seeds);head=0;t=time.time()
 while head<len(queue):
  a=reduce(queue[head],basis);head+=1
  if a==I:continue
  p=pivot(a);d=p[0];basis[p]=a
  if d+1<K:queue.append(mul(a,a))
  for b in gens:
   if d+val(b)<K:queue.append(comm(a,b))
  for q,b in list(basis.items()):
   if q!=p and d+q[0]<K:queue.append(comm(a,b))
 print(label,len(basis),'secs',round(time.time()-t,3),flush=True)
 return basis
seedgs=[fullmat('K',0,1),fullmat('K',0,2),fullmat('M',0,1,2),fullmat('K',1,0),fullmat('K',1,2),fullmat('M',1,0,2),fullmat('K',2,0),fullmat('K',2,1),fullmat('M',2,0,1)]
def W(i,j,k,l):return comm(comm(comm(seedgs[i],seedgs[j]),seedgs[k]),seedgs[l])
w=I
for inds,e in [((0,1,5,2),3),((0,1,1,1),-4),((0,2,5,1),2),((1,2,3,1),-2)]:w=mul(w,power(W(*inds),e))
print('seed',w,'val',val(w),flush=True)
b=None;results=[]
for c in range(1,8):
 seeds=gens if c==1 else [comm(x,y) for x in b.values() for y in gens if val(x)+val(y)<K]
 b=closure(seeds,'gamma%d'%c)
 r=reduce(w,b);print('seed remainder',r,'val',val(r),flush=True)
 results.append({'c':c,'log2order':len(b),'seed_nonzero':r!=I})
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent3_r%d_sign%s_mod256.py'%(n,''.join(map(str,signs))),'w') as f:f.write(open(__file__).read())
with open('workspace/agent3_r%d_sign%s_mod256.json'%(n,''.join(map(str,signs))),'w') as f:json.dump(results,f,indent=2)
