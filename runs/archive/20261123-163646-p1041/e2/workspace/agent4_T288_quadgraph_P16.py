import sys,itertools,json,time
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure
s=Path('workspace/agent1_boundary272_relatives.py').read_text();exec(s[:s.index('raw=json.load')])
v10=veronese(10,5);v11=veronese(11,5);res=[];st=time.time()
for a in [3,4]:
 def qs(x):return ((x&1)*(x>>1&1),((x&1)*(x>>2&1))^((x>>1&1)*(x>>3&1) if a==4 else 0))
 T=[]
 for x in range(256):
  q1,q2=qs(x);T.append(x|(q1<<8)|(q2<<9))
 B=basis([v10[p] for p in T]);hist={};cnts={};seeds=[]
 for d in range(a+1):
  total=aff=valid=0
  for Q in flats(a,d):
   total+=1
   for eps in [1,2,3]:
    P=[]
    for p in Q:
     for r in range(1<<(4-d)):
      x=p|(r<<a);q1,q2=qs(x);P.append(x|((q1^(eps&1))<<8)|((q2^(eps>>1))<<9))
    assert len(P)==16
    if len(basis([(p^P[0]) for p in P]))!=4:continue
    aff+=1;z=0
    for p in P:z^=v10[p]
    rem,co=red(z,B)
    if rem:continue
    valid+=1;H=P+[p for j,p in enumerate(T) if co>>j&1]
    F=sorted(set(H)^set(p|1024 for p in H)^set(p|1024 for p in T));assert len(F)==288
    af=len(basis([p^F[0] for p in F]));K=288-len(basis([v11[p] for p in F]));hist[af,K]=hist.get((af,K),0)+1
    seeds.append({'a':a,'d':d,'Q':Q,'eps':eps,'support':F,'affrank':af,'K5':K})
  cnts[d]={'totalQ':total,'affine_candidates':aff,'valid':valid}
  print('a,d',a,d,cnts[d], 'hist',hist,'sec',time.time()-st,flush=True)
 res.append({'a':a,'counts':cnts,'hist':{str(k):v for k,v in hist.items()},'seeds':seeds})
Path('workspace/agent4_T288_quadgraph_P16.json').write_text(json.dumps({'results':res,'seconds':time.time()-st}))
print('FINISHED',sum(len(r['seeds']) for r in res),flush=True)
