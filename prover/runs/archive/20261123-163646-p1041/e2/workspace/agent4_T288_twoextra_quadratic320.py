import sys,itertools,json,time,numpy as np
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure
s=Path('workspace/agent1_T288_quadgraph_ALLh.py').read_text();exec(s[:s.index('D=json.load')])
D=json.loads(Path('workspace/agent4_T288_quadgraph_P16.json').read_text());v10=veronese(10,5);v11=veronese(11,5);v13=veronese(13,5);st=time.time();summary=[];found=[];nseeds=0;nwith=0
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
 for sid,seed in enumerate(res['seeds']):
  for lid,u in enumerate(labels):
   S0=set(seed['support'])
   for i,p in enumerate(T):
    if u>>i&1:S0.symmetric_difference_update([p,p|1024])
   S=sorted(S0);KS=kernel(S,v11)
   if len(KS)!=14:continue
   nseeds+=1;aff=[sum(1<<i for i,p in enumerate(S) if j==-1 or p>>j&1) for j in range(-1,11)];AB={}
   for z in aff:assert insert(AB,z)
   extra=[]
   for z in KS:
    rr=insert(AB,z)
    if rr:extra.append(rr)
   assert len(extra)==2;e,f=extra;AC=[0]
   for z in aff:AC +=[p^z for p in AC]
   we=np.array([(e^z).bit_count() for z in AC],dtype=np.int16);wf=np.array([(f^z).bit_count() for z in AC],dtype=np.int16);wef=np.array([(e^f^z).bit_count() for z in AC],dtype=np.int16);ids=np.arange(4096,dtype=np.uint16)
   pairs=[];total=0
   for lo in range(0,4096,128):
    ii=ids[lo:lo+128];diff=we[ii,None]+wf[None,:]-wef[np.bitwise_xor(ii[:,None],ids[None,:])];hits=np.argwhere(diff==32);total+=len(hits)
    if len(pairs)<4:pairs +=[(lo+int(i),int(j)) for i,j in hits[:4-len(pairs)]]
   if total:
    nwith+=1;print('INTERSECTION16',a,sid,lid,'pairs',total,'nseeds',nseeds,'sec',time.time()-st,flush=True)
   for ia,ib in pairs:
    hh=e^AC[ia];kk=f^AC[ib];F=[]
    for i,p in enumerate(S):
     h=hh>>i&1;k=kk>>i&1
     if h:F.append(p|2048)
     if k:F.append(p|4096)
     if 1^h^k:F.append(p|6144)
    assert len(F)==320;F.sort();KF=kernel(F,v13);gram=sum((x&y).bit_count()%2 for x in KF for y in KF);cl,r=closure(set(F),v13)
    rr={'a':a,'seed':sid,'label':lid,'pair':[ia,ib],'K5':len(KF),'Gram_nonzero':gram,'cl5extras':len(cl),'support':F};found.append(rr)
    print('T320',rr['K5'],gram,len(cl),flush=True)
   summary.append({'a':a,'seed':sid,'label':lid,'pair_count':total})
   if time.time()-st>110:break
  if time.time()-st>110:break
 if time.time()-st>110:break
R={'nseeds':nseeds,'with_pairs':nwith,'summary':summary,'seeds320':found,'seconds':time.time()-st};Path('workspace/agent4_T288_twoextra_quadratic320.json').write_text(json.dumps(R));print('FINISHED nseeds',nseeds,'withpairs',nwith,'320built',len(found),'sec',time.time()-st,flush=True)
