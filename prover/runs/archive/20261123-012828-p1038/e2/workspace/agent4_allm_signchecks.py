import sys,math
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_blocks import *
mp.mp.dps=800
out=[]
for m in range(1,13):
 q=math.ceil(96/m);a=m*q
 signs=[]
 for eps in [mp.mpf(1),mp.mpf('0.0001')]:
  blocks=data(m,[-30]*a,[mp.mpf('.6')]*a,0,mp.mpf('.1'),eps,100*eps)
  ss=[]
  for D,tr,A,B in blocks:
   E=reduced(tr,A,B)
   val=mp.re(E[0,0]*E[1,1]-E[0,1]*E[1,0])
   ss.append(int(mp.sign(val)))
  signs.append(ss)
 assert all(s==-1 for s in signs[0]),(m,signs)
 assert all(s==1 for s in signs[1]),(m,signs)
 print('m',m,'a=b',a,'negative at radii1,100 and positive at0.0001,0.01 in all residues',flush=True)
 out.append({'m':m,'a':a,'signs':signs})
import json
Path('workspace/agent4_allm_signchecks.json').write_text(json.dumps(out))
