from sage.all import *
import json,time
from pathlib import Path
S=json.loads(Path('workspace/agent4_boundary256_base32.json').read_text());Gmat=matrix(GF(2),[[1]*32]+[[(x>>j)&1 for x in S] for j in range(7)])
C=LinearCode(Gmat);st=time.time();A=C.permutation_automorphism_group();print('Autorder',A.order(),'seconds',time.time()-st,flush=True)
# Recover affine generators using 8 independent homogenized point columns.
inds=Gmat.pivots();B=Gmat.matrix_from_columns(inds);assert B.is_invertible();gens=[]
for g in A.gens():
 im=[int(g(i+1))-1 for i in inds];T=Gmat.matrix_from_columns(im)*B.inverse()
 assert all(T*Gmat.column(i)==Gmat.column(int(g(i+1))-1) for i in range(32))
 mapping=[];direction=[]
 for x in range(128):
  v=T*vector(GF(2),[1]+[(x>>j)&1 for j in range(7)]);assert v[0]==1;mapping.append(sum(int(v[j+1])<<j for j in range(7)))
  v=T*vector(GF(2),[0]+[(x>>j)&1 for j in range(7)]);assert v[0]==0;direction.append(sum(int(v[j+1])<<j for j in range(7)))
 assert {mapping[x] for x in S}==set(S);gens.append({'points':mapping,'directions':direction})
seen=set();orbits=[]
for v in range(1,128):
 if v in seen:continue
 orb={v};todo=[v]
 while todo:
  x=todo.pop()
  for g in gens:
   y=g['directions'][x]
   if y not in orb:orb.add(y);todo.append(y)
 seen|=orb;orbits.append(sorted(orb))
print('direction orbits',[(len(o),o[0]) for o in orbits],flush=True)
Path('workspace/agent4_boundary32_automorphisms.json').write_text(json.dumps({'order':int(A.order()),'generators':gens,'direction_orbits':orbits}))
