import math,itertools,time
from functools import lru_cache
import numpy as np
P=1000000007;G=25;D=23
@lru_cache(None)
def parts(n,m=1):
 if n==0:return ((),)
 return tuple((i,)+p for i in range(m,n+1) for p in parts(n-i,i))
def sermul(a,b):return [sum(a[i]*b[n-i] for i in range(n+1))%P for n in range(D+1)]
A=[math.factorial(6*n)//(math.factorial(3*n)*math.factorial(2*n))%P for n in range(D+1)]
B=[A[n]*(6*n+1)*pow(6*n-1,-1,P)%P for n in range(D+1)]
AI=[1]
for n in range(1,D+1):AI.append(-sum(A[i]*AI[n-i] for i in range(1,n+1))%P)
BA=sermul(B,AI);LD=sermul([(i+1)*A[i+1]%P for i in range(D)]+[0],AI)
L=[0]+[LD[i-1]*pow(i,-1,P)%P for i in range(1,D+1)]
def add(a,b,c=1):
 out=a.copy()
 for k,v in b.items():
  out[k]=(out.get(k,0)+c*v)%P
  if not out[k]:del out[k]
 return out
def mul(a,b):
 out={}
 for x,v in a.items():
  sx=sum(x)
  for y,w in b.items():
   if sx+sum(y)<=D:
    k=tuple(sorted(x+y));out[k]=(out.get(k,0)+v*w)%P
 return out
def scale(a,c):return {k:v*c%P for k,v in a.items() if v*c%P}
F0={():1}
for i in range(1,D+1):F0=mul(F0,{(i,)*j:pow(-L[i],j,P)*pow(math.factorial(j),-1,P)%P for j in range(D//i+1)})
@lru_cache(None)
def gamma(sig):
 c=(-1)**(len(sig)+1)*math.factorial(len(sig)-1)
 for x in set(sig):c=c*pow(math.factorial(sig.count(x)),-1,P)%P
 shift=sum(x//3 for x in sig);arr=[1]+[0]*D
 for x in sig:
  if x%3==1:arr=sermul(arr,BA)
 arr=[0]*shift+arr[:D+1-shift]
 return {(() if i==0 else (i,)):v*c*(2*G-2 if i==0 else 1)%P for i,v in enumerate(arr) if v}
@lru_cache(None)
def F(sig):
 if not sig:return F0
 s=sig[0];cts={x:sig.count(x) for x in set(sig)};out={}
 for ns in itertools.product(*(range(cts[x]+1) for x in cts)):
  a=tuple(sorted(sum(([x]*n for x,n in zip(cts,ns)),[])))
  if s not in a:continue
  b=list(sig)
  for x in a:b.remove(x)
  out=add(out,mul(gamma(a),F(tuple(b))),-a.count(s))
 return scale(out,pow(cts[s],-1,P))
# modular row echelon, with early stopping for sufficient upper bound
class Space:
 def __init__(self,n):self.n=n;self.piv={}
 def push(self,row):
  v=np.array(row,dtype=np.int64)
  for j in sorted(self.piv):
   if v[j]:v=(v-v[j]*self.piv[j])%P
  nz=np.flatnonzero(v)
  if len(nz):
   j=int(nz[0]);self.piv[j]=v*pow(int(v[j]),-1,P)%P
 def rank(self):return len(self.piv)
@lru_cache(None)
def blocks(k):
 if not k:return {():1}
 a=k[0];rest=k[1:];out={};cts={x:rest.count(x) for x in set(rest)}
 for ns in itertools.product(*(range(cts[x]+1) for x in cts)):
  ch=[];left=[];c=1
  for x,n in zip(cts,ns):ch += [x]*n;left += [x]*(cts[x]-n);c*=math.comb(cts[x],n)
  c*=(-1)**len(ch)
  for sums,b in blocks(tuple(sorted(left))).items():
   key=tuple(sorted((a+sum(ch),)+sums));out[key]=out.get(key,0)+c*b
 return out
@lru_cache(None)
def top(k):
 assert sum(k)==23
 result=0
 for sums,c in blocks(k).items():
  den=math.prod(math.prod(range(1,2*s+2,2)) for s in sums)%P
  result=(result+c*math.factorial(47+len(sums))*pow(den,-1,P))%P
 return result
lower=[]
for d in range(24):
 e=min(d,23-d);f=23-e;S=Space(len(parts(f)))
 for a in parts(e):S.push([top(tuple(sorted(a+b))) for b in parts(f)])
 lower.append(S.rank())
print('pairing lower',lower,flush=True)
upper=[];ideals={}
for d in range(24):
 cols=parts(d);idx={x:i for i,x in enumerate(cols)};S=Space(len(cols));target=len(cols)-lower[d]-(d==12)
 # products of earlier known relations
 for i in range(1,d+1):
  for v in ideals[d-i]:
   row=np.zeros(len(cols),dtype=np.int64)
   for x,c in v.items():row[idx[tuple(sorted(x+(i,)))]]=c
   S.push(row)
   if S.rank()>=target:break
  if S.rank()>=target:break
 # add sufficiently many fresh FZ generators. Cap weight only for efficiency.
 if S.rank()<target:
  for w in range(min(14,3*d-G-1)+1):
   if (G-1-d-w)%2:continue
   for sig in parts(w):
    if any(x%3==2 for x in sig):continue
    pol=F(sig);S.push([pol.get(x,0) for x in cols])
    if S.rank()>=target:break
   if S.rank()>=target:break
 upper.append(len(cols)-S.rank())
 ideals[d]=[{cols[i]:int(v[i]) for i in np.flatnonzero(v)} for v in S.piv.values()]
 print('degree',d,'lower',lower[d],'upper',upper[d],flush=True)
 assert upper[d]==lower[d]+(d==12),(d,upper[d],lower[d])
print('SUCCESS: only possible discrepancy is one dimension in degree 12.',flush=True)
