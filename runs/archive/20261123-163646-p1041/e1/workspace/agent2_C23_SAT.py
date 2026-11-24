import pickle,itertools,time,functools,json
from z3 import *
from pathlib import Path
D=pickle.load(open('workspace/agent2_C23_data.pkl','rb'));H=D['H'];b=[Bool('b'+str(i)) for i in range(720)]
s=Solver();s.set(timeout=120000)
for row in H:
 inds=[i for i in range(720) if row>>i&1]
 s.add(Not(functools.reduce(Xor,[b[i] for i in inds])))
# Enforce necessary slice XOR=0, since C23 invariant RM4,11 min>400.
for j in range(90):s.add(Not(functools.reduce(Xor,[b[j+90*k] for k in range(8)])))
fixed=[b[90*k] for k in range(8)];high=[b[j+90*k] for k in range(8) for j in range(1,90)]
s.add(PbEq([(v,1) for v in high],14))
for low in (0,4,8):
 s.push();s.add(PbEq([(v,1) for v in fixed],low));t=time.time();r=s.check();print('TARGET',322+low,r,time.time()-t,flush=True)
 if r==sat:
  m=s.model();inds=[i for i in range(720) if is_true(m.eval(b[i]))]
  print('HIT',inds,flush=True);json.dump({'weight':322+low,'ones':inds},open('workspace/agent2_C23_hit.json','w'))
 s.pop()
Path('workspace/agent2_C23_SAT.py').write_text(Path('scratchpad.py').read_text())
