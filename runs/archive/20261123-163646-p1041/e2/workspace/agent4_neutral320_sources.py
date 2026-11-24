import sys,json,itertools,time,random,numpy as np
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese
s=Path('workspace/agent1_T288_quadgraph_ALLh.py').read_text();exec(s[:s.index('D=json.load')])
D=json.loads(Path('workspace/agent4_T288_quadgraph_P16.json').read_text());S=sorted(D['results'][0]['seeds'][0]['support']);KS=kernel(S,veronese(11,5));assert len(KS)==14
aff=[sum(1<<i for i,p in enumerate(S) if j==-1 or p>>j&1) for j in range(-1,11)];AB={}
for z in aff:insert(AB,z)
extra=[]
for z in KS:
 rr=insert(AB,z)
 if rr:extra.append(rr)
e,f=extra;AC=[0]
for z in aff:AC +=[p^z for p in AC]
we=np.array([(e^z).bit_count() for z in AC],dtype=np.int16);wf=np.array([(f^z).bit_count() for z in AC],dtype=np.int16);wef=np.array([(e^f^z).bit_count() for z in AC],dtype=np.int16);ids=np.arange(4096,dtype=np.uint16);pairs=[]
for lo in range(0,4096,128):
 ii=ids[lo:lo+128];diff=we[ii,None]+wf[None,:]-wef[np.bitwise_xor(ii[:,None],ids[None,:])];pairs +=[(lo+int(i),int(j)) for i,j in np.argwhere(diff==32)]
rng=random.Random(45);rng.shuffle(pairs);out=[];hist={}
for ia,ib in pairs[:100]:
 hh=e^AC[ia];kk=f^AC[ib];F=[]
 for i,p in enumerate(S):
  h=hh>>i&1;k=kk>>i&1
  if h:F.append(p|2048)
  if k:F.append(p|4096)
  if 1^h^k:F.append(p|6144)
 SS=set(F);p0=min(SS);periods=[p^p0 for p in SS if all(x^p^p0 in SS for x in SS)];pd=len(periods).bit_length()-1;hist[pd]=hist.get(pd,0)+1
 if pd<4:out.append({'pair':[ia,ib],'support':sorted(F),'pd':pd})
print('HIST',hist,'retained',len(out));Path('workspace/agent4_neutral320_sources.json').write_text(json.dumps(out));Path('workspace/agent4_neutral320_sources.py').write_text(Path('scratchpad.py').read_text().split('