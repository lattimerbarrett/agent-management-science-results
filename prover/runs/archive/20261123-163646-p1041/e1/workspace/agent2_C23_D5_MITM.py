import pickle,itertools,time,functools,json
from z3 import *
D=pickle.load(open('workspace/agent2_C23_data.pkl','rb'));ids=D['ids'];rows=[1<<ids[x] for x in range(2048)]
for i in range(11):
 for x in range(2048):
  if x>>i&1:rows[x]^=rows[x^(1<<i)]
bas={}
for x,row in enumerate(rows):
 if x.bit_count()<=5:continue
 while row:
  p=row.bit_length()-1
  if p not in bas:bas[p]=row;break
  row^=bas[p]
H=list(bas.values());cols=[sum(((r>>i)&1)<<j for j,r in enumerate(H)) for i in range(90)];tab={0:0};hits=[];t=time.time()
for k in range(1,4):
 for inds in itertools.combinations(range(1,90),k):
  syn=0;mask=0
  for i in inds:syn^=cols[i];mask^=1<<i
  if syn in tab and tab[syn]!=mask:hits.append(mask^tab[syn])
  if syn^cols[0] in tab:hits.append(mask^tab[syn^cols[0]]^1)
  tab[syn]=mask
print('triples',len(tab),'hits',len(hits),'time',time.time()-t,flush=True)
for inds in itertools.combinations(range(1,90),4):
 syn=cols[inds[0]]^cols[inds[1]]^cols[inds[2]]^cols[inds[3]]
 for bit in (0,1):
  target=syn^(cols[0] if bit else 0)
  if target in tab:
   mask=sum(1<<i for i in inds)^tab[target]^bit
   if mask:hits.append(mask)
print('DONE','hits',len(set(hits)),'time',time.time()-t,flush=True)
if hits:print([([i for i in range(90) if mask>>i&1]) for mask in set(hits)][:20],flush=True)
from pathlib import Path
Path('workspace/agent2_C23_D5_MITM.py').write_text(Path('scratchpad.py').read_text())
