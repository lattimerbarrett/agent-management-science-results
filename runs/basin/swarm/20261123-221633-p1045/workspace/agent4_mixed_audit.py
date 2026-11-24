"""Independent exact audit of adaptive three-root certificate and frozen extension."""
import sympy as S
r=S.sqrt(3)
s,u,A=S.symbols('s u A', positive=True)
H=S.symbols('H0:3',nonnegative=True);N=S.symbols('N0:3',nonnegative=True)
L=S.symbols('L',real=True)
k=3-(2*r-3)/u;t=2*r*u;ell=4/t-2;K=3-t;a=u*u
zeta=k*s/t
eli=[4/(t+k*s*h)-2 for h in H]
# L here is E[sum(1-r_i)^2]; N_i=E[r_j r_k].
D= -s*K-k*s*(a-s)+s*L+s*sum(l*n for l,n in zip(eli,N))-a*sum(eli)+3*a*ell
F0=L+ell*sum(N)+k*sum(H)/3-k*a-K
formula=F0+k*s-k*zeta/3*sum(h*h/(1+zeta*h) for h in H)-k*s/(3*a)*sum(h*n/(1+zeta*h) for h,n in zip(H,N))
assert S.simplify(D/s-formula)==0
# Frozen endpoint, with a>=A and A=q*².
q=4/r-2;AA=S.expand(q*q);kk=S.Rational(3,2);tt=2*r*q;ll=r;KK=4*r-5
elistar=[4/(tt+kk*s*h)-2 for h in H];zz=kk*s/tt
bb=S.symbols('a',positive=True)
DD=-s*KK-kk*s*(bb-s)+s*L+s*sum(l*n for l,n in zip(elistar,N))-bb*sum(elistar)+3*bb*ll
FF=L+ll*sum(N)+kk*sum(H)/3-kk*bb-KK
frozen_formula=FF+kk*s-kk*zz/3*sum(h*h/(1+zz*h) for h in H)-kk*s/(3*AA)*sum(h*n/(1+zz*h) for h,n in zip(H,N))
extra=kk*(bb-AA)/(3*AA)*sum(h/(1+zz*h) for h in H)
assert S.simplify(DD/s-frozen_formula-extra)==0
assert S.simplify(kk/(3*tt)+1/(9*AA))<S.Rational(5,3)
# Exact SOS for sum H_i sqrt(H_j H_k)<=Q²/3.
x,y,z=S.symbols('x y z',real=True)
lhs=(x*x+y*y+z*z)**2-3*x*y*z*(x+y+z)
rhs=((x*x-y*y)**2+(y*y-z*z)**2+(z*z-x*x)**2)/2+S.Rational(3,2)*((x*y-y*z)**2+(y*z-z*x)**2+(z*x-x*y)**2)
assert S.expand(lhs-rhs)==0
print('ALL INDEPENDENT ADAPTIVE-CERTIFICATE IDENTITIES PASSED')
