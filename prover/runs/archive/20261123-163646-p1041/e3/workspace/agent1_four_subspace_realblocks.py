import random,itertools,json,time
rng=random.Random(91283)
def basis(rows):
 P={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in P:v^=P[p]
   else:P[p]=v;break
 return P

def kernel(rows,n):
 P=basis(rows);out=[]
 for j in range(n):
  if j in P:continue
  v=1<<j
  for p,r in sorted(P.items()):
   if (r&v).bit_count()%2:v^=1<<p
  out.append(v)
 return out

def randomspace(D,d):
 P={}
 while len(P)<d:
  v=rng.randrange(1,1<<D)
  for p,r in sorted(P.items(),reverse=True):
   if v>>p&1:v^=r
  if v:P[v.bit_length()-1]=v
 return list(P.values())

def endorank(U,D):
 rows=[]
 for B in U:
  for a in kernel(B,D):
   for b in B:
    rows.append(sum((b<<(i*D)) for i in range(D) if a>>i&1))
 return kernel(rows,D*D)

def indecomp(U,D):
 E=endorank(U,D)
 if len(E)>8:return False
 I=sum(1<<(i*D+i) for i in range(D))
 mats=[0]
 for b in E:mats += [x^b for x in mats]
 mask=(1<<D)-1
 for A in mats:
  if A in (0,I):continue
  rows=[(A>>(i*D))&mask for i in range(D)];sq=0
  for i,row in enumerate(rows):
   r=0
   while row:
    bit=row&-row;r^=rows[bit.bit_length()-1];row^=bit
   sq|=r<<(i*D)
  if sq==A:return False
 return True

blocks=[];start=time.time()
for D in range(2,14):
 dims=[]
 if D%2==0:
  k=D//2
  for arm in range(4):
   for s in [-1,1]:
    ds=[k]*4;ds[arm]+=s
    if min(ds)>=0 and max(ds)<=7:dims.append(tuple(ds))
 else:
  k=D//2
  for bits in range(16):
   ds=tuple(k+((bits>>i)&1) for i in range(4))
   if max(ds)<=7:dims.append(ds)
 for ds in dims:
  for trial in range(100000):
   U=[randomspace(D,d) for d in ds]
   if indecomp(U,D):break
  else:
   if D==3:
    planes=[kernel([a],3) for a in range(1,8)];lines=[[a] for a in range(1,8)]
    lists=[planes if d==2 else lines for d in ds]
    best=min((endorank(U,D),U) for U in itertools.product(*lists))
    maxrank=max(endorank(U,D) for U in itertools.product(*lists))
    print('EXHAUST',D,ds,best[0],maxrank,flush=True)
   raise RuntimeError((D,ds))
  # Endomorphism algebra has no nontrivial idempotents, certifying indecomposability.
  # These are only real-root representatives, not a full arbitrary-word census.
  pairdims=[ds[i]+ds[j]-len(basis(U[i]+U[j])) for i,j in itertools.combinations(range(4),2)]
  assert pairdims==[max(0,ds[i]+ds[j]-D) for i,j in itertools.combinations(range(4),2)]
  blocks.append({'D':D,'dims':ds,'U':U,'pairdims':pairdims,'trials':trial+1})
 print('D',D,'blocks',len(blocks),'seconds',round(time.time()-start,2),flush=True)
open('workspace/agent1_four_subspace_realblocks.json','w').write(json.dumps(blocks))
print('saved real-root blocks',len(blocks))
open('workspace/agent1_four_subspace_realblocks.py','w').write(open(__file__).read())
