import json
from itertools import combinations
from collections import Counter

def check():
 old=[tuple(t) for t in json.load(open('workspace/agent3_2core_order.json'))]
 T=set(old)
 assert len(T)==28
 assert set(e for t in T for e in combinations(t,2))==set(combinations(range(9),2))
 assert all(sum(t in T for t in combinations(q,3))<=2 for q in combinations(range(9),4))
 # Verify original PURE shelling, including all old lower faces.
 oldfaces=[set() for _ in range(3)]
 for i,t in enumerate(old):
  if i:
   edges=[e for e in combinations(t,2) if e in oldfaces[2]]
   assert edges
   for v in t:
    assert (v,) not in oldfaces[1] or any(v in e for e in edges)
  for q in [1,2]:oldfaces[q].update(combinations(t,q))
 m=4;r=4
 order=[];present=set();oldedges=set();faces=[set() for _ in range(4)]
 for it,t in enumerate(old):
  C=[m*v+j for v in t for j in range(m)]
  if it:
   R=[v for v in t if tuple(x for x in t if x!=v) in oldedges]
   assert 0<len(R)<3
   P={m*v+j for v in t if v not in R for j in range(m)}
  else:P=set(C)
  new=[s for s in combinations(C,r) if s not in present]
  new.sort(key=lambda s:(-len(set(s)&P),tuple(x for x in s if x not in P),tuple(x for x in s if x in P)))
  for s in new:
   if order:
    tris=[t for t in combinations(s,3) if t in faces[3]]
    assert tris,('no old triangle',it,s)
    for q in [1,2]:
     for f in combinations(s,q):
      assert f not in faces[q] or any(set(f)<=set(t) for t in tris),('BAD',it,s,f,tris)
   present.add(s);order.append(s)
   for q in [1,2,3]:faces[q].update(combinations(s,q))
  oldedges.update(combinations(t,2))
 assert len(faces[2])==630
 assert len(order)==10521
 missing=0
 for f in combinations(range(36),4):
  if f in present:continue
  missing+=1
  tri=[t for t in combinations(f,3) if t in faces[3]]
  assert not all(any(set(e)<=set(t) for t in tri) for e in combinations(f,2)),('ADDABLE',f)
 return len(T),len(order),len(faces[3]),missing

if __name__=='__main__':print(check())
