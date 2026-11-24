import itertools as it, pickle, heapq, time, os

def make(m):
 faces=[[] for _ in range(m+1)]
 for a in it.product(range(-1,4),repeat=m):
  if any(a.count(i)>2 for i in range(3)) or a.count(3)>m-5:continue
  f=tuple(4*j+x for j,x in enumerate(a) if x>=0)
  faces[len(f)].append(f)
 dims=list(map(len,faces));print('face cardinality counts',dims,flush=True)
 ids=[{f:i for i,f in enumerate(fs)} for fs in faces]
 mats=[None]
 for q in range(1,m+1):
  mats.append([{ids[q-1][f[:j]+f[j+1:]]:(-1)**j for j in range(q)} for f in faces[q]])
 return dims,mats

def rank_mod(mat,nrows,p):
 cols=[{i:v%p for i,v in c.items() if v%p} for c in mat]
 rows=[set() for _ in range(nrows)];heap=[]
 for j,c in enumerate(cols):
  for i in c:rows[i].add(j)
  if c:heapq.heappush(heap,(len(c),j))
 count=0
 while heap:
  _,j=heapq.heappop(heap);c=cols[j]
  if not c:continue
  i=min(c,key=lambda x:len(rows[x]));iv=pow(c[i],-1,p)
  for jj in list(rows[i]):
   if jj==j:continue
   cc=cols[jj];fac=cc[i]*iv%p
   for ii,w in c.items():
    z=(cc.get(ii,0)-fac*w)%p
    if z:
     if ii not in cc:rows[ii].add(jj)
     cc[ii]=z
    elif ii in cc:
     del cc[ii];rows[ii].discard(jj)
   if cc:heapq.heappush(heap,(len(cc),jj))
  for ii in c:rows[ii].discard(j)
  c.clear();count+=1
 return count
if __name__=='__main__' and False:
 m=8;fn=f'original{m}.pkl'
 if os.path.exists(fn): dims,mats=pickle.load(open(fn,'rb'))
 else:
  dims,mats=make(m);pickle.dump((dims,mats),open(fn,'wb'))
 for p in [2,3,5,101]:
  rr=[0]
  for q in range(1,m+1):
   t=time.time();r=rank_mod(mats[q],dims[q-1],p);rr.append(r)
   print('p,q,rank,time',p,q,r,round(time.time()-t,2),flush=True)
  rr.append(0)
  print('REDUCED BETTI indexed by face cardinality',p,[dims[q]-rr[q]-rr[q+1] for q in range(m+1)],flush=True)

def top_reduced(m):
 k=m-5;rows=[]
 for S in it.combinations(range(m),3):
  U=[x for x in range(m) if x not in S];p=U[0]
  for a in it.product(range(3),repeat=3):
   if len(set(a))==1:continue
   for omit in U[1:]:
    rows.append((tuple(zip(S,a)),tuple(x for x in U if x!=omit)))
 ids={r:i for i,r in enumerate(rows)};cols=[]
 for S in it.combinations(range(m),4):
  tau=tuple(x for x in range(m) if x not in S)
  for a in it.product(range(3),repeat=4):
   if any(a.count(i)>2 for i in range(3)):continue
   sig=tuple(zip(S,a));co={}
   for j in range(4):
    sig2=sig[:j]+sig[j+1:];p=next(x for x in range(m) if x not in dict(sig2))
    if p in tau:terms=[(tau,1)]
    else:
     u=tuple(sorted((p,)+tau));ip=u.index(p)
     terms=[(u[:h]+u[h+1:],(-1)**(h-ip+1)) for h in range(len(u)) if h!=ip]
    for t,s in terms:co[ids[sig2,t]]=(-1)**j*s
   cols.append(co)
 return len(rows),cols

def eliminate_units(mat,nrows):
 cols=[dict(c) for c in mat];rows=[set() for _ in range(nrows)];heap=[]
 for j,c in enumerate(cols):
  for i in c:rows[i].add(j)
  if c:heapq.heappush(heap,(len(c),j))
 count=0
 while heap:
  _,j=heapq.heappop(heap);c=cols[j]
  uu=[i for i,v in c.items() if abs(v)==1]
  if not uu:continue
  i=min(uu,key=lambda x:len(rows[x]));iv=c[i]
  for jj in list(rows[i]):
   if jj==j:continue
   cc=cols[jj];fac=cc[i]*iv
   for ii,w in c.items():
    z=cc.get(ii,0)-fac*w
    if z:
     if ii not in cc:rows[ii].add(jj)
     cc[ii]=z
    elif ii in cc:
     del cc[ii];rows[ii].discard(jj)
   if cc:heapq.heappush(heap,(len(cc),jj))
  for ii in c:rows[ii].discard(j)
  c.clear();count+=1
 return count,[c for c in cols if c]
if __name__=='__main__':
 for m in [9,10,11,12,13,14,15]:
  t=time.time()
  if os.path.exists(f'mats{m}.pkl'):
   dims,mats=pickle.load(open(f'mats{m}.pkl','rb')); nr=dims[3];mat=mats[3]
  else:nr,mat=top_reduced(m)
  n,rem=eliminate_units(mat,nr)
  print('m units remainingcols time',m,n,len(rem),round(time.time()-t,2),flush=True)
  print('residual entries',sorted({v for c in rem for v in c.values()}),flush=True)
  print('residual mod ranks',[(p,rank_mod(rem,nr,p)) for p in [2,3,5,7,101]],flush=True)
