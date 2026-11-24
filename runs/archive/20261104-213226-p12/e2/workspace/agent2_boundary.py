import os,sys,json,math,itertools,collections,time
from fractions import Fraction
from functools import lru_cache
from sage.all import matrix,GF,vector
code=open('workspace/agent2_fz.py').read().split('cols=parts(12)')[0].replace('D=12','D=13')
exec(code)
for n in range(len(BAp),14):BAp.append(conv(BAp[-1],BA))
# Monomials (kappa partition, psi1 exponent, psi2 exponent).
def mons(d):return [(p,a,d-k-a) for k in range(d+1) for p in parts(k) for a in range(d-k+1)]
cols=mons(13);idx={m:i for i,m in enumerate(cols)}
rows=[];labels=[]
for r in range(8,13): # require multiplier psi, so r<=12
 for aa,bb in itertools.product(range(2),repeat=2):
  for size in range(3*r-24-aa-bb+1):
   if (23+size+aa+bb-r)%2:continue
   for sig in parts(size):
    if any(j%3==2 for j in sig):continue
    kp=pmul(E,f(sig));base={}
    for m,c in kp.items():
     for a in range(r-sum(m)+1):
      b=r-sum(m)-a
      fac=(A if aa==0 else B)[a]*(A if bb==0 else B)[b]%P
      if fac:base[(m,a,b)]=c*fac%P
    for q,u,v in mons(13-r):
     if not u+v:continue # kills rational-tail corrections!
     row=[0]*len(cols)
     for (m,a,b),c in base.items():row[idx[(mulmono(m,q),a+u,b+v)]]=c
     rows.append(row);labels.append((r,aa,bb,sig,q,u,v))
 print('r',r,'rows',len(rows),flush=True)
print('relation matrix',len(rows),len(cols),flush=True)
R=matrix(GF(P),rows); RE=R.echelon_form(); piv=RE.pivots();print('rankR',len(piv),flush=True)
# Symmetric beta with both psi exponents positive.
bcols=[(p,a,b) for p,a,b in mons(12) if b>=a and a+b>=1]
N=[]
for p,a,b in bcols:
 row=[0]*len(cols)
 for aa,bb in [(a,b)]+([] if a==b else [(b,a)]):
  for u,v in [(aa+1,bb),(aa,bb+1)]:row[idx[(p,u,v)]]+=1
 N.append(row)
N=matrix(GF(P),N)
# Reduce every normal multiplication row modulo known relations.
for i,pivcol in enumerate(piv):
 coeff=N.column(pivcol)
 N-=matrix(coeff.column())*RE.row(i).row()
print('beta variables',len(bcols),'rank normal mod R',N.rank(),flush=True)
K=N.left_kernel().basis_matrix();print('annihilators',K.nrows(),flush=True)
# Faber integrals for kappa mu, psi powers>=1.
weights={a:pow(math.prod(range(1,2*a+2,2)),P-2,P) for a in range(25)}
@lru_cache(None)
def bell(mu):
 if not mu:return (1,)
 co=collections.Counter(mu[1:]);keys=tuple(co);out=[0]*(len(mu)+1)
 for ns in itertools.product(*(range(co[k]+1) for k in keys)):
  s=mu[0]+sum(k*n for k,n in zip(keys,ns)); rem=tuple(sorted(k for k,n in zip(keys,ns) for _ in range(co[k]-n)))
  c=math.prod(math.comb(co[k],n) for k,n in zip(keys,ns))*weights[s]%P
  for j,v in enumerate(bell(rem)):out[j+1]=(out[j+1]+c*v)%P
 return tuple(out)
@lru_cache(None)
def integral(mu,a,b):
 val=sum((-1)**(len(mu)-k)*math.factorial(47+k)*v for k,v in enumerate(bell(mu)))%P
 return val*pow(math.prod(range(1,2*a,2))*math.prod(range(1,2*b,2)),P-2,P)%P
j=json.load(open('workspace/agent3_radical.json'))
delta=[]
for m,c in zip(j['monomials'],j['coefficients']):
 c=Fraction(c);delta.append((tuple(m),c.numerator*pow(c.denominator,P-2,P)%P))
L=vector(GF(P),[sum(c*integral(tuple(sorted(m+p)),a,b) for m,c in delta)*(1 if a==b else 2)%P for p,a,b in bcols])
vals=K*L
print('nonzero delta test?',any(vals),'num nonzero',sum(bool(x) for x in vals),flush=True)
import pickle
pickle.dump((P,bcols,K,L,labels),open('workspace/agent2_boundary_test.pkl','wb'))
# Self-save omitted to avoid truncation when run from workspace.
