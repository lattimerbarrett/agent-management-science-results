from itertools import combinations

def bits(f):
 while f:
  b=f&-f;yield b;f^=b

def verify_uniform(fs,k,c):
 """Exact independent verifier. No maximal-face O(f^2) comparisons.
 Uniform facets represented by integer masks; certificates use simplex/shed.
 Deletes facets in place along each deletion branch, updating ridge counts.
 All σ-avoiding faces are covered iff every removed F-v (v in σ) remains
 covered by some surviving full facet. Links are computed independently.
 """
 stack=[(set(fs),c)];nodes=0;facets_seen=0
 while stack:
  F,c=stack.pop();assert F
  p=next(iter(F)).bit_count();assert all(f.bit_count()==p for f in F)
  counts={}
  for f in F:
   for v in bits(f):
    r=f^v;counts[r]=counts.get(r,0)+1
  while True:
   nodes+=1
   if c[0]=='simplex':
    assert F=={c[1]}
    break
   assert c[0]=='shed' and len(c)==4
   _,s,cd,cl=c
   assert s and s.bit_count()<=k+1 and s.bit_count()<=p
   removed=[f for f in F if f&s==s];assert removed
   L={f^s for f in removed};facets_seen+=len(removed)
   for f in removed:
    F.remove(f)
    for v in bits(f):counts[f^v]-=1
   assert F
   for f in removed:
    for v in bits(s):assert counts.get(f^v,0)>0
   stack.append((L,cl))
   c=cd
 return {'nodes':nodes,'removed_facet_visits':facets_seen}
