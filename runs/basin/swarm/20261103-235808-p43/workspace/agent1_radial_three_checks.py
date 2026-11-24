import sympy as s
k=s.symbols('k',positive=True)
t=s.symbols('t',real=True)
C=k*s.sqrt(1+k*k)
tminus=-1/s.sqrt(1+k*k)
tplus=s.sqrt(1+k*k)/(k*k+2)
pplus=s.sqrt(2*k*k+3)/(k*k+2)
# branch equations after tan(theta/2)=C*r; original unit constraints retain restrictions
Fminus=s.expand(C*(1-k*k*t*t)+k*t)
Fplus=s.expand(C*(1-(k*k+2)*t*t)-k*t)
for name, expr in [('minus_node',Fminus.subs(t,tminus)),('plus_node',Fplus.subs(t,tminus)),('plus_two',Fplus.subs(t,tplus)),('unit',pplus*pplus+(1+k*k)*tplus*tplus-1)]:
 print(name,s.simplify(expr)); assert s.simplify(expr)==0
other=s.sqrt(1+k*k)/k**2
assert s.simplify(Fminus.subs(t,other))==0
print('other minus root exceeds unit bound:',s.simplify(other*other-1/(1+k*k)))
# exact k=1 fixed configurations and numerical Rodrigues checks
import numpy as np
K=1.; cc=K*np.sqrt(1+K*K)
a=2*np.arctan(K)
A=np.array([[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]])
B=np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])
pts=[(0.,-1/np.sqrt(2),0.)]+[(sg*np.sqrt(5)/3,np.sqrt(2)/3,sg*np.sqrt(5)/3) for sg in [-1,1]]
for p,t,q in pts:
 x=np.array([p,t,K*t]); y=np.array([t,q,-K*t]); m=x+y;r=np.linalg.norm(m);u=m/r;theta=2*np.arctan(cc*r)
 def rot(z): return np.cos(theta)*z+np.sin(theta)*np.cross(u,z)+(1-np.cos(theta))*u*np.dot(u,z)
 err=np.linalg.norm(A@rot(x)-x)+np.linalg.norm(B@rot(y)-y)
 print('fixed error',err); assert err<1e-12
open('workspace/agent1_radial_three_checks.py','w').write(open(__file__).read())
r=s.symbols('r',positive=True); aa=s.sqrt(2)*r
for sig in [-1,1]:
 E=r*r*(3*aa*aa+sig*2*s.sqrt(2)*aa+2)-2*(2*aa+sig*s.sqrt(2))**2
 print('E',sig,s.factor(E))
d2,d3,d4=s.symbols('d2 d3 d4');QQ=1+d2*(r*r-1)**2+d3*(r*r-1)**3+d4*(r*r-1)**4
EE=s.expand(r*r*(3*r*r-2*r*QQ+QQ*QQ)-2*(2*r-QQ)**2)
print('E jet at 1', [s.factor(s.diff(EE,r,j).subs(r,1)) for j in range(5)])
# share scalar homogeneous equations
open('workspace/agent1_scalar_equations.txt','w').write('Let signed r range (-sqrt(3),sqrt(3))\\{0}, N,Q polynomials in r^2, tan(theta/2)=sqrt(2)*r*N/Q. Branch q=p roots of E(r)=r^2*(3*r^2*N^2-2*r*N*Q+Q^2)-2*(2*r*N-Q)^2. Positive r corresponds w<0; negative r to w>0. Branch q=-p: z=r^2 in [1,2], roots of B(z)=(2-z)*Q(z)^2-z^2*N(z)^2. Interior roots contribute two points, z=1 node contributes one already counted in E. For N=1 no numerator/denominator degeneracies. Exactly2 requires E has exactly two distinct real roots in signed interval and B only z=1. All coefficient arithmetic rational.')
