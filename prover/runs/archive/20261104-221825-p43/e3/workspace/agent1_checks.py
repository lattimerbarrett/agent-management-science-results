import sympy as s
from pathlib import Path
# Preserve this reproducible verification script for the team.
Path('workspace/agent1_checks.py').write_text(Path(__file__).read_text())
k=s.symbols('k', positive=True)
x=s.Matrix([-k,-1,0]); y=s.Matrix([0,1,-k]); w=x+y
v=s.Matrix([-k,1,0]) # A^{-1}x
# Use vectors before common sqrt(1+k²) normalization
r2=s.simplify(w.dot(w)/(1+k*k))
perp2=s.simplify(x.dot(x)-x.dot(w)**2/w.dot(w))
cosine=s.factor((x.dot(v)-x.dot(w)*v.dot(w)/w.dot(w))/perp2)
sine=s.factor(w.dot(x.cross(v))/s.sqrt(w.dot(w))/perp2)
assert s.simplify(r2-2*k*k/(1+k*k))==0
assert s.simplify(cosine-(k*k-2)/(k*k+2))==0
assert s.simplify(sine-2*s.sqrt(2)*k/(k*k+2))==0
assert s.simplify(cosine**2+sine**2-1)==0
# For finite positive k, sine positive => angle !=0,pi.
assert sine.is_positive
print('Verified exact crossing radius and rotation phase:',r2,cosine,sine)
# Check an admissible explicit upper-bound-four Hamiltonian.
x1,x2,x3,alpha=s.symbols('x1 x2 x3 alpha', real=True)
xx=s.Matrix([x1,x2,x3]); e3=s.Matrix([0,0,1]); X=alpha*e3.cross(xx)
assert s.expand(xx.dot(X))==0
assert s.simplify(xx.cross(X)-alpha*(e3-xx[2]*xx)) == s.Matrix([0,0,alpha*(x1*x1+x2*x2+x3*x3-1)])
angle=s.pi/2
RR=s.Matrix([[s.cos(angle),-s.sin(angle),0],[s.sin(angle),s.cos(angle),0],[0,0,1]])
assert (RR-s.eye(3)).nullspace()==[e3]
assert s.solve([x1,x2,x3*x3-1],[x1,x2,x3])==[(0,0,-1),(0,0,1)]
print('Checked Hamiltonian vector field and exactly four product-rotation fixed points.')
# Exact 2 fixed swap map has cohomological Lefschetz index2 vs Ham4.
T=s.Matrix([[0,1],[1,0]])
I=s.eye(2)
assert 1+s.trace(T)+1==2
assert 1+s.trace(I)+1==4
assert T*T==I
print('Verified swap action on H2, non-Hamiltonian obstruction, square trivial H2.')
U,T,Z,p,q=s.symbols('U T Z p q', nonzero=True, real=True)
v=s.Matrix([p,0,q]); d=s.Matrix([-Z*q/T,(T*T+Z*Z)*q/(U*T),Z*p/T]); xx=(v+d)/2
AA=s.Matrix([[1-2*Z*Z,-2*U*Z,2*T*Z],[2*U*Z,1-2*(T*T+Z*Z),-2*U*T],[2*T*Z,2*U*T,1-2*T*T]])
print('BranchII cross numerator',s.factor(v.dot(xx.cross(AA*xx))))
print('BranchII 1-cos numerator',s.factor(xx.dot(xx)-xx.dot(AA*xx)))
import numpy as np
from scipy.optimize import root_scalar
U0=np.sqrt(np.pi/4); Z0=(1-U0**2)/U0; T0=np.sqrt(1-U0**2-Z0**2); L0=1-U0**2
r0=2*T0*U0/np.sqrt(L0); theta0=np.pi/2; u0=theta0/r0
Rprime=T0*Z0/L0**1.5
Rsecond=T0/2*(-U0/L0**1.5+3*U0*Z0**2/L0**2.5)
# derivative of thetaIplus wrt r
D=np.sqrt(1-T0*T0); e=r0*T0/(D*np.sqrt(4-r0*r0)); ep=4*T0/(D*(4-r0*r0)**1.5)
theta_r=2*ep/np.sqrt(1-e*e)
u1=(theta_r-2*u0)/r0
Fsecond=-Rsecond*u0*u0-Rprime*u1
print('Resonance target',dict(U=U0,Z=Z0,T=T0,r=r0,u=u0,Rprime=Rprime,check=Rprime*u0,theta_r=theta_r,u1=u1,Fsecond=Fsecond))
delta0=np.arctan2(Z0,U0)
import mpmath as mp
mp.mp.dps=50
TT=mp.sqrt(1-mp.pi/4-(1-mp.pi/4)**2/(mp.pi/4)); DD=mp.sqrt(1-TT*TT)
RR=2*TT*mp.sqrt(mp.pi/4)/mp.sqrt(1-mp.pi/4)
cc=lambda rr: 2*mp.atan((1-mp.pi/4)/(mp.pi/4))+2*mp.asin(rr*TT/(DD*mp.sqrt(4-rr*rr)))
aa1=(mp.pi/2)/RR
aa2=(mp.diff(cc,RR)-2*aa1)/RR
aa3=(mp.diff(cc,RR,2)-3*aa2)/RR
aa4=(mp.diff(cc,RR,3)-4*aa3)/RR
print('h0 ODE jets',*[float(t) for t in [aa1,aa2,aa3,aa4]])
for u2 in [-10,0,10]:
 for dx in [-.001,.001]:
  r=r0+dx; a=u0*dx+u1*dx*dx/2+u2*dx**3/6; ap=u0+u1*dx+u2*dx*dx/2
  U=U0*np.cos(a/2)+Z0*np.sin(a/2); Z=Z0*np.cos(a/2)-U0*np.sin(a/2); L=1-U*U
  q=U*np.sqrt(4*T0*T0-L*r*r)/L
  thetaI=2*(delta0-a/2)+2*np.arcsin(r*T0/(D*np.sqrt(4-r*r)))
  thetaII=2*np.arctan(q*L/(U*Z*r))
  h=thetaI-ap*r; g=thetaII-ap*q
  print('jet',u2,dx,'h/x²',h/dx**2,'g/x²',g/dx**2,'q-r',(q-r)/dx**2)
