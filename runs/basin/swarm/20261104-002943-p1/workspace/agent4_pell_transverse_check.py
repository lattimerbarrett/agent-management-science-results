import sympy as S,pickle,time
from pathlib import Path
x,a=S.symbols('x a');zz=S.symbols('z0:3');dom=S.QQ.frac_field(*zz);N=6
P=S.Poly(x**4-5*x*x+4,x,domain=dom);hh=S.Poly(-x**3-2*x*x+x+8,x,domain=dom);D=P*P-S.Poly(1,x,domain=dom);zero=S.Poly(0,x,domain=dom);one=S.Poly(1,x,domain=dom)
# Rational Hensel lift of q_a rootbranches.
rootjets=[]
for alpha in [-2,-1,1,2]:
 rr=S.Integer(alpha);target=-hh.as_expr().subs(x,alpha)
 for j in range(1,N+1):
  residual=S.Poly(S.expand(rr**4-5*rr**2+4),a).nth(j);co=((target if j==1 else 0)-residual)/(4*alpha**3-10*alpha);rr+=co*a**j
 rootjets.append([S.Poly(rr,a).nth(j) for j in range(N+1)])
qjet=[one]+[zero]*N
for rj in rootjets:
 fac=[S.Poly(x-rj[0],x,domain=dom)]+[S.Poly(-rj[j],x,domain=dom) for j in range(1,N+1)];qjet=[sum((qjet[k]*fac[j-k] for k in range(j+1)),zero) for j in range(N+1)]
assert qjet[0]==P and qjet[1]==hh
for j in range(N+1):
 prod=sum((qjet[k]*qjet[j-k]*(-1)**(j-k) for k in range(j+1)),zero);target=P*P if j==0 else (S.Poly(-36,x,domain=dom) if j==2 else zero);assert prod==target
print('factorbranchchecked',flush=True)
# moments through15
Comp=S.zeros(8)
for i in range(7):Comp[i+1,i]=1
for i in range(8):Comp[i,7]=-D.nth(i)
mom=[];CC=S.eye(8)
for j in range(16):mom.append(S.trace(CC)/8);CC=CC*Comp

def exp(p,j=0):return S.expand(sum(p.nth(i)*mom[i+j] for i in range(8)))
def mul(p,q):return (p*q).rem(D)
def scale(p,c):return p.mul_ground(c)
def orthop(L):
 M=[S.Matrix(4,4,lambda i,j:exp(ll,i+j)) for ll in L];cc=[S.Matrix([exp(ll,j+4) for j in range(4)]) for ll in L];MI=M[0].inv();aa=[];pq=[]
 for j in range(len(L)):
  aa.append((-MI*(cc[j]+sum((M[r]*aa[j-r] for r in range(1,j+1)),S.zeros(4,1)))).applyfunc(S.expand));pq.append(S.Poly((x**4 if j==0 else 0)+sum(aa[j][i]*x**i for i in range(4)),x,domain=dom))
 return pq

def step(L):
 pq=orthop(L);out=[];den=[]
 for j in range(len(L)):
  rr=zero
  for b in range(j+1):
   for c in range(j-b+1):rr+=mul(L[b],mul(pq[c],pq[j-b-c]))
  den.append(exp(rr));out.append(scale(rr-sum((scale(out[j-r],den[r]) for r in range(1,j+1)),zero),1/den[0]))
 return out
Z=S.Poly(zz[0]+zz[1]*x+zz[2]*x*x,x,domain=dom);L=[mul(P,qjet[j])*(-1)**j for j in range(N+1)];L[2]+=mul(P,Z);L[4]-=36*mul(P,Z)
p0=orthop(L);f1=step(L);print('firstdone',flush=True);f2=step(f1);print('seconddone',flush=True);p2=orthop(f2);print('thirdOPdone',flush=True)
for j in range(N+1):
 dL=f2[j]-L[j];dp=p2[j]-p0[j]
 print('ORDER',j,'densityzero',dL.is_zero,'qdiff=',S.factor(dp.as_expr()),flush=True)
 if j==3:print('BASE3',S.factor(dL.as_expr()),flush=True)
dp5=p2[5]-p0[5];r=S.factor(dp5.nth(3)/hh.nth(3));Zdot=-(dp5-scale(hh,r));print('RADIAL',r,'ZDOT',S.factor(Zdot.as_expr()),flush=True)
with open('workspace/agent4_pell_transverse_jets.pkl','wb') as f:pickle.dump(dict(P=P,h=hh,D=D,Zvars=zz,qjet=qjet,L=L,F2=f2,pbefore=p0,pafter=p2,radial=r,Zdot=Zdot),f)
