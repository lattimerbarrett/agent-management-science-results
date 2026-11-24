import sys,json,pathlib,time,collections,numpy as np
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

def trans_basis(bs):
 B={};bb=[]
 for v0 in bs+[1<<i for i in range(14)]:
  v=v0;c=0
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c^(1<<len(bb)));bb.append(v0);break
   v^=B[k][0];c^=B[k][1]
  if len(bb)==14:break
 def enc(p):
  c=0
  while p:
   k=p.bit_length()-1;p^=B[k][0];c^=B[k][1]
  return c
 return enc,bb

def arank(S):
 B={};o=next(iter(S))
 for p in S:
  p^=o
  while p:
   k=p.bit_length()-1
   if k in B:p^=B[k]
   else:B[k]=p;break
 return len(B)

def fwht(F):
 F=F.copy();h=1
 while h<128:
  A=F.reshape(-1,2*h,128);x=A[:,:h,:].copy();y=A[:,h:,:].copy();A[:,:h,:]=x+y;A[:,h:,:]=x-y;h*=2
 return F
D=json.load(open('workspace/agent1_fullspan_predecessors.json'));start=time.time();hits=[];seen=set();stats=collections.Counter();V=None
for ii,d in enumerate(D):
 S=set(d['support'])
 for jj,bb in enumerate(d['basis']):
  enc,BB=trans_basis(bb);M=np.zeros((128,128),dtype=np.int16)
  for p in S:q=enc(p);M[q&127,q>>7]=1
  F=fwht(M);N=M.sum(axis=0);A=(N+F)//2;B=(N-F)//2
  lut=[]
  for p in range(16384):
   v=0
   for j,b in enumerate(BB):
    if p>>j&1:v^=b
   lut.append(v)
  for ell in range(1,128):
   sums=A[ell,:,None]+B[ell,None,:]
   for target in [58,60,62]:
    pairs=np.argwhere(sums==target)
    for b0,b1 in pairs:
     if b0==b1:continue
     H={lut[x|((int(b1) if ((x&ell).bit_count()%2) else int(b0))<<7)] for x in range(128)}
     key=tuple(sorted(H))
     if key in seen:continue
     seen.add(key);G=S^H;assert len(S&H)==target
     rr=arank(G);stats[(target,rr)]+=1
     if rr==14:
      if V is None:V=veronese(14,5)
      cl,rk=closure(G,V);ans={'seed':ii,'comp':jj,'ell':ell,'b0':int(b0),'b1':int(b1),'weight':len(G),'support':sorted(G),'flat':key,'cl5extra':len(cl),'K5':len(G)-rk}
      if cl:ans['closure_witness']=[cl[0][0],cl[0][1]]
      hits.append(ans);print('FULLHIT', {k:v for k,v in ans.items() if k not in ['support','flat']},flush=True)
      json.dump(hits,open('workspace/agent1_rank1switch_hits.json','w'))
      if cl:raise SystemExit('CLOSUREHIT')
 if ii%10==0:print('progress',ii,'stats',dict(stats),'time',time.time()-start,flush=True)
json.dump({'stats':{str(k):v for k,v in stats.items()},'hits':hits,'distinct_flats':len(seen)},open('workspace/agent1_rank1switch_results.json','w'));pathlib.Path('workspace/agent1_rank1switch.py').write_text(pathlib.Path(__file__).read_text());print('DONE',dict(stats),len(hits),time.time()-start)
