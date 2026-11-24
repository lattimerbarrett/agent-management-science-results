import math,itertools,collections,pickle,os
from functools import lru_cache
P=1000000007; D=12; k0=48

def inv(x):return pow(x,P-2,P)
def conv(a,b):
 c=[0]*(D+1)
 for i,x in enumerate(a):
  for j,y in enumerate(b[:D+1-i]):c[i+j]=(c[i+j]+x*y)%P
 return c
A=[math.factorial(6*n)//(math.factorial(3*n)*math.factorial(2*n))%P for n in range(D+1)]
B=[a*((6*n+1)*inv(6*n-1)%P)%P for n,a in enumerate(A)]
Ai=[1]+[0]*D
for i in range(1,D+1): Ai[i]=-sum(A[j]*Ai[i-j] for j in range(1,i+1))%P
BA=conv(B,Ai)
logA=[0]+[sum(j*A[j]*Ai[n-j] for j in range(1,n+1))*inv(n)%P for n in range(1,D+1)]
# exponent in graded kappa polynomial
@lru_cache(None)
def mulmono(a,b):return tuple(sorted(a+b))
def pmul(a,b):
 out=collections.defaultdict(int)
 for x,c in a.items():
  for y,e in b.items():
   if sum(x)+sum(y)<=D:
    z=mulmono(x,y);out[z]=(out[z]+c*e)%P
 return {z:c for z,c in out.items() if c}
E={():1}
for n in range(1,D+1):
 fac={tuple([n]*j):pow(-logA[n],j,P)*inv(math.factorial(j))%P for j in range(D//n+1)}
 E=pmul(E,fac)
BAp=[[1]+[0]*D]
for n in range(1,11): BAp.append(conv(BAp[-1],BA))
@lru_cache(None)
def block(sig):
 shift=sum(x//3 for x in sig); m=sum(x%3==1 for x in sig)
 out={}
 for n in range(shift,D+1):
  c=BAp[m][n-shift]
  if c:out[(n,) if n else ()]=c*(k0 if n==0 else 1)%P
 return out
@lru_cache(None)
def f(sig):
 if not sig:return {():1}
 counts=collections.Counter(sig[1:]);types=tuple(counts)
 out=collections.defaultdict(int)
 for nums in itertools.product(*(range(counts[t]+1) for t in types)):
  sub=(sig[0],)+tuple(t for t,n in zip(types,nums) for _ in range(n))
  rem=tuple(t for t,n in zip(types,nums) for _ in range(counts[t]-n))
  coeff=(-1)**len(sub)*math.factorial(len(sub)-1)
  coeff*=math.prod(math.comb(counts[t],n) for t,n in zip(types,nums))
  pol=pmul(block(sub),f(rem))
  for z,c in pol.items():out[z]=(out[z]+coeff*c)%P
 return {z:c for z,c in out.items() if c}
@lru_cache(None)
def parts(n,lo=1):
 if not n:return ((),)
 return tuple((i,)+p for i in range(lo,n+1) for p in parts(n-i,i))
cols=parts(12); idx={p:i for i,p in enumerate(cols)}
rows=[]; labels=[]
for r in range(9,13):
 for size in range(3*r-26+1):
  if (size-r)%2:continue
  for sig in parts(size):
   if any(x%3==2 for x in sig):continue
   rel={m:c for m,c in pmul(E,f(sig)).items() if sum(m)==r}
   for q in parts(12-r):
    row=[0]*len(cols)
    for m,c in rel.items():row[idx[mulmono(m,q)]]=c
    rows.append(row);labels.append((r,sig,q))
 print('degree',r,'relations',len(rows),flush=True)
base={}; pivots=[]
for row,lab in zip(rows,labels):
 row=row[:]
 for j in range(len(cols)):
  if not row[j]:continue
  if j in base:
   c=row[j];row=[(a-c*b)%P for a,b in zip(row,base[j])]
  else:
   c=inv(row[j]);base[j]=[a*c%P for a in row];pivots.append(lab);break
print('columns',len(cols),'rows',len(rows),'rank',len(base),'dimension upper',len(cols)-len(base))
print('independent labels',pivots)
os.makedirs('workspace',exist_ok=True)
pickle.dump((P,cols,rows,labels),open('workspace/agent2_fz_mod.pkl','wb'))
# Explicit 33 by 33 minor selected by row and column pivot labels.
ri=[labels.index(lab) for lab in pivots]; ci=sorted(base)
minor=[[rows[i][j] for j in ci] for i in ri]
det=1
for k in range(len(minor)):
 q=next(i for i in range(k,len(minor)) if minor[i][k])
 if q!=k: minor[q],minor[k]=minor[k],minor[q];det=-det
 v=minor[k][k];det=det*v%P
 for i in range(k+1,len(minor)):
  c=minor[i][k]*inv(v)%P
  for j in range(k,len(minor)):minor[i][j]=(minor[i][j]-c*minor[k][j])%P
print('minor determinant mod P',det%P)
print('pivot columns',ci)
print('44 surviving monomials',[cols[i] for i in range(len(cols)) if i not in base])
import json
json.dump({'prime':P,'row_indices':ri,'column_indices':ci,'determinant':det%P,'independent_relation_labels':pivots,'monomials':cols},open('workspace/agent2_upper_certificate.json','w'))
# Save this self-contained verifier in shared workspace.
if os.path.abspath(__file__) != os.path.abspath('workspace/agent2_fz.py'):
 open('workspace/agent2_fz.py','w').write(open(__file__).read())
