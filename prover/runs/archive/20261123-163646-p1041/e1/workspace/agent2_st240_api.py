import sys,itertools,random,time,pickle
sys.path.insert(0,'workspace');from a1_quadratic_image_api import cols,decode as dec128
start=time.time();d=3;z=7-d;nint=1<<d;npart=128-nint
H=[r+(a<<d) for a in range(1,1<<z) for r in range(nint)]+[r+(b<<7) for b in range(1,1<<z) for r in range(nint)];HS=set(H);qb={}
def insert(piv,v):
 while v:
  p=v.bit_length()-1
  if p in piv:v^=piv[p]
  else:piv[p]=v;return True
 return False
mons=[0]+[1<<j for j in range(12)]+[(1<<i)|(1<<j) for i,j in itertools.combinations(range(12),2)]
for m in mons:insert(qb,sum(1<<i for i,x in enumerate(H) if x&m==m))
assert len(qb)==51
qp=sorted(qb,reverse=True);ALL=(1<<len(H))-1
rl=[sum(1<<i for i in range(len(H)) if (i%nint)>>j&1) for j in range(d)]
faces=[(i,j,rl[i]&rl[j],ALL^(rl[i]|rl[j])) for i,j in itertools.combinations(range(d),2)]
flatlin=[sum(1<<x for x in range(nint) if x>>i&1) for i in range(d)];afffills=[]
for pat in range(1<<(d+1)):
 v=((1<<nint)-1) if pat&1 else 0
 for i,l in enumerate(flatlin):
  if pat>>(i+1)&1:v^=l
 afffills.append(v)
maskA=(1<<npart)-1

def decode(h):
 qfree=0
 for i,j,mon,mask in faces:
  si=1<<i;sj=1<<j
  if ((h^(h>>si)^(h>>sj)^(h>>(si+sj)))&mask).bit_count()>(64-(1<<(d-1)))//2:
   qfree^=sum(1<<x for x in range(nint) if (x>>i&1) and (x>>j&1))
 a=(h&maskA)<<nint;b=(h>>npart)<<nint
 for aff in afffills:
  fill=qfree^aff
  qa,ea=dec128(a|fill)
  if ea.bit_count()>15:continue
  qb0,eb=dec128(b|fill)
  if eb.bit_count()>15 or (qa&((1<<nint)-1))!=(qb0&((1<<nint)-1)):continue
  e=(ea>>nint)|((eb>>nint)<<npart)
  if e.bit_count()<=15:return e
 return None
random.seed(15)
for _ in range(1000):
 w=0
 for b in qb.values():
  if random.getrandbits(1):w^=b
 err=sum(1<<i for i in random.sample(range(len(H)),random.randrange(16)))
 assert decode(w^err)==err
print('decoderOK',len(H),len(qb),'sec',time.time()-start,flush=True)
def image_H(U):
 bas={}
 for x in U-HS:
  v=cols[x]
  while v:
   p=v.bit_length()-1
   if p not in bas:bas[p]=(v,0);break
   v^=bas[p][0]
 extras=[];eb={}
 for j,x in enumerate(H):
  v=cols[x];img=1<<j
  while v:
   p=v.bit_length()-1
   if p not in bas:bas[p]=(v,img);break
   a,b=bas[p];v^=a;img^=b
  if v:continue
  for p in qp:
   if img>>p&1:img^=qb[p]
  if insert(eb,img):extras.append(img)
 return extras,bas
QCOL=[sum(1<<j for j,m in enumerate(mons) if x&m==m) for x in range(4096)]
def outside_kernel(U,bas):
 V=HS|U;lb={}
 for x in V:insert(lb,QCOL[x])
 E=[]
 for x in range(4096):
  if x in V:continue
  v=QCOL[x]
  while v and v.bit_length()-1 in lb:v^=lb[v.bit_length()-1]
  if not v:E.append(x)
 bb={p:(v,im,0) for p,(v,im) in bas.items()};gens=[]
 for j,x in enumerate(E):
  v=cols[x];im=0;out=1<<j
  while v:
   p=v.bit_length()-1
   if p not in bb:bb[p]=(v,im,out);break
   a,b,c=bb[p];v^=a;im^=b;out^=c
  if not v:gens.append((im,out))
 return E,gens
def span(bs,sh=0):
 ps=[sh]
 for v in bs:ps +=[x^v for x in ps]
 return set(ps)
