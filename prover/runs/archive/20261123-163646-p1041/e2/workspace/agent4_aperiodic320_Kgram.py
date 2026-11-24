import sys,json,time,random,math,numpy as np
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese
rng=random.Random(320506);m=12;fd=7;sz=128;N=4096;sel=[np.flatnonzero((np.arange(sz)>>j)&1) for j in range(fd)];V=veronese(m,5)
def span(bs):
 out=[0]
 for b in bs:out +=[v^b for v in out]
 return np.array(out,dtype=np.int32)
def perioddim(S):
 SS=set(S);p0=S[0];periods=[p^p0 for p in S if all(x^p^p0 in SS for x in S)];assert len(periods)&(len(periods)-1)==0
 return len(periods).bit_length()-1

def kernel(S):
 B={};K=[]
 for i,p in enumerate(S):
  v=V[p];c=1<<i
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j][0];c^=B[j][1]
   else:B[j]=(v,c);break
  if not v:K.append(c)
 return K
st=time.time();trials=0;cache={};pstats={};kstats={};found=[];bestp=99
for restart in range(10000):
 count=[3,4,5,6,8,10,12][restart%7];bs=[[1<<i for i in range(fd)] for j in range(count)];off=[0]*count;pts=[span(b) for b in bs];f=np.zeros(N,dtype=np.uint8)
 for p in pts:f[p]^=1
 w=int(f.sum());score=abs(w-320)
 for step in range(25000):
  trials+=1;j=rng.randrange(count);old=pts[j]
  if rng.random()<.92:
   q=rng.randrange(fd);delta=1<<rng.randrange(m)
   if rng.random()<.2:delta^=1<<rng.randrange(m)
   if delta in old^off[j]:continue
   inds=sel[q];half=old[inds]^delta;newp=old.copy();newp[inds]=half;toggle=np.concatenate((old[inds],half));nb=bs[j].copy();nb[q]^=delta;no=off[j]
  else:
   delta=1<<rng.randrange(m)
   if delta in old^off[j]:continue
   newp=old^delta;toggle=np.concatenate((old,newp));nb=bs[j];no=off[j]^delta
  nw=w+len(toggle)-2*int(f[toggle].sum());ns=abs(nw-320)
  if nw==320:
   f[toggle]^=1;key=np.packbits(f).tobytes();info=cache.get(key)
   if info is None:
    S=np.flatnonzero(f).tolist();pd=perioddim(S);pstats[pd]=pstats.get(pd,0)+1;kk=0
    if pd<bestp:bestp=pd;print('NEWLOWPERIOD',pd,'trials',trials,'sec',time.time()-st,flush=True)
    if pd==0:
     K=kernel(S);kk=len(K);nz=any((u&v).bit_count()%2 for i,u in enumerate(K) for v in K[i+1:]);kstats[kk]=kstats.get(kk,0)+1
     if nz:
      a=f.copy()
      for bit in range(m):a=a.reshape(-1,2,1<<bit);a[:,1,:]^=a[:,0,:];a=a.reshape(-1)
      deg=max(int(x).bit_count() for x in np.flatnonzero(a));assert deg<=5
      found.append({'support':S,'K5':kk,'kernel':K,'degree':deg});print('NONSELF320FOUND K',kk,flush=True)
    info=(pd,kk);cache[key]=info
   pd,kk=info;ns=5*pd+(max(0,15-kk)*2 if pd==0 else 0);f[toggle]^=1
  temp=1.5 if step%5000<3500 else 15.
  if ns<=score or rng.random()<math.exp((score-ns)/temp):
   f[toggle]^=1;pts[j]=newp;bs[j]=nb;off[j]=no;w=nw;score=ns
  if found or time.time()-st>110:break
 if found or time.time()-st>110:break
R={'trials':trials,'seconds':time.time()-st,'unique320':len(cache),'period_hist':pstats,'aperiodicK_hist':kstats,'found':found};print('DONE',{k:v for k,v in R.items() if k!='found'},flush=True)
Path('workspace/agent4_aperiodic320_Kgram.json').write_text(json.dumps(R))
