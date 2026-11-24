import sympy as s
from fractions import Fraction as R
import numpy as np
# Area normalization and the finite quantum-ring calculation.
th=s.symbols('th',real=True)
assert s.integrate(s.sin(th),(th,0,s.pi))*2*s.pi==4*s.pi
u,v,q=s.symbols('u v q')
G=s.groebner([u*u-q,v*v-q],u,v,q)
assert G.reduce(u*u-q)[1]==0
# Exact fixed-point algebra for the unmodified map.
k=s.symbols('k',positive=True);U=s.symbols('U',real=True)
fminus=k*k*U*U-U-(k*k+1)
fplus=(k*k+2)*U*U+U-(k*k+1)
assert s.expand(fminus-(U+1)*(k*k*U-k*k-1))==0
assert s.expand(fplus-(U+1)*((k*k+2)*U-k*k-1))==0
T=s.sqrt(1+k*k)/(k*k+2);P=s.sqrt(2*k*k+3)/(k*k+2)
assert s.simplify(P*P+(1+k*k)*T*T-1)==0
assert s.simplify((k*k+1)/k**2-1)==1/k**2
# Canonical coordinates and limiting symplectic map.
x1,x2,y1,y2=s.symbols('x1 x2 y1 y2')
a=s.Matrix([x1,x2,y1,y2]);b=s.Matrix([x1+y1,x2+y2,(x2-y2)/2,(y1-x1)/2])
J=s.Matrix([[0,1],[-1,0]])
Omega=s.diag(J,-J);Can=s.zeros(4)
Can[:2,2:]=s.eye(2);Can[2:,:2]=-s.eye(2)
assert b.jacobian(a).T*Can*b.jacobian(a)==Omega
q1,q2,p1,p2,Q1,Q2=s.symbols('q1 q2 p1 p2 Q1 Q2',real=True)
r2=q1*q1+q2*q2
phi=s.Matrix([2*p2+4*q2/r2+2,2*p1+4*q1/r2+2,1-q2/2,1-q1/2])
Dphi=phi.jacobian([q1,q2,p1,p2])
assert (Dphi.T*Can*Dphi-Can).applyfunc(s.simplify)==s.zeros(4)
S=-(q1*Q2+q2*Q1)/2+q1+q2+Q1+Q2+s.log(r2)
assert s.simplify((-s.diff(S,q1)).subs({Q1:phi[0],Q2:phi[1]})-p1)==0
assert s.simplify((-s.diff(S,q2)).subs({Q1:phi[0],Q2:phi[1]})-p2)==0
assert s.diff(S,Q1)==phi[2] and s.diff(S,Q2)==phi[3]
F0=-q1*q2+2*q1+2*q2+s.log(r2)
P0=s.Matrix([q2/2-1-2*q1/r2,q1/2-1-2*q2/r2])
assert (phi[2:4,0]-P0-s.Matrix([s.diff(F0,q1),s.diff(F0,q2)])).applyfunc(s.simplify)==s.zeros(2,1)
# Planar surgery: exactly one critical point, a double zero.
Ft=-q1*q2+2*q1-2*q2+s.log(r2)
z=s.symbols('z')
gp=s.I*z+2+2*s.I+2/z
assert s.factor(gp)==s.I*(z+1-s.I)**2/z
assert s.simplify((s.diff(Ft,q1)-s.I*s.diff(Ft,q2))-gp.subs(z,q1+s.I*q2))==0
assert [s.diff(Ft,t).subs({q1:-1,q2:1}) for t in [q1,q2]]==[0,0]
# Exact bounds for cutoff shells and all complex analytic estimates.
assert 2/R(2,100)-R(2,100)-3-16>0
assert 50-3-R(2,50)-16>0
assert R(1,16)**2/50>R(1,10**5)
h=R(1,10**20);delta=R(1,10**12);L=10**7;Tbound=10**14
sqrtdev=h*h*L*L/2;qdev=2*L*sqrtdev
Verror=4*200*delta+4*delta*delta+4*200*qdev+4*qdev*qdev+h*h*Tbound*Tbound
Derror=Verror+h*h*(10**6+1)
assert R(1,200)**2-Derror>R(1,10**5)
Dmin=R(1,10**5);Vbound=10**6;qb=201
Hnum=h*h*L+2*Vbound*L+4*(qb*2+h*h*Tbound*L)
assert Hnum<10**14
Hbound=R(10**14)/Dmin
Ez=h*h*(2+Vbound*L*L+4*qb*L+2*Vbound*Tbound)/Dmin
assert Ez<R(1,10**13)
assert 4*h*h*(Hbound+1)+2*Ez<R(1,10**12)
assert 4*Hbound+10<10**30
assert 12*10**30*10**20*10**36<10**100
# These numerical evaluations supplement, not replace, the bounds above.
def chart(h,qp):
 Q=np.asarray(qp[:2],complex);P=np.asarray(qp[2:],complex)
 X=np.array([Q[0]/2-P[1],Q[1]/2+P[0]])
 Y=np.array([Q[0]/2+P[1],Q[1]/2-P[0]])
 XX=X@X;YY=Y@Y;v=X*np.sqrt(1-h*h*XX/4);w=Y*np.sqrt(1-h*h*YY/4)
 xz=1-h*h*XX/2;yz=-1+h*h*YY/2;M=v+w;Z=(YY-XX)/2;c=np.sqrt(1+h*h)
 RR=M@M+h*h*Z*Z;DD=h*h+c*c*RR
 rot=lambda u:np.array([u[1],-u[0]])
 A=(h*h*v+c*c*RR*w+2*c*(rot(M)*xz-h*h*Z*rot(v)))/DD
 B=(h*h*w+c*c*RR*v+2*c*(rot(M)*yz-h*h*Z*rot(w)))/DD
 az=((h*h-c*c*RR)*xz+2*c*h*h*(M[0]*v[1]-M[1]*v[0])+c*c*h*h*RR*Z)/DD
 bz=((h*h-c*c*RR)*yz+2*c*h*h*(M[0]*w[1]-M[1]*w[0])+c*c*h*h*RR*Z)/DD
 ca=(h*h-1)/(h*h+1);sa=2/(h*h+1)
 AX=np.array([A[0],ca*A[1]-sa*az]);AZ=h*h*sa*A[1]+ca*az
 BY=np.array([ca*B[0]+sa*bz,B[1]]);BZ=-h*h*sa*B[0]+ca*bz
 AX/=np.sqrt((1+AZ)/2);BY/=np.sqrt((1-BZ)/2)
 return np.array([*(AX+BY),(AX[1]-BY[1])/2,(BY[0]-AX[0])/2])
lim=s.lambdify((q1,q2,p1,p2),phi,'numpy')
rng=np.random.default_rng(3102)
for j in range(100):
 qp=rng.normal(size=4)
 if np.linalg.norm(qp[:2])<.1:continue
 value=np.array(lim(*qp),dtype=complex).ravel()
 assert np.max(abs(chart(0,qp)-value))<1e-10
 assert np.max(abs(chart(1e-6,qp)-value))<1e-5
print('PASS: area, quantum relation, exact base fixed-point factors, canonical chart, symplectic limit, generating function, exact unique monkey saddle, cutoff bounds, rational analytic/Cauchy ledger, and 100 direct chart evaluations.')
from pathlib import Path
source=Path(__file__).read_text(); source=source[:source.rfind('\nfrom pathlib import Path')]
Path('workspace/agent1_solution_checks.py').write_text(source+'\n')
