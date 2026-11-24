import itertools,json
V=range(7);pairs=list(itertools.combinations(V,2));quads=list(itertools.combinations(V,4));lookup={s:i for i,s in enumerate(quads)}
def rank(cols):
 basis={}
 for v in cols:
  while v:
   j=v.bit_length()-1
   if j in basis:v^=basis[j]
   else:basis[j]=v;break
 return len(basis)
for r in (2,4,6):
 q=[(i,i+1) for i in range(0,r,2)];cols=[]
 for p in pairs:
  v=0
  for pp in q:
   if not(set(p)&set(pp)):v^=1<<lookup[tuple(sorted(p+pp))]
  cols.append(v)
 print('rank(q)',r,'rankLq',rank(cols),'ker',len(pairs)-rank(cols))
 assert len(pairs)-rank(cols)=={2:11,4:5,6:1}[r]
print('All exterior-map rank checks passed')
from pathlib import Path
Path('workspace/agent2_exterior_rank.py').write_text(Path(__file__).read_text())
