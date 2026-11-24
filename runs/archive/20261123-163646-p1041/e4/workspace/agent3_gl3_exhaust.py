import time,json,itertools
N=16384;parent=list(range(N))
def find(a):
 while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
 return a
def union(a,b):
 a=find(a);b=find(b)
 if a!=b:parent[a]=b
for i in range(3):
 for j in range(3):
  if i==j:continue
  perm=[(v ^ (((v>>i)&1)<<j))-1 for v in range(1,8)]
  trans=[sum(((x>>k)&1)<<perm[k] for k in range(7)) for x in range(128)]
  for v in range(N):union(v,trans[v&127]|(trans[v>>7]<<7))
reps={}
for v in range(N):reps.setdefault(find(v),[]).append(v)
orbits=list(reps.values());oid={v:i for i,O in enumerate(orbits) for v in O}
coeff=[0]*N
for i,O in enumerate(orbits):
 for v in O:coeff[v]=1<<i
for b in range(14):
 for v in range(N):
  if v>>b&1:coeff[v]^=coeff[v^(1<<b)]
rows=[coeff[v] for v in range(N) if v.bit_count()>7]
rows += [1<<i for i,O in enumerate(orbits) if len(O)>=84]
masks={d:sum(1<<i for i,O in enumerate(orbits) if len(O)==d) for d in [1,7,21,28,42,84,168]}

def space(equations):
 B={}
 for row,rhs in equations:
  while row:
   p=row.bit_length()-1
   if p in B:row^=B[p][0];rhs^=B[p][1]
   else:B[p]=(row,rhs);break
  if not row and rhs:return None
 free=[i for i in range(len(orbits)) if i not in B]
 def lift(f,homog):
  v=f
  for p,(row,rhs) in sorted(B.items()):
   if ((row&v).bit_count()%2)^(0 if homog else rhs):v^=1<<p
  return v
 return lift(0,False),[lift(1<<i,True) for i in free]

def enumspan(basis):
 vals=[0]
 for b in basis:vals += [x^b for x in vals]
 return vals

targets=[310,322,326,330];patterns={310:{0,16383},322:set(),326:{0,127,16256,16383},330:{0}}
found={}
for target in targets:
 equations=[(r,0) for r in rows]+[(1<<oid[v],int(v in patterns[target])) for v in [0,127,16256,16383]]
 result=space(equations)
 if result is None:print('empty',target);continue
 particular,basis=result
 P={};K=[]
 for b in basis:
  proj=b&masks[42]
  while proj:
   p=proj.bit_length()-1
   if p in P:b^=P[p];proj=b&masks[42]
   else:P[p]=b;break
  if not proj:K.append(b)
 print('target',target,'dim',len(basis),'P',len(P),'K',len(K),flush=True)
 kv=enumspan(K);pv=enumspan(list(P.values()));count=0;t=time.time()
 for v in pv:
  z=particular^v
  w42=(z&masks[42]).bit_count()*42
  if w42>target:continue
  count+=1
  for k in kv:
   zz=z^k
   w=w42+sum(d*(zz&masks[d]).bit_count() for d in [1,7,21,28])
   if w==target:
    found[target]=zz;break
  if target in found:break
 print('done',target,'selected',count,'seconds',time.time()-t,'FOUND',target in found,flush=True)
 if target in found:
  z=found[target];truth=[int(z>>oid[v]&1) for v in range(N)];anf=truth.copy()
  for b in range(14):
   for v in range(N):
    if v>>b&1:anf[v]^=anf[v^(1<<b)]
  assert sum(truth)==target and max(v.bit_count() for v,a in enumerate(anf) if a)<=7
  out={w:[v for v,a in enumerate(anf) if a] for w in []}
  json.dump({'weight':target,'anf':[v for v,a in enumerate(anf) if a]},open('workspace/agent3_GL3_%d.json'%target,'w'))

# Search all patterns on84/168orbits allowed by the total weight budget.
large=masks[84]|masks[168]
rows_full=[coeff[v] for v in range(N) if v.bit_count()>7]
for target in [322,326,330]:
 equations=[(r,0) for r in rows_full]+[(1<<oid[v],int(v in patterns[target])) for v in [0,127,16256,16383]]
 result=space(equations)
 if result is None:continue
 particular,basis=result;LP={};SK=[]
 for b in basis:
  proj=b&large
  while proj:
   p=proj.bit_length()-1
   if p in LP:b^=LP[p];proj=b&large
   else:LP[p]=b;break
  if not proj:SK.append(b)
 P={};K=[]
 for b in SK:
  proj=b&masks[42]
  while proj:
   p=proj.bit_length()-1
   if p in P:b^=P[p];proj=b&masks[42]
   else:P[p]=b;break
  if not proj:K.append(b)
 kv=enumspan(K);pv=enumspan(list(P.values()))
 print('FULL',target,'LP',len(LP),'P',len(P),'K',len(K),flush=True)
 indices84=[i for i,O in enumerate(orbits) if len(O)==84];indices168=[i for i,O in enumerate(orbits) if len(O)==168]
 choices=[()] + [(i,) for i in indices84+indices168]+list(itertools.combinations(indices84,2))+list(itertools.combinations(indices84,3))+[(i,j) for i in indices84 for j in indices168]
 t=time.time();valid=0;tested=0
 for selected in choices:
  bigweight=sum(len(orbits[i]) for i in selected)
  if bigweight>target:continue
  lp=particular;rem=(particular&large)^sum(1<<i for i in selected)
  while rem:
   p=rem.bit_length()-1
   if p not in LP:break
   lp^=LP[p];rem=lp&large ^ sum(1<<i for i in selected)
  if rem:continue
  valid+=1
  budget=target-bigweight
  for v in pv:
   z=lp^v;w42=(z&masks[42]).bit_count()*42
   if w42>budget:continue
   tested+=1
   for k in kv:
    zz=z^k
    w=bigweight+w42+sum(d*(zz&masks[d]).bit_count() for d in [1,7,21,28])
    if w==target:
     found[target]=zz;break
   if target in found:break
  if target in found:break
 print('FULLDONE',target,'valid',valid,'tested',tested,'seconds',time.time()-t,'found',target in found,flush=True)
 if target in found:
  z=found[target];truth=[int(z>>oid[v]&1) for v in range(N)];anf=truth.copy()
  for b in range(14):
   for v in range(N):
    if v>>b&1:anf[v]^=anf[v^(1<<b)]
  assert sum(truth)==target and max(v.bit_count() for v,a in enumerate(anf) if a)<=7
  json.dump({'weight':target,'anf':[v for v,a in enumerate(anf) if a]},open('workspace/agent3_GL3_%d.json'%target,'w'))
