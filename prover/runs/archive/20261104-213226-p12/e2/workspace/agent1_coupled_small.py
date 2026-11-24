# Coupled nonseparating/elliptic boundary detector, modular exploratory check.
import math,itertools,collections,sys,json,time,pickle,os
from functools import lru_cache
from fractions import Fraction
from sage.all import matrix,GF,vector
src=open('workspace/agent2_fz.py').read().split('cols=parts(12)')[0].replace('D=12','D=13').replace('range(1,11)','range(1,16)')
src=src.replace('P=1000000007','P=1000003')
ns={};exec(src,ns);nt={};exec(src.replace('k0=48','k0=47'),nt)
P=ns['P'];parts=ns['parts'];D=13
A=ns['A'];B=ns['B'];pmul=ns['pmul'];E=ns['E'];f=ns['f'];f47=nt['f'];E47=nt['E']
def mm(a,b):return tuple(sorted(a+b))
def mons(d,n=2):
 if n==2:return [(p,a,d-k-a) for k in range(d+1) for p in parts(k) for a in range(d-k+1)]
 return [(p,d-k) for k in range(d+1) for p in parts(k)]
def rels(d,n):
 for r in range(8,d+1):
  for ab in itertools.product(range(2),repeat=n):
   for size in range(3*r-24-sum(ab)+1):
    if (23+size+sum(ab)-r)%2:continue
    for sig in parts(size):
     if any(j%3==2 for j in sig):continue
     kp=pmul(E,f(sig)) if n==2 else pmul(E47,f47(sig))
     base={}
     for m,c in kp.items():
      rem=r-sum(m)
      if rem<0:continue
      for aps in ([(a,rem-a) for a in range(rem+1)] if n==2 else [(rem,)]):
       v=c*math.prod((A if ai==0 else B)[a] for ai,a in zip(ab,aps))%P
       if v:base[(m,)+aps]=v
     for mul in mons(d-r,n):
      out={}
      for mono,c in base.items():out[(mm(mono[0],mul[0]),)+tuple(x+y for x,y in zip(mono[1:],mul[1:]))]=c
      yield out,(r,ab,sig,mul)
cols=mons(13);idx={m:i for i,m in enumerate(cols)}; h12=mons(12,1);i12={m:i for i,m in enumerate(h12)};h13=mons(13,1);i13={m:i for i,m in enumerate(h13)}
N=len(cols);U=len(h12);V=len(h13);total=N+U+V
rows=[];fl=[];labs=[]
for rel,lab in rels(13,2):
 r,ab,sig,mul=lab;row=[0]*total
 for m,c in rel.items():row[idx[m]]=c
 if mul[1:]==(0,0):
  ones=sig.count(1)
  for z in range(ones+1):
   ss=list(sig)
   for _ in range(z):ss.remove(1)
   pol=pmul(E47,f47(tuple(ss)));fac=(-1)**sum(ab)*math.comb(ones,z)*math.factorial(z)
   for k,c in pol.items():
    a=r-1-sum(k)
    if a<0:continue
    hc=B[a+1] if (z+sum(ab))%2 else -A[a+1]
    key=(mm(k,mul[0]),a)
    row[N+i12[key]]=(row[N+i12[key]]+fac*c*hc)%P
 rows.append(row);fl.append(0);labs.append(('rel',lab))
print('double rels',len(rows),flush=True)
# Hodge integrals direct in pointed kappa coordinates.
weights={a:pow(math.prod(range(1,2*a+2,2)),P-2,P) for a in range(25)}
@lru_cache(None)
def bell(mu):
 if not mu:return (1,)
 co=collections.Counter(mu[1:]);ks=tuple(co);out=[0]*(len(mu)+1)
 for ns in itertools.product(*(range(co[k]+1) for k in ks)):
  s=mu[0]+sum(k*n for k,n in zip(ks,ns));rem=tuple(sorted(k for k,n in zip(ks,ns) for _ in range(co[k]-n)))
  c=math.prod(math.comb(co[k],n) for k,n in zip(ks,ns))*weights[s]%P
  for j,v in enumerate(bell(rem)):out[j+1]=(out[j+1]+c*v)%P
 return tuple(out)
@lru_cache(None)
def integral(mu,aps):
 n=len(aps);v=sum((-1)**(len(mu)-k)*math.factorial(45+n+k)*x for k,x in enumerate(bell(mu)))%P
 return v*pow(math.prod(math.prod(range(1,2*a,2)) for a in aps),P-2,P)%P
j=json.load(open('workspace/agent3_radical.json'));delta=[]
for m,c in zip(j['monomials'],j['coefficients']):
 c=Fraction(c);delta.append((tuple(m),c.numerator*pow(c.denominator,P-2,P)%P))
bcols=[m for m in mons(12) if m[2]>=m[1] and m[1]+m[2]>0]
for p,a,b in bcols:
 row=[0]*total
 for aa,bb in [(a,b)]+([] if a==b else [(b,a)]):
  for key in [(p,aa+1,bb),(p,aa,bb+1)]:row[idx[key]]-=1
 rows.append(row);labs.append(('beta',(p,a,b)))
 fl.append(12*sum(c*integral(mm(m,p),(a,b)) for m,c in delta)*(1 if a==b else 2)%P)
for p,a in mons(11,1):
 row=[0]*total;row[N+i12[(p,a+1)]]=-1;row[N+U+i13[(p,a+2)]]=1
 val=0
 for m,c in delta:
  val+=c*integral(mm(m,p),(a,))
  if 1 in m:
   rem=list(m);rem.remove(1);val-=c*m.count(1)*integral(mm(tuple(rem),p),(a+1,))
 rows.append(row);fl.append(val%P);labs.append(('gamma',(p,a)))
for d,offset,ix in [(12,N,i12),(13,N+U,i13)]:
 for rel,lab in rels(d,1):
  row=[0]*total
  for m,c in rel.items():row[offset+ix[m]]=c
  rows.append(row);fl.append(0);labs.append(('single',d,lab))
print('matrix',len(rows),total,flush=True)
M=matrix(GF(P),rows);print('rank',M.rank(),flush=True)
aug=M.augment(vector(GF(P),fl).column());print('augmented rank',aug.rank(),flush=True)
pickle.dump((P,labs,rows,fl),open('workspace/agent1_coupled_small_matrix.pkl','wb'))

print('matrix saved; selecting independent rows',flush=True)
ri=aug.transpose().pivots();print('selected',len(ri),flush=True)
S=aug.matrix_from_rows(ri); ci=S.pivots();SS=S.matrix_from_columns(ci)
target=vector(GF(P),[1 if c==total else 0 for c in ci])
x=SS.transpose().solve_right(target)
assert x*S==vector(GF(P),[0]*total+[1])
sol=[0]*len(rows)
for i,c in zip(ri,x):sol[i]=int(c)
pickle.dump((P,labs,sol,ri,ci),open('workspace/agent1_coupled_small_solution.pkl','wb'))
beta=[];rho=[]
for lab,c in zip(labs,sol):
 if c and lab[0]=='beta':p,a,b=lab[1];beta.append((p,a,b,c))
 if c and lab[0]=='gamma':p,a=lab[1];rho.append((p,a,c))
json.dump({'beta':beta,'rho':rho},open('workspace/agent1_small_dual.json','w'))
print('witness saved beta',len(beta),'rho',len(rho),flush=True)
