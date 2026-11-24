from sage.all import *
import json,time
from pathlib import Path
D=json.loads(Path('workspace/agent4_boundary32_automorphisms.json').read_text());S=set(json.loads(Path('workspace/agent4_boundary256_base32.json').read_text()));Sym=SymmetricGroup(256)
G=PermutationGroup([Sym([x+1 for x in g['points']]+[x+129 for x in g['directions']]) for g in D['generators']]);print('order',G.order(),flush=True);results=[]
for v in [0,1,2,4,12,32]:
 H=G if v==0 else G.stabilizer(v+129)
 gs=[[int(g(x+1))-1 for x in range(128)] for g in H.gens()];allowed={x for x in range(128) if x not in S and (not v or x^v not in S) and (not v or x<x^v)}
 seen=set();reps=[];orbs=[]
 for p in sorted(allowed):
  if p in seen:continue
  orb={p};todo=[p]
  while todo:
   x=todo.pop()
   for g in gs:
    y=g[x]
    if v:y=min(y,y^v)
    assert y in allowed
    if y not in orb:orb.add(y);todo.append(y)
  seen|=orb;reps.append(p);orbs.append(sorted(orb))
 R={'vbase':v,'staborder':int(H.order()),'point_reps':reps,'point_orbits':orbs};results.append(R)
 print('v',v,'stab',H.order(),'allowed',len(allowed),'pointorbits',[(len(o),o[0]) for o in orbs],flush=True)
Path('workspace/agent4_T280_period_point_orbits.json').write_text(json.dumps(results))
