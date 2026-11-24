import sympy as S,pickle
from pathlib import Path
z=S.symbols('z');P=S.Poly(z**4-5*z*z+4,z);h=S.Poly(-z**3-2*z*z+z+8,z);k=S.Poly(z*z+4*z+7,z);D=P*P-S.Poly(1,z);assert h*h-P*k==S.Poly(36,z)
N=6;zero=S.Poly(0,z);one=S.Poly(1,z)
# Newton sums through15 usingcompanion traces
coeff=[D.nth(i) for i in range(8)];Comp=S.zeros(8)
for i in range(7):Comp[i+1,i]=1
for i in range(8):Comp[i,7]=-coeff[i]
mom=[];CC=S.eye(8)
for j in range(16):mom.append(S.trace(CC)/8);CC=CC*Comp

def expect(p,j=0):return sum(p.nth(a)*mom[a+j] for a in range(8))
def pmul(a,b):return (a*b).rem(D)
def pscale(a,c):return S.Poly(a.as_expr()*c,z,domain=S.QQ)
def step(L):
 count=len(L);M=[S.Matrix(4,4,lambda i,j:expect(ll,i+j)) for ll in L];cc=[S.Matrix([expect(ll,j+4) for j in range(4)]) for ll in L];MI=M[0].inv();aa=[];pp=[]
 for j in range(count):
  aa.append(-MI*(cc[j]+sum((M[r]*aa[j-r] for r in range(1,j+1)),S.zeros(4,1))))
  pp.append(S.Poly((z**4 if j==0 else 0)+sum(aa[j][i]*z**i for i in range(4)),z))
 raw=[];den=[];out=[]
 for j in range(count):
  rr=zero
  for a in range(j+1):
   for b in range(j-a+1):rr+=pmul(L[a],pmul(pp[b],pp[j-a-b]))
  raw.append(rr);den.append(expect(rr))
  out.append(pscale(raw[j]-sum((pscale(out[j-r],den[r]) for r in range(1,j+1)),zero),1/den[0]))
 return out
L=[one,(P*h).rem(D)]+[zero]*(N-1);f1=step(L);print('firstdone',flush=True);f2=step(f1);print('seconddone',flush=True)
for j in range(N+1):
 diff=f2[j]-L[j];print('ORDER',j,'diff=',S.factor(diff.as_expr()),'normalmoments',[S.factor(expect(pmul(diff,P),i)) for i in range(4)],flush=True)
b3=f2[3]-L[3]
M=S.Matrix(4,4,lambda i,j:mom[i+j])
def tangent(a):
 aa=a-one*expect(a);co=M.inv()*S.Matrix([expect(pmul(P,aa),j) for j in range(4)]);return aa-pmul(P,S.Poly(sum(co[j]*z**j for j in range(4)),z))
for expr in [pmul(h,k),pmul(P,pmul(h,k))]:
 pr=tangent(expr);rat=S.cancel(b3.as_expr()/pr.as_expr());print('b3/gradientratio',rat)
moving=pmul(b3,pmul(P,h));print('movingnormal4residual',[S.factor(expect(pmul(f2[4]-moving,P),j)) for j in range(4)])
with open('workspace/agent4_simplepell_jets.pkl','wb') as f:pickle.dump(dict(P=P,h=h,k=k,D=D,L=L,F2=f2,mom=mom,movingnormal4=[expect(pmul(f2[4]-moving,P),j) for j in range(4)]),f)
