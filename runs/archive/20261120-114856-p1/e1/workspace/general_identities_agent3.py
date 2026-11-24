import sympy as S
from pathlib import Path
# Exact rational verification of s-step orthogonal polynomial map identities.
z=S.symbols('z')
def update(lam,y,s):
 n=len(lam); A=S.diag(*lam); K=S.Matrix.hstack(*[A**j*y for j in range(s)])
 h=(K.T*K).inv()*(K.T*A**s*y)
 q=z**s-sum(h[j]*z**j for j in range(s))
 v=A**s*y-K*h
 assert K.T*v==S.zeros(s,1)
 return v,q
for s in range(1,5):
 lam=list(map(S.Integer,range(1,2*s+3)))
 y=S.Matrix([S.Rational(i+1,i+2) for i in range(len(lam))]); yn=(y.T*y)[0]
 v,q=update(lam,y,s); vn=(v.T*v)[0]
 u,p=update(lam,v,s); un=(u.T*u)[0]
 # Homogeneous norm growth and exact two-step overlap
 assert (y.T*u)[0]==vn
 assert S.factor(un*yn-vn**2)>=0
 # Stieltjes numerator transform (before normalization)
 P=S.prod(z-a for a in lam)
 N=S.expand(sum(y[i]**2*S.div(P,z-a,z)[0] for i,a in enumerate(lam)))
 Nv=S.expand(sum(v[i]**2*S.div(P,z-a,z)[0] for i,a in enumerate(lam)))
 h=S.rem(q*N,P,z)
 assert S.degree(h,z)<=len(lam)-s-1
 assert S.expand(Nv-q*h)==0
 print('s=',s,'exact orthogonality, norm monotonicity, overlap, Stieltjes identities PASS')
