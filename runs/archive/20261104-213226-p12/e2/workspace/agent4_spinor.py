import itertools, json, random, time, numpy as np
from math import prod
P=10007
# Extra GL8 scalar weight t, repeated in eight linear equations.

def mons(n, weights, cap=None):
 if not weights:
  if n==0:yield ()
  return
 m=n//weights[0]
 if cap and cap[0] is not None:m=min(m,cap[0])
 for a in range(m+1):
  for tail in mons(n-a*weights[0],weights[1:],cap[1:] if cap else None):yield (a,)+tail
src=list(mons(11,[1,2,3,4,5,1]+list(range(1,9))+[1],[None]*14+[8]))
tgt=list(mons(12,[1,2,4,6,8,5]+list(range(1,9))))
srcarr=np.array(src,dtype=np.int64);tgtarr=np.array(tgt,dtype=np.int64)
def evmon(vals,arr):
 out=np.ones(len(arr),dtype=np.int64)
 for j,v in enumerate(vals):
  pp=np.array([pow(int(v),k,P) for k in range(13)],dtype=np.int64)
  out=out*pp[arr[:,j]]%P
 return out
print('source',len(src),'target',len(tgt),flush=True)
print('full GL8 source,target',len(list(mons(11,[1,2,3,4,5,1]+list(range(1,9))+[1],[None]*14+[8]))),len(list(mons(12,[1,2,4,6,8,5]+list(range(1,9))))),flush=True)

def elementary(vals):
 e=[1]+[0]*len(vals)
 for x in vals:
  for j in range(len(vals),0,-1):e[j]=(e[j]+x*e[j-1])%P
 return e

def homogeneous(vals,lim):
 a=[1]+[0]*lim
 for x in vals:
  for j in range(1,lim+1):a[j]=(a[j]+x*a[j-1])%P
 return a

def rank(a):
 a=np.array(a,dtype=np.int64).copy(); m,n=a.shape;r=0
 for j in range(n):
  inds=np.flatnonzero(a[r:,j])
  if len(inds)==0:continue
  k=r+inds[0];a[[r,k]]=a[[k,r]]
  a[r]=a[r]*pow(int(a[r,j]),P-2,P)%P
  factors=a[:,j].copy();factors[r]=0
  a=(a-factors[:,None]*a[r])%P
  r+=1
  if r==m:break
 return r
rad=json.load(open('workspace/agent3_radical.json'))
from fractions import Fraction
coeff=[]
for c in rad['coefficients']:
 c=Fraction(c);coeff.append(c.numerator*pow(c.denominator%P,P-2,P)%P)
signs=[s for s in itertools.product([1,-1],repeat=5) if prod(s)==1]
random.seed(143)
N=len(tgt)+5
B=np.zeros((len(src),N),dtype=np.int64)
T=np.zeros((len(tgt),N),dtype=np.int64)
K=np.zeros((12,N),dtype=np.int64)
Delta=np.zeros(N,dtype=np.int64)
t0=time.time()
for n in range(N):
 while True:
  xs=[random.randrange(1,P) for _ in range(5)]
  if all((xs[i]+s*xs[j])%P for i in range(5) for j in range(i+1,5) for s in [1,-1]):break
 z=random.randrange(P);ys=[random.randrange(P) for _ in range(8)];ey=elementary(ys)
 xsq=elementary([x*x%P for x in xs]);g=[z]+xsq[1:5]+[prod(xs)%P]+ey[1:]
 T[:,n]=evmon(g,tgtarr)
 if n%100==0:print('point',n,'elapsed',time.time()-t0,flush=True)
 deg=0
 for sign in signs:
  xx=[x*s%P for x,s in zip(xs,sign)]; e=elementary(xx)
  h=e[1]*pow(2,P-2,P)%P
  tw=[(xx[i]+xx[j])%P for i in range(5) for j in range(i+1,5)]
  den=prod(tw)%P; invden=pow(den,P-2,P)
  deg=(deg+pow(h,10,P)*invden)%P
  eroots=[(h+y)%P for y in ys]+[(2*h+z)%P]
  ce=prod(eroots)%P
  for i in range(1,13):K[i-1,n]=(K[i-1,n]+ce*pow((2*h+ey[1]+z)%P,i+1,P)*invden)%P
  cot=elementary([-x%P for x in tw]); hs=homogeneous(eroots,10)
  qpush=np.array([sum(cot[j]*hs[m+2-j] for j in range(min(10,m+2)+1))%P for m in range(9)],dtype=np.int64)
  evals=e[1:]+[z]+ey[1:]
  ff=evmon(evals,srcarr[:,:-1])
  B[:,n]=(B[:,n]+ce*invden%P*ff%P*qpush[srcarr[:,-1]])%P
 assert deg==12,(deg,xs)
 Delta[n]=sum(c*prod(int(K[i-1,n]) for i in mon) for c,mon in zip(coeff,rad['monomials']))%P
print('built',time.time()-t0,flush=True)
print('target rank',rank(T),'boundary rank',rank(B),'augmented',rank(np.vstack([B,Delta])), 'delta nonzero eval',bool(np.any(Delta)),flush=True)
np.savez('workspace/agent4_spinor_test.npz',B=B,T=T,K=K,Delta=Delta)
from pathlib import Path
if Path(__file__).resolve()!=Path('workspace/agent4_spinor.py').resolve():
 Path('workspace/agent4_spinor.py').write_text(Path(__file__).read_text())
