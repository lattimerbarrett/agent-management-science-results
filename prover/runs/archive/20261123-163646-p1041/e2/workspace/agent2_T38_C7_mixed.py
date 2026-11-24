import itertools,json
from pathlib import Path

def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  a<<=1
  if a&8:a^=11
  b>>=1
 return c

def pow3(a):return mul(mul(a,a),a)
def rank(vs):
 b={}
 for v in vs:
  while v:
   j=v.bit_length()-1
   if j in b:v^=b[j]
   else:b[j]=v;break
 return len(b)
for types in [(1,1,1),(1,1,3)]:
 orbits=[];seen=set()
 for x in range(1,512):
  if x in seen:continue
  a=[(x>>(3*i))&7 for i in range(3)]
  orb=[sum(mul(l if t==1 else pow3(l),a[i])<<(3*i) for i,t in enumerate(types)) for l in range(1,8)]
  assert len(set(orb))==7;seen.update(orb);orbits.append(orb)
 assert len(orbits)==73
 masks=[sum(1<<i for i in inds) for d in range(1,4) for inds in itertools.combinations(range(9),d)]
 vectors=[sum(1<<j for j,mask in enumerate(masks) if sum(x&mask==mask for x in orb)%2) for orb in orbits]
 secondmask=(1<<(9+36))-1
 pairs={}
 for a,b in itertools.combinations(range(73),2):pairs.setdefault(vectors[a]^vectors[b],[]).append((a,b))
 rels=set();hits=0
 for abc in itertools.combinations(range(73),3):
  for de in pairs.get(vectors[abc[0]]^vectors[abc[1]]^vectors[abc[2]],[]):
   if set(abc)&set(de):continue
   ids=tuple(sorted(abc+de))
   if ids in rels:continue
   rels.add(ids)
   if rank([x for i in ids for x in orbits[i]])<9:continue
   for zero in itertools.combinations(ids,2):
    rest=[i for i in ids if i not in zero]
    if any(vectors[i]&secondmask for i in rest):continue
    S=[x for i in zero for x in orbits[i]]
    for j,i in enumerate(rest):S.extend(x|(1<<(9+j)) for x in orbits[i])
    S.extend(1<<(9+j) for j in range(3));assert len(set(S))==38
    for d in range(4):
     for inds in itertools.combinations(range(12),d):
      mask=sum(1<<i for i in inds);assert sum(x&mask==mask for x in S)%2==0
    p=S[0];assert rank([x^p for x in S])==12
    print('VERIFIED HIT',types,ids,zero);json.dump({'types':types,'support':S},open('workspace/agent2_T38_C7_mixed_HIT.json','w'));raise SystemExit
 print('types',types,'five moment relations',len(rels))
Path('workspace/agent2_T38_C7_mixed.py').write_text(Path(__file__).read_text())
