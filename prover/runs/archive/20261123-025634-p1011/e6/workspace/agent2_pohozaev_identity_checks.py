from pathlib import Path
import sympy as S
# Radial arbitrary-test-function stress divergence in formal dimension n.
s,n=S.symbols('s n',positive=True)
u=1+s
a=(n-2)/2
q=2*n/(n-2)
F=S.Function('F')(s)
f=S.diff(F,s)
# For u(x)=1+|x|^2: grad u=2x, Delta u=2n.
# J=(x.grad u+a*u) grad u -x(|grad u|^2/2-F)=x*j.
j=2*s+2*a*u+F
divJ=n*j+2*s*S.diff(j,s)
res=divJ-(2*s+a*u)*(2*n+f)
assert S.simplify(res-(n*F-a*u*f))==0
# The dimension-free derivation leaves nF-a*u*f; for F=C*u^q,
# u*f=q*F, so criticality is precisely n=a*q.
assert S.simplify(n-a*q)==0
# Explicit nonradial tests, derivative-based, dimensions 3,4,6.
for N in (3,4,6):
 x=S.symbols('x:'+str(N)); U=1+sum((i+1)*z*z for i,z in enumerate(x))
 aa=S.Rational(N-2,2); QQ=S.Rational(2*N,N-2)
 FF=S.Rational((N-2)**2,2)*U**QQ
 ff=N*(N-2)*U**S.Rational(N+2,N-2)
 DU=[S.diff(U,z) for z in x]
 A=sum(z*d for z,d in zip(x,DU))+aa*U
 norm=sum(d*d for d in DU)
 JJ=[A*d-z*(norm/2-FF) for z,d in zip(x,DU)]
 div=sum(S.diff(j,z) for j,z in zip(JJ,x))
 lap=sum(S.diff(U,z,2) for z in x)
 assert S.expand(div-A*(lap+ff))==0
print('Critical stress divergence checked symbolically in n and nonradially for n=3,4,6.')
Path('workspace/agent2_pohozaev_identity_checks.py').write_text(Path(__file__).read_text())
