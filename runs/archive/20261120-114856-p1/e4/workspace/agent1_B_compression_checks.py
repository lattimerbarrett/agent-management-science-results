import sympy as S
import numpy as np
from scipy.linalg import null_space
from pathlib import Path
z=S.symbols('z')
def poly(vals,w,s):
 mu=[sum(wi*xi**j for wi,xi in zip(w,vals)) for j in range(2*s+1)]
 G=S.Matrix(s,s,lambda i,j:mu[i+j]);u=-G.inv()*S.Matrix(mu[s:2*s])
 q=S.Poly(z**s+sum(u[j]*z**j for j in range(s)),z)
 h=sum(wi*q.eval(xi)**2 for wi,xi in zip(w,vals))
 wn=[wi*q.eval(xi)**2/h for wi,xi in zip(w,vals)]
 return q,h,wn
for s,n in [(1,4),(2,5),(2,6),(3,6),(3,8),(4,8),(4,9)]:
 vals=list(range(1,n+1));ww=list(range(3,3+n));w=[S.Rational(a,sum(ww)) for a in ww]
 P=S.Poly(S.prod(z-x for x in vals),z)
 def M(w):return S.Poly(sum((wi*P.exquo(S.Poly(z-xi,z)).as_expr() for wi,xi in zip(w,vals))),z)
 q,h,w1=poly(vals,w,s);r,h1,w2=poly(vals,w1,s)
 a,t=(q*M(w)).div(P);a1,t1=(r*M(w1)).div(P)
 B,rem=(a*t1-a1*t).div(q);assert rem.is_zero
 assert B.nth(n-s-2)==h1-h
 y=np.sqrt(np.array(w,dtype=float));yp=np.sqrt(np.array(w1,dtype=float))*np.array([(-1.)**s*np.sign(float(q.eval(x))) for x in vals])
 # Use signed q*y/sqrt(h), global irrelevant.
 yp=np.array([float(q.eval(xi)) for xi in vals])*y/np.sqrt(float(h))
 e=np.array([float(q.eval(xi)*r.eval(xi)-h) for xi in vals])
 V=np.column_stack([yp*np.array(vals,dtype=float)**j for j in range(s)]+[y,e*y])
 C=null_space(V.T)
 assert C.shape[1]==n-s-2
 eig=np.linalg.eigvalsh(C.T@np.diag(vals)@C)
 roots=np.sort(np.array([complex(t) for t in S.nroots(B.as_expr())]).real)
 err=np.max(abs(eig-roots)) if len(eig) else 0
 print('s,n',s,n,'err',err,'B',B.as_expr(),flush=True)
 assert err<1e-7
print('PASS compression-spectrum checks')
