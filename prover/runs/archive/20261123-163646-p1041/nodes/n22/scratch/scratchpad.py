import json,itertools,random,time
n=13;S=json.load(open('T316_projection_example.json'));SS=set(S)
mons=[sum(1<<j for j in I) for r in range(6) for I in itertools.combinations(range(n),r)];idx={a:i for i,a in enumerate(mons)}
def veronese(p):
 v=0;s=p
 while True:
  if s in idx:v|=1<<idx[s]
  if s==0:break
  s=(s-1)&p
 return v
basis={}
def reduce(v):
 while v:
  k=v.bit_length()-1
  if k not in basis:return v
  v^=basis[k]
 return 0
for p in S:
 v=reduce(veronese(p))
 if v:basis[v.bit_length()-1]=v
# A complete quotient normal form, not just reduction at the leading pivot.
def residual(v):
 for k,b in sorted_basis:
  if v>>k&1:v^=b
 return v
sorted_basis=sorted(basis.items(),reverse=True)
rng=random.Random(6316);masks=[rng.getrandbits(len(mons)) for _ in range(64)]
def hash64(v):return sum(((v&m).bit_count()&1)<<i for i,m in enumerate(masks))
R=[];H=[];pts=[]
for p in range(1<<n):
 if p not in SS:
  v=residual(veronese(p));R.append(v);H.append(hash64(v));pts.append(p)
D={}
for i,h in enumerate(H):D.setdefault(h,[]).append(i)
print('support',len(S),'ambient',n,'Veronese rank',len(basis),'outside',len(pts),'single defects',sum(v==0 for v in R),flush=True)
triples=[];checks=0;start=time.time()
for i in range(len(H)):
 for j in range(i+1,len(H)):
  for k in D.get(H[i]^H[j],()):
   if k>j and R[i]^R[j]^R[k]==0:triples.append((pts[i],pts[j],pts[k]))
  checks+=1
print('exact outside triple relations:',len(triples),'pairs checked',checks,'seconds',round(time.time()-start,2))
print('For hypothetical weights the mean unordered difference multiplicity in dimension 14 is:')
for w in [310,322,326,330,334]:print(w,w*(w-1)/(2*((1<<14)-1)),'possible small-collision projections',[(k,w-2*k) for k in [1,3]])