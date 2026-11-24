import itertools,json,time

def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  a<<=1
  if a&8:a^=11
  b>>=1
 return c

def inv(a):
 return next(b for b in range(1,8) if mul(a,b)==1)
pts=[]
for a in itertools.product(range(8),repeat=3):
 if not any(a):continue
 p=next(x for x in a if x)
 if p==1:pts.append(a)
assert len(pts)==73
triples=list(itertools.combinations(range(9),3))
orbits=[];vectors=[]
for a in pts:
 S=[sum(mul(l,a[i])<<(3*i) for i in range(3)) for l in range(1,8)];orbits.append(S)
 v=0
 for j,t in enumerate(triples):
  mask=sum(1<<i for i in t)
  if sum(x&mask==mask for x in S)%2:v|=1<<j
 vectors.append(v)
assert len(set(vectors))==73
pairs={}
for i,j in itertools.combinations(range(73),2):pairs.setdefault(vectors[i]^vectors[j],[]).append((i,j))
def rank(vs):
 b={}
 for v in vs:
  while v:
   j=v.bit_length()-1
   if j in b:v^=b[j]
   else:b[j]=v;break
 return len(b)
relations=[]
for ijk in itertools.combinations(range(73),3):
 v=vectors[ijk[0]]^vectors[ijk[1]]^vectors[ijk[2]]
 for ab in pairs.get(v,[]):
  if set(ab)&set(ijk):continue
  ids=tuple(sorted(ab+ijk))
  if ids in relations:continue
  relations.append(ids)
  if rank([s for i in ids for s in orbits[i]])==9:
   S=[]
   for j,i in enumerate(ids):
    label=0 if j<2 else 1<<(j-2)
    S.extend(x|(label<<9) for x in orbits[i])
   S.extend((1<<i)<<9 for i in range(3));assert len(set(S))==38
   # verify all moments through degree3 and affine rank12
   for d in range(4):
    for inds in itertools.combinations(range(12),d):
     m=sum(1<<i for i in inds);assert sum(x&m==m for x in S)%2==0
   p=S[0];assert rank([x^p for x in S])==12
   json.dump({'projective_points':[pts[i] for i in ids],'support':S},open('workspace/agent2_T38_C7_HIT.json','w'));print('VERIFIED HIT',ids,[pts[i] for i in ids]);raise SystemExit
print('all five-relations',len(relations),relations[:20])
from pathlib import Path
Path('workspace/agent2_T38_C7_search.py').write_text(Path(__file__).read_text())
