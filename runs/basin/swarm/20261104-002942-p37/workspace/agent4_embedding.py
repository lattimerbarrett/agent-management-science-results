from itertools import combinations,product
from random import Random
from pathlib import Path
rng=Random(4); full=255
A=sum(1<<i for i in [0,1,2,5]); roots=[A,full^A]
partitions=[[[0,1],[2,3,4],[5,6,7]],[[3,4],[0,2,6],[1,5,7]]]
verts=[]
for branch,groups in enumerate(partitions):
 gm=[sum(1<<i for i in g) for g in groups]
 assert all(roots[branch]&g for g in gm)
 assert any(roots[branch]&g==g for g in gm)
 safe=[a for a in range(256) if all(a&g and (full^a)&g for g in gm)]
 pairs=[(a,full^a) for a in safe if a<(full^a)]
 for v in range(10):
  chosen=[]
  for a,b in pairs:
   if a.bit_count()!=4: chosen.append(a if a.bit_count()>4 else b)
   else: chosen.append(rng.choice((a,b)))
  assert all(a&b for a,b in combinations(chosen,2))
  assert all(all(a&g for g in gm) for a in chosen)
  verts.append((branch,chosen,[next(c for c,g in enumerate(groups) if i in g) for i in range(8)]))
N=len(verts)
h=[[0]*N for i in range(8)]
for i in range(8):
 order=sorted(range(N),key=lambda v:tuple([bool(roots[verts[v][0]]&(1<<i))]+[bool(a&(1<<i)) for a in verts[v][1]]))
 for r,v in enumerate(order):h[i][v]=r
for x,y in product(range(N),repeat=2):
 if x!=y: assert {verts[x][2][i] for i in range(8) if h[i][x]>h[i][y]}=={0,1,2}
for tri in combinations(range(N),3):
 for x in tri: assert any(all(h[i][x]>h[i][y] for y in tri if y!=x) for i in range(8))
print('20-vertex tree: all pairs local rainbow; all triples suitable')
P=list(product(range(2),repeat=3))
Q=[(i,) for i in range(N)]+list(combinations(range(N),2))
objects=list(product(P,Q)); K=3
vectors=[]
for p,B in objects:
 vectors.append(tuple(max(K*h[i][v]+p[verts[v][2][i]] for v in B) for i in range(8)))
for a,(p,B) in enumerate(objects):
 for b,(q,C) in enumerate(objects):
  actual=all(x<=y for x,y in zip(p,q)) and set(B)<=set(C)
  geom=all(x<=y for x,y in zip(vectors[a],vectors[b]))
  assert actual==geom
print('Full order embedding checked for',len(objects),'points,',len(objects)**2,'ordered pairs')
