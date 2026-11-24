"""Explicit edge-fill then boundary-fill completion in dimension two, k>=1."""
from itertools import combinations
from agent3_checker import subsets,verify
from agent2_boundary_fill import fill_boundary

def rank3_completion(facets,k,cert,ambient=None):
 assert k>=1
 cur=set(facets);assert all(F.bit_count()==3 for F in cur)
 verify(tuple(sorted(cur)),k,cert)
 U=0
 for F in cur:U|=F
 ambient=U if ambient is None else ambient
 assert U&ambient==U
 out=[]
 def append(F,c):
  nonlocal cert
  assert F not in cur
  cur.add(F);cert=c;verify(tuple(sorted(cur)),k,cert);out.append((F,cert))
 # Introduce any ambient ghost vertices through a new triangle.
 for v in subsets(ambient&~U,1):
  edge=next(subsets(next(iter(cur)),2))
  append(v|edge,('shed',v,cert,('simplex',edge)));U|=v
 while True:
  edges={e for F in cur for e in subsets(F,2)}
  missing=set(subsets(U,2))-edges
  if not missing:break
  triple=None
  for b in subsets(U,1):
   nbr=[a for a in subsets(U&~b,1) if a|b in edges]
   for a,c in combinations(nbr,2):
    if a|c not in edges:triple=(a,b,c);break
   if triple:break
  assert triple,'Graph must be connected for induced-path completion.'
  a,b,c=triple
  append(a|b|c,('shed',a|c,cert,('simplex',b)))
 for F in subsets(U,3):
  if F not in cur:append(F,fill_boundary(tuple(sorted(cur)),k,cert,F))
 assert cur==set(subsets(U,3))
 return tuple(out)
