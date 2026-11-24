import itertools,numpy as np,time,json

def partitions(n,k,lo=1):
 if k==0:
  if n==0:yield()
  return
 for a in range(lo,n//k+1):
  for rest in partitions(n-a,k-1,a):yield(a,)+rest

def subspace(ns,weights):
 t=len(ns);N=1<<t;cells=[i for i,w in enumerate(weights) if w<=334]
 C=[0]*N
 for j,x in enumerate(cells):C[x]=1<<j
 for b in range(t):
  for x in range(N):
   if x>>b&1:C[x]^=C[x^(1<<b)]
 B={}
 for s,row in enumerate(C):
  if sum(ns[i] for i in range(t) if s>>i&1)<=7:continue
  while row:
   p=row.bit_length()-1
   if p in B:row^=B[p]
   else:B[p]=row;break
 basis=[]
 for i in range(len(cells)):
  if i in B:continue
  v=1<<i
  for p,row in sorted(B.items()):
   if (v&row).bit_count()%2:v^=1<<p
  basis.append(v)
 return cells,basis

def fwht(a):
 h=1
 while h<len(a):
  A=a.reshape(-1,2*h);x=A[:,:h].copy();np.add(A[:,:h],A[:,h:],out=A[:,:h]);np.subtract(x,A[:,h:],out=A[:,h:]);h*=2

found={};targets={310,322,326,330,334};start=time.time();count=0;dims={}
for t in range(2,8):
 for ns in partitions(14,t):
  options=[list(range(1,min(32,1<<(n-1)),2)) if n>=2 else[1] for n in ns]
  for aa in itertools.product(*options):
   if max(aa)==1:continue
   if any(ns[i]==ns[i-1] and aa[i]<aa[i-1] for i in range(1,t)):continue
   weights=[np.prod([aa[i] if x>>i&1 else (1<<ns[i])-aa[i] for i in range(t)],dtype=np.int64).item() for x in range(1<<t)]
   cells,basis=subspace(ns,weights);d=len(basis);dims[d]=dims.get(d,0)+1
   if d!=30:continue
   hist=np.zeros(1<<d,dtype=np.int16)
   for j,x in enumerate(cells):
    pattern=sum(((v>>j)&1)<<i for i,v in enumerate(basis));hist[pattern]+=weights[x]
   total=int(hist.sum());fwht(hist);count+=1
   for target in targets-found.keys():
    ids=np.flatnonzero(hist==total-2*target)
    if len(ids):
     u=int(ids[0]);truth=0
     for i,v in enumerate(basis):
      if u>>i&1:truth^=v
     support=[cells[j] for j in range(len(cells)) if truth>>j&1]
     found[target]={'ns':ns,'aa':aa,'super_support':support}
     print('FOUND',target,found[target],flush=True);json.dump(found,open('workspace/agent3_composition_seeds.json','w'))
   if targets<=found.keys():break
  if targets<=found.keys():break
 if targets<=found.keys():break
 print('t',t,'checked',count,'secs',time.time()-start,'dims',dims,flush=True)
print('done',found,time.time()-start)
