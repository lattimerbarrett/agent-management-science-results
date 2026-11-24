import z3,time,json,functools
N=16384;parent=list(range(N))
def find(a):
 while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
 return a
def union(a,b):
 a=find(a);b=find(b)
 if a!=b:parent[a]=b
def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  a<<=1;b>>=1
  if a&16:a^=19
 return c
for trans in [[mul(a,2) for a in range(16)],[mul(a,a) for a in range(16)]]:
 for v in range(N):
  w=(v&12288)|sum(trans[(v>>(4*j))&15]<<(4*j) for j in range(3))
  union(v,w)
D={}
for v in range(N):D.setdefault(find(v),[]).append(v)
orbits=list(D.values());oid={v:i for i,O in enumerate(orbits) for v in O}
from collections import Counter
print('orbits',len(orbits),Counter(map(len,orbits)),flush=True)
C=[1<<oid[v] for v in range(N)]
for b in range(14):
 for v in range(N):
  if v>>b&1:C[v]^=C[v^(1<<b)]
B={}
for v in range(N):
 if v.bit_count()<=7:continue
 r=C[v]
 while r:
  p=r.bit_length()-1
  if p in B:r^=B[p]
  else:B[p]=r;break
print('rank',len(B),'dim',len(orbits)-len(B),flush=True)
for threshold in [60,30]:
 BB=B.copy()
 for i,O in enumerate(orbits):
  if len(O)<threshold:continue
  r=1<<i
  while r:
   p=r.bit_length()-1
   if p in BB:r^=BB[p]
   else:BB[p]=r;break
 print('excluded>=',threshold,'dim',len(orbits)-len(BB),flush=True)
import random
free=[i for i in range(len(orbits)) if i not in B]
basis=[]
for i in free:
 v=1<<i
 for p,r in sorted(B.items()):
  if (r&v).bit_count()%2:v^=1<<p
 basis.append(v)
largepos=[i for i,O in enumerate(orbits) if len(O)==60]
large=sum(1<<i for i in largepos)
wmasks={d:sum(1<<i for i,O in enumerate(orbits) if len(O)==d) for d in [1,15,30,60]}
rng=random.Random(851);found={};t=time.time()
def test(v):
 if (v&large).bit_count()>5:return
 for k in kv:
  z=v^k
  wt=sum(d*(z&wmasks[d]).bit_count() for d in [1,15,30,60])
  if wt in [330,334] and wt not in found:
   found[wt]=z
   print('FOUND',wt,flush=True)
   truth=[int(z>>oid[x]&1) for x in range(N)];anf=truth.copy()
   for bb in range(14):
    for x in range(N):
     if x>>bb&1:anf[x]^=anf[x^(1<<bb)]
   assert sum(truth)==wt and max(x.bit_count() for x,c in enumerate(anf) if c)<=7
   json.dump({'weight':wt,'anf':[x for x,c in enumerate(anf) if c]},open('workspace/agent3_singer4_%d.json'%wt,'w'))
for trial in range(100):
 rng.shuffle(largepos);P={};K=[]
 for v in basis:
  proj=sum(((v>>p)&1)<<j for j,p in enumerate(largepos))
  while proj:
   p=proj.bit_length()-1
   if p in P:proj^=P[p][0];v^=P[p][1]
   else:P[p]=(proj,v);break
  if not proj:K.append(v)
 for p in sorted(P):
  pp,pv=P[p]
  for q in list(P):
   if q>p and P[q][0]>>p&1:P[q]=(P[q][0]^pp,P[q][1]^pv)
 vals=[v for pp,v in P.values()]
 kv=[0]
 for k in K:kv += [z^k for z in kv]
 for i,v in enumerate(vals):
  test(v)
  for j,u in enumerate(vals[:i]):
   vu=v^u;test(vu)
   for w in vals[:j]:test(vu^w)
 if trial%10==0:print('ISD',trial,'sec',time.time()-t,'rank',len(P),'kernel',len(K),flush=True)
 if len(found)==2:break
print('DONEISD',time.time()-t,found.keys(),flush=True)
checkpos=[j for j in range(len(largepos)) if j not in P]
columns=[sum((int(i==j) if i not in P else ((P[i][0]>>j)&1))<<k for k,j in enumerate(checkpos)) for i in range(len(largepos))]
pairs={};low={0}
for i in range(len(columns)):
 if columns[i]==0:low.add(1<<i)
 for j in range(i):pairs.setdefault(columns[i]^columns[j],[]).append((1<<i)|(1<<j))
for sy,pp in pairs.items():
 if sy==0:low.update(pp)
 for i in range(len(columns)):
  if sy==columns[i]:low.update(p^(1<<i) for p in pp)
 if len(pp)>1:
  for p in pp:
   for q in pp:low.add(p^q)
for i in range(len(columns)):
 for j in range(i):
  sy=columns[i]^columns[j]
  for k in range(j):
   pp=pairs.get(sy^columns[k])
   if pp:
    v=(1<<i)|(1<<j)|(1<<k)
    low.update(v^p for p in pp)
print('EXACTlowprojected',len(low),flush=True)
for proj in low:
 v=0;r=proj
 while r:
  p=r.bit_length()-1
  assert p in P
  r^=P[p][0];v^=P[p][1]
 test(v)
print('EXACTDONE',found.keys(),flush=True)
raise SystemExit
X=[z3.Bool('x%d'%i) for i in range(len(orbits))]
s=z3.SolverFor('QF_FD');s.set(timeout=60000)
for r in B.values():
 vs=[X[i] for i in range(len(orbits)) if r>>i&1]
 s.add(z3.Not(functools.reduce(z3.Xor,vs)))
for wt in [330,334]:
 s.push()
 for i,O in enumerate(orbits):
  if len(O)==1:s.add(X[i] if wt==334 else z3.Not(X[i]))
 s.add(z3.PbEq([(X[i],len(O)//15) for i,O in enumerate(orbits) if len(O)>1],22))
 t=time.time();status=s.check();print('target',wt,status,time.time()-t,flush=True)
 if status==z3.sat:
  model=s.model();truth=[int(z3.is_true(model.eval(X[oid[v]]))) for v in range(N)];anf=truth.copy()
  for b in range(14):
   for v in range(N):
    if v>>b&1:anf[v]^=anf[v^(1<<b)]
  assert sum(truth)==wt and max(v.bit_count() for v,c in enumerate(anf) if c)<=7
  json.dump({'weight':wt,'anf':[v for v,c in enumerate(anf) if c]},open('workspace/agent3_singer4_%d.json'%wt,'w'))
 s.pop()
