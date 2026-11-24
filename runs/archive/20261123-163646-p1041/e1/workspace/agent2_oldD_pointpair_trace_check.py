import itertools,time,json
from pathlib import Path
A=set(range(16));B={x<<4 for x in range(16)};U=A|B
mons=[sum(1<<i for i in I) for k in range(4) for I in itertools.combinations(range(8),k)];cols=[sum((x&m==m)<<j for j,m in enumerate(mons)) for x in range(256)]
bas={}
for x in U:
 v=cols[x]
 while v:
  p=v.bit_length()-1
  if p not in bas:bas[p]=v;break
  v^=bas[p]
order=sorted(bas,reverse=True);out=[]
for x in range(256):
 if x in U:continue
 v=cols[x]
 for p in order:
  if v>>p&1:v^=bas[p]
 out.append((x,v))
print('rankinside',len(bas),'outside',len(out),flush=True)
tab={0:()};hits=[];t=time.time()
for k in range(1,4):
 for inds in itertools.combinations(range(len(out)),k):
  syn=0
  for j in inds:syn^=out[j][1]
  if syn in tab:
   diff=set(inds)^set(tab[syn])
   if diff:hits.append(sorted(diff));break
  tab[syn]=inds
 if hits:break
 print('k',k,'hashes',len(tab),'sec',time.time()-t,flush=True)
print('DONE','hits',hits,'time',time.time()-t,flush=True)
json.dump({'inside_rank':len(bas),'hashes':len(tab),'hits':hits},open('workspace/agent2_oldD_pointpair_trace_result.json','w'))
Path('workspace/agent2_oldD_pointpair_trace_check.py').write_text(Path('scratchpad.py').read_text())
