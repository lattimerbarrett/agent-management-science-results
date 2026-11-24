"""Exact checks accompanying agent2_strict_left_deflation.md."""
import sympy as S
x=S.symbols('x'); nodes=list(map(S.Rational,[-3,-2,-1,1,2,3]))
d=[S.prod(a-b for b in nodes if b!=a) for a in nodes]
q=[S.Rational(30,11) if abs(a)==3 else S.Integer(1) for a in nodes]
p=[1/(di**2*qi) for di,qi in zip(d,q)];p=[pi/sum(p) for pi in p]
def op(p,degree):
 M=S.Matrix([[sum(pi*a**(j+k) for pi,a in zip(p,nodes)) for k in range(degree)] for j in range(degree)])
 rhs=S.Matrix([-sum(pi*a**(j+degree) for pi,a in zip(p,nodes)) for j in range(degree)])
 c=M.inv()*rhs
 return S.Poly(x**degree+sum(c[i]*x**i for i in range(degree)),x).as_expr()
def block(p):
 f=op(p,3); N=S.factor(sum(pi*f.subs(x,a)**2 for pi,a in zip(p,nodes)))
 new=[S.factor(pi*f.subs(x,a)**2/N) for pi,a in zip(p,nodes)]
 H=op([1/(di**2*pi) for di,pi in zip(d,p)],2)
 for i,a in enumerate(nodes): assert S.cancel(H.subs(x,a)-d[i]*p[i]*f.subs(x,a)/N)==0
 assert S.cancel(sum(H.subs(x,a)**2/(di**2*pi) for a,di,pi in zip(nodes,d,p))-1/N)==0
 return new,f,N,H
p1,f0,N0,H0=block(p);p2,f1,N1,H1=block(p1);p3,f2,N2,H2=block(p2)
assert H0==x*x-S.Rational(25,4)
Hs=[H0,H1,H2]; ps=[p,p1,p2]
Ds=[x+S.sqrt(-Hi.subs(x,0)) for Hi in Hs]
HH=[x-S.sqrt(-Hi.subs(x,0)) for Hi in Hs]
qs=[[1/(di**2*pi) for di,pi in zip(d,pp)] for pp in ps]
for qi,Di,hi,Hi in zip(qs,Ds,HH,Hs):
 assert S.simplify(Di*hi-Hi)==0
 # Degree-one orthogonality for the exact positive Christoffel measure.
 assert S.simplify(sum(qj*Di.subs(x,a)**2*hi.subs(x,a) for qj,a in zip(qi,nodes)))==0
for i,a in enumerate(nodes):
 assert S.simplify(H1.subs(x,a)/H0.subs(x,a)-f0.subs(x,a)*f1.subs(x,a)/N1)==0
 # Scalar in q2/q0 equals N0/N1.
 lhs=qs[2][i]*Ds[2].subs(x,a)**2/(qs[0][i]*Ds[0].subs(x,a)**2)
 rhs=N0/N1*(HH[0].subs(x,a)/HH[1].subs(x,a))**2*(Ds[2].subs(x,a)/Ds[1].subs(x,a))**2
 assert S.simplify(lhs-rhs)==0
print('PASS exact dual interpolation/norm/two-block identities and Christoffel deflation')
eta,a0,a1,C,h,zeta=S.symbols('eta a0 a1 C h zeta', nonzero=True)
Sl=C*h*h*a0*(1-a0/a1)
Spl=C*h*h*a0*a0/(eta*a1*a1)
R=zeta+eta*a1+Sl/Spl
assert S.cancel(R-zeta-eta*a1*a1/a0)==0
print('PASS signed finite-triple Rayleigh displacement identity (no alpha-sign assumption)')
# Abstract subtract-zeta estimate: old-node numerator N, denominator L/eta+D;
# perturb numerator by rho*n and leading+regular denominator by relative rho terms.
rho,n,N,L,D,l,e=S.symbols('rho n N L D l e',nonzero=True)
R0=N/(L/eta+D)
RE=(N+rho*n)/((L+rho*l)/eta+D+rho*e)
scaled=S.cancel((RE-R0)/eta)
lim=S.simplify(S.limit(scaled,eta,0))
assert S.simplify(lim-rho*(L*n-N*l)/(L*(L+rho*l)))==0
print('PASS Rayleigh error is eta*O(rho), with exact coefficient',lim)
