import numpy as np,random,time,math,json,pathlib,sys
rng=random.Random(433456);d=15;N=1<<d;fd=7;size=128;sel=[np.flatnonzero((np.arange(size)>>j)&1) for j in range(fd)]
base=json.loads(pathlib.Path('workspace/agent4_boundary256_base32.json').read_text());E=[p|(r<<7) for p in base for r in range(8)]
def span(b):
 out=[0]
 for x in b:out += [v^x for v in out]
 return np.array(out,dtype=np.int32)
def qual(f):
 S=np.flatnonzero(f);B={}
 for x in S:
  x=int(x)^int(S[0])
  while x:
   j=x.bit_length()-1
   if j in B:x^=B[j]
   else:B[j]=x;break
 qbad=0
 for b in range(d):
  X=S[((S>>b)&1)==0];qbad+=int(f[X^(1<<b)].sum())%2!=1
 return len(B),qbad
st=time.time();trials=0;stats={};best=99;found=[]
for restart in range(10000):
 count=[3,4,5,6,7,8][restart%6];bs=[[1<<i for i in range(fd)] for j in range(count)];offs=[0]*count;pts=[span(b) for b in bs];f=np.zeros(N,dtype=np.uint8);f[E]=1
 for p in pts:f[p]^=1
 w=int(f.sum());score=abs(w-334)
 for step in range(25000):
  trials+=1;j=rng.randrange(count);old=pts[j];basis=bs[j]
  if rng.random()<.92:
   q=rng.randrange(fd);delta=1<<rng.randrange(d)
   if rng.random()<.2:delta^=1<<rng.randrange(d)
   if delta in (old^offs[j]):continue
   inds=sel[q];newhalf=old[inds]^delta;toggle=np.concatenate((old[inds],newhalf));newp=old.copy();newp[inds]=newhalf;newb=basis.copy();newb[q]^=delta;newo=offs[j]
  else:
   delta=1<<rng.randrange(d)
   if delta in (old^offs[j]):continue
   newp=old^delta;toggle=np.concatenate((old,newp));newb=basis;newo=offs[j]^delta
  nw=w+len(toggle)-2*int(f[toggle].sum());ns=abs(nw-334)
  if nw==334:
   f[toggle]^=1;af,qb=qual(f);ns=4*(15-af)+2*qb;stats[af,qb]=stats.get((af,qb),0)+1
   if ns<best:best=ns;print('TARGET334best',af,qb,'trials',trials,'seconds',time.time()-st,flush=True)
   if ns==0:
    support=np.flatnonzero(f).tolist();a=f.copy()
    for bit in range(15):a=a.reshape(-1,2,1<<bit);a[:,1,:]^=a[:,0,:];a=a.reshape(-1)
    deg=max(int(x).bit_count() for x in np.flatnonzero(a));assert deg<=8
    found.append({'support':support,'degree':deg,'rank':af,'qbad':qb});print('FOUND334',af,qb,'DEG',deg,flush=True)
   f[toggle]^=1
  temp=1.2 if step%5000<4000 else 7.
  if ns<=score or rng.random()<math.exp((score-ns)/temp):
   f[toggle]^=1;pts[j]=newp;bs[j]=newb;offs[j]=newo;w=nw;score=ns
  if found or time.time()-st>110:break
 if found or time.time()-st>110:break
R={'trials':trials,'seconds':time.time()-st,'best':best,'stats':{str(k):v for k,v in stats.items()},'found':found};print('DONE',{k:v for k,v in R.items() if k!='found'},flush=True)
pathlib.Path('workspace/agent4_E256_multiflat334.json').write_text(json.dumps(R))
