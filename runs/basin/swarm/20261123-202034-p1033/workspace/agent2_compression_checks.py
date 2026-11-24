"""Exact finite check of owner-labelled sunflower compression lemma."""
from itertools import combinations,product
import json

def tau(edges,vertices):
 for r in range(len(vertices)+1):
  for c in combinations(vertices,r):
   if all(set(c)&e for e in edges):return r

def check(t,core_size):
 # Regular cyclic tournament t odd, enough values to produce a sunflower.
 cores=[frozenset(range(i*core_size,(i+1)*core_size)) for i in range(t)]
 owner={v:i for i,X in enumerate(cores) for v in X}
 d=(t-1)//2
 groups=[]
 for i in range(t):
  targets=[j for j in range(t) if 1<=(j-i)%t<=d]
  groups.append([cores[i]|frozenset(p) for p in product(*(cores[j] for j in targets))])
 edges=[e for g in groups for e in g]
 assert all(a&b for a,b in combinations(edges,2))
 assert tau(edges,list(owner))==t
 i=0; petals=[e-cores[i] for e in groups[i]]
 augmented=[frozenset([('v',v) for v in p]+[('c',owner[v]) for v in p]) for p in petals]
 L=d+2
 found=0
 for inds in combinations(range(len(petals)),L):
  kernel=frozenset.intersection(*(augmented[q] for q in inds))
  if any((augmented[a]&augmented[b])!=kernel for a,b in combinations(inds,2)):continue
  K=frozenset(v for typ,v in kernel if typ=='v')
  labels=set(v for typ,v in kernel if typ=='c')-{owner[v] for v in K}
  assert len(K)+len(labels)<=d
  additions=[cores[i]|K|frozenset(p) for p in product(*(cores[j] for j in sorted(labels)))]
  assert all(a&b for a in additions for b in edges)
  assert all(a&b for a,b in combinations(additions,2))
  assert tau(edges+additions,list(owner))==t
  found+=1
 return {'t':t,'d':d,'core_size':core_size,'edges':len(edges),'sunflowers_checked':found}
results=[check(3,3)]
# t=5,d=2,core_size=4: pairwise checks and all covers up to4 on20 vertices manageable.
results.append(check(5,4))
assert all(r['sunflowers_checked']>0 for r in results)
with open('workspace/agent2_compression_checks.json','w') as f:json.dump(results,f,indent=2)
with open('workspace/agent2_compression_checks.py','w') as f:f.write(open('scratchpad.py').read())
print(json.dumps(results,indent=2))
