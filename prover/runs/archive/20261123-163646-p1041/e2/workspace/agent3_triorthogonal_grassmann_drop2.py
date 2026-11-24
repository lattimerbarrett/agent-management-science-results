import itertools,json,pathlib,time,collections,random,sys
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese
rng=random.Random(381312);n=38;ALL=(1<<n)-1

def bas(rows):
 D={}
 for z in rows:
  while z:
   p=z.bit_length()-1
   if p in D:z^=D[p]
   else:D[p]=z;break
 return D

def solve(rows,bs=None):
 if bs is None:bs=[0]*len(rows)
 D={};rhs={}
 for z,b in zip(rows,bs):
  while z:
   p=z.bit_length()-1
   if p in D:z^=D[p];b^=rhs[p]
   else:D[p]=z;rhs[p]=b;break
  if z==0 and b:return None
 def back(z):
  for p in sorted(D):
   if ((D[p]&z).bit_count()&1)!=rhs[p]:z^=1<<p
  return z
 part=back(0);free=[i for i in range(n) if i not in D]
 # homogeneous solve removes affine particular
 ker=[back(1<<i)^part for i in free]
 return part,ker,D

def square(C):return list({a&b for i,a in enumerate(C) for b in C[:i+1]})
def patterns(C):return [sum(((r>>i)&1)<<j for j,r in enumerate(C)) for i in range(n)]
def independent(C,r):
 D=bas(C)
 while r:
  p=r.bit_length()-1
  if p in D:r^=D[p]
  else:return True
 return False
# obtain a newly derived T38 seed of Kdim11
raw=json.loads(pathlib.Path('workspace/agent4_boundary256_orbits.json').read_text())[0]
S={(p&63)|((p>>9)<<6) for p in raw['support']};vs=veronese(8,2)
found=None
for piv in itertools.combinations(range(7),3):
 if found:break
 non=[j for j in range(7) if j not in piv];free=[(i,j) for i,p in enumerate(piv) for j in non if j>p]
 for z in range(1<<len(free)):
  if found:break
  B=[1<<p for p in piv]
  for h,(i,j) in enumerate(free):
   if z>>h&1:B[i]^=1<<j
  H=[0]
  for b in B:H += [x^b for x in H]
  offs=[0]
  for j in non:offs += [x^(1<<j) for x in offs]
  for off in offs:
   K=[x^off for x in H];F=set(K+[x^128 for x in K])
   if len(S&F)!=5:continue
   T=sorted(S^F)
   if 38-len(bas([vs[p] for p in T]))==11:found=T;break
assert found
C=[ALL]+[sum(((p>>j)&1)<<i for i,p in enumerate(found)) for j in range(8)]
assert len(bas(C))==len(C) and len(set(patterns(C)))==38
while True:
 _,ker,_=solve(square(C));extra=next((r for r in ker if independent(C,r)),None)
 if extra is None:break
 C.append(extra)
print('initial rank',len(C),flush=True)
def drop(C):
 k=len(C);u=rng.randrange(1,1<<(k-1));pivot=u.bit_length()-1;rr=C[pivot+1]
 return [ALL]+[r^(rr if u>>j&1 else 0) for j,r in enumerate(C[1:]) if j!=pivot]
start=time.time();steps=0;best=len(C);counts=collections.Counter();hits=[];blocked=0
while time.time()-start<115:
 steps+=1;k=len(C);D=drop(drop(C))
 if max(collections.Counter(patterns(D)).values())>4:blocked+=1;continue
 _,firstker,_=solve(square(D))
 for attempt in range(6):
  r=0
  for b in firstker:
   if rng.getrandbits(1):r^=b
  if independent(D,r) and max(collections.Counter(patterns(D+[r])).values())<=2:break
 else:blocked+=1;continue
 D.append(r)
 pat=patterns(D);groups={}
 for i,a in enumerate(pat):groups.setdefault(a,[]).append(i)
 if any(len(a)>2 for a in groups.values()):blocked+=1;continue
 dup=[(1<<a[0])^(1<<a[1]) for a in groups.values() if len(a)==2]
 sq=square(D);sol=solve(sq+dup,[0]*len(sq)+[1]*len(dup))
 if sol is None:blocked+=1;continue
 part,ker,_=sol
 # choose random replacement and avoid dependence (rare)
 for attempt in range(5):
  r=part
  for b in ker:
   if rng.getrandbits(1):r^=b
  if independent(D,r):break
 else:blocked+=1;continue
 C=D+[r]
 assert all((r&a&b).bit_count()%2==0 for i,a in enumerate(D) for b in D[:i+1])
 _,K,_=solve(square(C));counts[len(K)]+=1
 while len(K)>len(C):
  extra=next((r for r in K if independent(C,r)),None)
  if extra is None:break
  C.append(extra);_,K,_=solve(square(C))
 if len(C)>best:
  best=len(C);print('NEW',best,'step',steps,'elapsed',time.time()-start,flush=True)
  hits.append({'rank':best,'rows':C.copy()})
  if best>=13:break
 if steps%10000==0:
  assert len(set(patterns(C)))==38 and len(bas(C))==len(C)
print('steps',steps,'best',best,'blocked',blocked,'Kcounts',dict(counts),'elapsed',time.time()-start,flush=True)
out={'steps':steps,'best_rank':best,'blocked':blocked,'Kcounts':dict(counts),'hits':hits,'final_rows':C}
pathlib.Path('workspace/agent3_triorthogonal_grassmann_drop2.json').write_text(json.dumps(out,indent=2))
pathlib.Path('workspace/agent3_triorthogonal_grassmann_drop2.py').write_text(pathlib.Path(__file__).read_text())
