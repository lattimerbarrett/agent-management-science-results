import os, time, pickle
from collections import Counter
text=open('record/finals.md').read()
code=text.split('```python\n',1)[1].split('```',1)[0]
open('final_code.py','w').write(code)
import final_code as F
for q in (5,7,9,11):
 t=time.time(); D=F.make(q); print('generated',q,time.time()-t,flush=True)
 saved=pickle.load(open(f'agents/agent_1/data{q}.pkl','rb'))
 assert D==saved
 if q<11:
  out=F.enumerate_nests(D)
 else:
  out=pickle.load(open(f'agents/agent_1/raw{q}.pkl','rb'))
 F.check_nests(D,out)
 bad=[s for s in out if not F.hemi(D,s)]
 print(q,'search',Counter(map(len,out)),'bad',Counter(map(len,bad)),flush=True)
 if bad:
  reps,rooted,rootings=F.bad_classes(D,bad)
  print('classes',Counter(map(len,reps)),'rooted',rooted,'rootings',rootings,flush=True)
 print('elapsed',time.time()-t,flush=True)
