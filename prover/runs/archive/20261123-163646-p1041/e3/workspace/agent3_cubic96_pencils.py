"""Restricted cubic96 pencil classification experiment. Not general K."""
import itertools,json

def basis(vs):
 D={}
 for v in vs:
  for k in sorted(D,reverse=True):
   if v>>k&1:v^=D[k]
  if v:
   k=v.bit_length()-1
   for j in list(D):
    if D[j]>>k&1:D[j]^=v
   D[k]=v
 return tuple(D[k] for k in sorted(D,reverse=True))

def span(B):
 a=[0]
 for b in B:a +=[x^b for x in a]
 return a

T9=list(itertools.combinations(range(9),3));I9={v:i for i,v in enumerate(T9)}
P9=list(itertools.combinations(range(9),2));J9={v:i for i,v in enumerate(P9)}
T5=list(itertools.combinations(range(5),3));I5={v:i for i,v in enumerate(T5)}
P4=list(itertools.combinations(range(4),2))

def wedge3(a,b,c):
 out=0
 for i in range(9):
  if not a>>i&1:continue
  for j in range(9):
   if j==i or not b>>j&1:continue
   for k in range(9):
    if k not in (i,j) and c>>k&1:out^=1<<I9[tuple(sorted((i,j,k))) ]
 return out

def essrank(f):
 rows=[0]*9
 while f:
  t=f&-f;f^=t;I=T9[t.bit_length()-1]
  for i in I:rows[i]^=1<<J9[tuple(j for j in I if j!=i)]
 return len(basis(rows))

def symp(a,b):
 return (((a&5)<<1)&b).bit_count()%2 ^ (((a&10)>>1)&b).bit_count()%2

def T_representatives():
 allsub={()};todo=[()]
 for B in todo:
  for a in range(1,32):
   C=basis(B+(a,))
   if C not in allsub:allsub.add(C);todo.append(C)
 assert len(allsub)==374
 reps={}
 for T in allsub:
  t=len(T)
  if t==0:continue
  contains=1 in span(T)
  R=basis(v>>1 for v in T)
  rank=len(basis(sum(symp(a,b)<<j for j,b in enumerate(R)) for a in R))
  reps.setdefault((t,contains,rank),T)
 assert len(reps)==11
 return sorted(reps.items())

def verify_T_orbits():
 reps=T_representatives();gens=[]
 for v in range(1,16):
  gens.append((1,)+tuple(((1<<i)^(v if symp(1<<i,v) else 0))<<1 for i in range(4)))
 for j in range(1,5):gens.append(tuple((1<<i)^(1 if i==j else 0) for i in range(5)))
 for g in gens:
  assert wedge3(g[0],g[1],g[2])^wedge3(g[0],g[3],g[4]) == ((1<<I9[(0,1,2)])|(1<<I9[(0,3,4)]))
 def transform(T,g):
  return basis(__import__('functools').reduce(int.__xor__,(g[i] for i in range(5) if v>>i&1),0) for v in T)
 seen=set()
 for key,T in reps:
  orbit={T};todo=[T]
  for A in todo:
   for g in gens:
    B=transform(A,g)
    if B not in orbit:orbit.add(B);todo.append(B)
  assert not(seen&orbit)
  seen|=orbit
 assert len(seen)==373
 return True

PLANES={}
for a,b in itertools.combinations(range(1,16),2):
 q=sum((((a>>i&1)&(b>>j&1))^((a>>j&1)&(b>>i&1)))<<k for k,(i,j) in enumerate(P4))
 PLANES.setdefault(q,(a,b))
assert len(PLANES)==35
QDECOMP={}
for q in range(1,64):
 if q in PLANES:continue
 for p in PLANES:
  if q^p in PLANES:QDECOMP[q]=PLANES[p]+PLANES[q^p];break
assert len(QDECOMP)==28

def smallword(f):
 # f is a nondecomposable3-form in five variables.
 lam=None
 for a in range(1,32):
  out=0
  for k,I in enumerate(T5):
   if not f>>k&1:continue
   for i in range(5):
    if i not in I and a>>i&1:out^=1<<list(itertools.combinations(range(5),4)).index(tuple(sorted(I+(i,))))
  if out==0:
   assert lam is None
   lam=a
 assert lam is not None
 pivot=(lam&-lam).bit_length()-1;others=[i for i in range(5) if i!=pivot]
 q=0
 for k,(i,j) in enumerate(P4):
  if f>>I5[tuple(sorted((pivot,others[i],others[j])))]&1:q^=1<<k
 assert q in QDECOMP
 u,v,s,t=QDECOMP[q]
 word=0
 for x in range(32):
  z=sum(((x>>i)&1)<<j for j,i in enumerate(others))
  val=((lam&x).bit_count()%2)*((((u&z).bit_count()%2)*((v&z).bit_count()%2))^(((s&z).bit_count()%2)*((t&z).bit_count()%2)))
  word|=val<<x
 assert word.bit_count()==6
 return word

def embed_word(w,W):
 out=0
 for x in range(512):
  y=sum(((a&x).bit_count()%2)<<i for i,a in enumerate(W))
  if w>>y&1:out|=1<<x
 return out

def shiftword(w,a):return sum(((w>>(x^a))&1)<<x for x in range(32))

def enumerate_pencils():
 alpha=(1<<I9[(0,1,2)])|(1<<I9[(0,3,4)])
 u=sum(((((x>>0)&1)*((((x>>1)&1)*((x>>2)&1))^(((x>>3)&1)*((x>>4)&1)))))<<x for x in range(512))
 assert u.bit_count()==96
 verify_T_orbits()
 # Exhaust all quadratic lowerparts for one special cubic top on five variables.
 smallalpha=(1<<I5[(0,1,2)])|(1<<I5[(0,3,4)])
 p0=smallword(smallalpha)
 lowbasis=[sum((x&sum(1<<i for i in I)==sum(1<<i for i in I))<<x for x in range(32)) for d in range(3) for I in itertools.combinations(range(5),d)]
 actual={p0^q for q in span(lowbasis) if (p0^q).bit_count()==6}
 assert actual=={shiftword(p0,a) for a in range(32)} and len(actual)==32
 models=[];counts=[]
 for key,T in T_representatives():
  t=len(T);W=T+tuple(1<<(5+i) for i in range(5-t))
  assert len(W)==5
  F=[wedge3(W[i],W[j],W[k]) for i,j,k in T5]
  embedded=span(F);cnt=0;cntwords=0
  assert sum(essrank(beta)==5 for beta in embedded)==868
  for small,beta in enumerate(embedded):
   if essrank(beta)!=5 or essrank(alpha^beta)!=5:continue
   cnt+=1
   b=smallword(small)
   for a in range(32):
    v=embed_word(shiftword(b,a),W)
    if (u^v).bit_count()==96:
     cntwords+=1;models.append((key,T,small,a,hex(v)))
  counts.append((key,cnt,cntwords))
  print(key,cnt,cntwords,flush=True)
 out=dict(counts=counts,models=models,u=hex(u))
 with open('workspace/agent3_cubic96_pencils.json','w') as f:json.dump(out,f)
 print('MODELS',len(models))
 return out
if __name__=='__main__':enumerate_pencils()
