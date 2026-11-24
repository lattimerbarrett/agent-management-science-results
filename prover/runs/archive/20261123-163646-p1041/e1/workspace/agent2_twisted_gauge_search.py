import numpy as np,random,time,json,itertools
from pathlib import Path
random.seed(285277)
xx=np.array([[int(x>>i&1) for x in range(64)] for i in range(6)],dtype=np.int16)
mon=[np.ones(64,dtype=np.int16)]+[xx[i] for i in range(6)]+[xx[i]*xx[j] for i in range(6) for j in range(i)]
a=xx[0]*xx[1]*xx[2];b=xx[3]*xx[4]*xx[5]
def quad(c):
 q=np.zeros(64,dtype=np.int16)
 for i in range(22):
  if c>>i&1:q^=mon[i]
 return q
def samplequad():
 if random.random()<.5:return random.randrange(1<<22)
 c=0
 for _ in range(random.randrange(1,8)):c^=1<<random.randrange(22)
 return c
flipcache={};hits=[];t0=time.time();minimum=99999
for trial in range(2000):
 co=[samplequad() for _ in range(4)];L=[a,b,quad(co[0]),quad(co[1])];R=[a,b,quad(co[2]),quad(co[3])]
 li=sum((L[i].astype(np.int64)<<i) for i in range(4));ri=sum((R[i].astype(np.int64)<<i) for i in range(4))
 pl=np.bincount(li,minlength=16);pr=np.bincount(ri,minlength=16);lis=np.where(pl>0)[0];ris=np.where(pr>0)[0];nl=pl[lis];nr=pr[ris]
 M=np.zeros((4,4),dtype=np.int16);M[0,0]=M[1,1]=1
 for _ in range(random.randrange(1,9)):
  i,j=random.choice([(i,j) for i in range(4) for j in range(4) if i>=2 or j>=2]);M[i,j]^=1
 H=np.array([[sum(((i>>k)&1)*int(M[k,l])*((j>>l)&1) for k in range(4) for l in range(4))%2 for j in ris] for i in lis],dtype=np.int16)
 m=len(ris)
 if m not in flipcache:flipcache[m]=np.array([[int(x>>i&1) for i in range(m)] for x in range(1<<m)],dtype=np.int16)
 B=flipcache[m];S=(H@nr)[None,:]+(B*nr)@(1-2*H).T;parity=(B@nr)%2
 for correction in range(-1,m):
  if correction<0:sel=np.where(parity==0)[0];C=B[sel].astype(np.int64)*nr;V=S[sel]
  else:
   sel=np.where(parity==1)[0];C=B[sel].astype(np.int64)*nr;delta=1-2*B[sel,correction];C[:,correction]+=delta;V=S[sel]+delta[:,None]*(1-2*H[:,correction])[None,:]
  u=(V>32).astype(np.int16);ucount=u*nl;cost=np.minimum(V,64-V)@nl;up=(ucount.sum(axis=1))%2
  penalty=np.abs(64-2*V);where=penalty.argmin(axis=1);cost+=up*penalty[np.arange(len(sel)),where]
  if len(cost):minimum=min(minimum,int(cost.min()))
  # For low-cost column patterns enumerate ALL arbitrary row-flip counts
  # by exact subset-sum of the 64 individual majority penalties.
  raw=np.minimum(V,64-V)@nl
  for jj0 in np.where(raw<=206)[0]:
   lim=206-int(raw[jj0]);masklim=(1<<(lim+1))-1;de,do=1,0;history=[(de,do)];pvals=[]
   for it,nit in enumerate(nl):
    for nt in range(int(nit)):
     pv=int(penalty[jj0,it]);pvals.append((pv,it));de,do=(de|(do<<pv))&masklim,(do|(de<<pv))&masklim;history.append((de,do))
   par=int(up[jj0]);bits=(de,do)[par]
   for target in [194,198,202,206]:
    diff=target-int(raw[jj0])
    if diff<0 or not (bits>>diff&1):continue
    rct=(u[jj0]*nl).copy();need=diff;cp=par
    for kk in range(63,-1,-1):
     if history[kk][cp]>>need&1:continue
     pv,it=pvals[kk];need-=pv;cp^=1;rct[it]+=1-2*u[jj0,it]
    assert need==0 and cp==0
    hit={'weight':target,'coeffs':co,'M':M.tolist(),'rowtypes':lis.tolist(),'coltypes':ris.tolist(),'rowcounts':rct.tolist(),'colcounts':C[jj0].tolist()};hits.append(hit);print('HITDP',hit,flush=True);break
   if hits:break
  if hits:break
  for target in [194,198,202,206]:
   inds=np.where(cost==target)[0]
   if len(inds):
    j=int(inds[0]);rct=ucount[j].copy();jj=int(where[j])
    if up[j]:rct[jj]+=1-2*u[j,jj]
    hit={'weight':target,'coeffs':co,'M':M.tolist(),'rowtypes':lis.tolist(),'coltypes':ris.tolist(),'rowcounts':rct.tolist(),'colcounts':C[j].tolist()};hits.append(hit);print('HIT',hit,flush=True);break
  if hits:break
 if hits:break
 if trial%100==0:print('progress',trial,'minimum',minimum,'seconds',time.time()-t0,flush=True)
print('DONE',minimum,hits,'time',time.time()-t0,flush=True)
json.dump(hits,open('workspace/agent2_twisted_gauge_hits.json','w'))
Path('workspace/agent2_twisted_gauge_search.py').write_text(Path('scratchpad.py').read_text())
