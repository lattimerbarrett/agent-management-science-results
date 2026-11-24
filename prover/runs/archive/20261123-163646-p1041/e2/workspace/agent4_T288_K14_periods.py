import sys,json,time,collections
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese
s=Path('workspace/agent1_T288_quadgraph_ALLh.py').read_text();exec(s[:s.index('D=json.load')])
D=json.loads(Path('workspace/agent4_T288_quadgraph_P16.json').read_text());v10=veronese(10,5);v11=veronese(11,5);hist=collections.Counter();ct=0;st=time.time()
for res in D['results']:
 a=res['a'];T=[]
 for x in range(256):
  q1=(x&1)*(x>>1&1);q2=((x&1)*(x>>2&1))^((x>>1&1)*(x>>3&1) if a==4 else 0);T.append(x|(q1<<8)|(q2<<9))
 K=kernel(T,v10);B={}
 for j in range(-1,10):insert(B,sum(1<<i for i,p in enumerate(T) if j==-1 or p>>j&1))
 ex=[]
 for u in K:
  r=insert(B,u)
  if r:ex.append(r)
 labels=[0]
 for u in ex:labels +=[z^u for z in labels]
 for seed in res['seeds']:
  for u in labels:
   SS=set(seed['support'])
   for i,p in enumerate(T):
    if u>>i&1:SS.symmetric_difference_update([p,p|1024])
   S=sorted(SS);KS=kernel(S,v11)
   if len(KS)!=14:continue
   p0=S[0];periods=[p^p0 for p in S if all((x^p^p0) in SS for x in S)];pd=len(periods).bit_length()-1
   assert len(periods)==1<<pd;hist[pd]+=1;ct+=1
assert ct==288 and hist=={4:288}
Path('workspace/agent4_T288_K14_periods.json').write_text(json.dumps({'count':ct,'period_dim_hist':dict(hist),'seconds':time.time()-st}))
print('COMPLETE',ct,hist,time.time()-st)
