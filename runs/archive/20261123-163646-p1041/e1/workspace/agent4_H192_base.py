import sys,itertools,time,random,pickle,json
open('workspace/agent4_H192_base.py','w').write(open(__file__).read())
sys.path.insert(0,'workspace');from a1_quadratic_image_api import cols
start=time.time()
A={x for x in range(4096) if x&~63==0};bm=sum(1<<j for j in [0,1,2,3,6,7]);B={x for x in range(4096) if x&~bm==0};pm=sum(1<<j for j in [4,5,8,9,10,11]);P={x for x in range(4096) if x&~pm==0};Q=A^B;U=P|Q
T=[u for u in range(16) if ((u&12)==0)^((u&3)==0)]
H=[(u<<4)|(r&15)|((r>>4)<<8) for u in T for r in range(32)];hs=set(H);N=sum(1<<i for i,x in enumerate(H) if x in P and x in Q);outside=len(U-hs)
print('T',T,'outside',outside,'N',N.bit_count(),'wanted',[w//2-outside-96 for w in [322,326,330,334]],flush=True)
ALL=(1<<192)-1
# degree2restrictionbasis
qmons=[0]+[1<<i for i in range(9)]+[(1<<i)|(1<<j) for i,j in itertools.combinations(range(9),2)]
qb={}
def insert(piv,v):
 while v:
  p=v.bit_length()-1
  if p in piv:v^=piv[p]
  else:piv[p]=v;return True
 return False
for m in qmons:insert(qb,sum(1<<i for i,x in enumerate(H) if x&m==m))
assert len(qb)==41
# imagecoldependence, thenquotientbase
bas={}
for x in U-hs:
 v=cols[x]
 while v:
  p=v.bit_length()-1
  if p not in bas:bas[p]=(v,0);break
  v^=bas[p][0]
extras=[];eb={};qp=sorted(qb,reverse=True)
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
print('imagebase41+extras',len(extras),'sec',time.time()-start,flush=True)
# decoderprecompute
R=[sum(1<<i for i in range(192) if (i%32)>>j&1) for j in range(5)]
FACE=[(i,j,R[i]&R[j],ALL^(R[i]|R[j])) for i,j in itertools.combinations(range(5),2)]
ll=[sum(1<<r for r in range(32) if r>>i&1) for i in range(5)]

def decode(h):
 q=0
 for i,j,mon,mask in FACE:
  si=1<<i;sj=1<<j
  if ((h^(h>>si)^(h>>sj)^(h>>(si+sj)))&mask).bit_count()>24:q^=mon
 z=h^q
 blocks=[(z>>(32*b))&((1<<32)-1) for b in range(6)]
 L=[[int(((v^(v>>(1<<i)))&(((1<<32)-1)^ll[i])).bit_count()>8) for i in range(5)] for v in blocks]
 for bad in range(6):
  coeff=[row[:] for row in L]
  coeff[bad]=[sum(coeff[b][i] for b in range(6) if b!=bad)%2 for i in range(5)]
  e=0
  for b,v in enumerate(blocks):
   pred=0
   for i in range(5):
    if coeff[b][i]:pred^=ll[i]
   err=v^pred
   if err.bit_count()>16:err^=(1<<32)-1
   e|=err<<(32*b)
  if e.bit_count()<=15:return e
 return None
# independentdecodertest
random.seed(0)
for _ in range(1000):
 w=0
 for v in qb.values():
  if random.getrandbits(1):w^=v
 err=sum(1<<i for i in random.sample(range(192),random.randrange(16)))
 assert decode(w^err)==err
print('decoderverified1000',flush=True)
# enumerateglues
goals={w:w//2-outside-96 for w in [322,326,330,334]};found={};hist={};h=N;prev=0
for n in range(1<<len(extras)):
 gray=n^(n>>1)
 if n:h^=extras[(gray^prev).bit_length()-1]
 prev=gray;e=decode(h)
 if e is None:continue
 wt=e.bit_count();hist[wt]=hist.get(wt,0)+1
 for target,needed in goals.items():
  if wt==needed:
   found[target]=(gray,e);print('FOUND',target,wt,n,flush=True);pickle.dump((U,P,Q,H,N,extras,found),open('workspace/agent4_H192_hit.pkl','wb'))
 if len(found)==4:break
print('DONEhist',hist,'found',found.keys(),'sec',time.time()-start,flush=True)
