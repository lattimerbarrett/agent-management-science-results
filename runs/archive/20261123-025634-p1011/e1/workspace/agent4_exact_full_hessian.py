import sympy as s
from pathlib import Path
k=s.symbols('k'); lam=s.symbols('lam'); pi=s.pi
w0=8400*pi/s.factorial(10)**2;w1=23*4*441*(4**11*s.factorial(11)/s.factorial(22))**2/pi

def total(target):
 target=s.expand(target)
 if target==0:return s.Integer(0)
 R=s.Poly((2*k+21)*target,k);B=0
 for z in range(s.degree(target,k),-1,-1):
  b=R.nth(z+1)/(30-2*z);B+=b*k**z
  R-=s.Poly(b*((k+18)**2*k**z-(k+3)**2*(k+2)**z),k)
 assert R.is_zero
 q=(k+18)**2*B/(2*k+21)
 return s.factor(w0*q.subs(k,0)+w1*q.subs(k,1))
P=[s.Integer(1),(k*k+21*k+11)/9,(k**4+42*k**3+467*k*k+546*k+264)/144,(k**6+63*k**5+1372*k**4+11319*k**3+22855*k*k+26166*k+10296)/3024]
x=k+1
R1=[s.Integer(0),s.Integer(2),(x*x+19*x+2)/4,(x+1)*(x+2)*(x+17)*(x+18)/56-3*(x+1)*(x+18)/4+6]
x=k-1
R3=[s.Integer(1),(x+2)*(x+21)/18-1,(x+2)*(x+3)*(x+20)*(x+21)/432-(x+2)*(x+21)/9+1]
A1=s.Matrix(4,4,lambda i,j:total((k+1)*(k+20)*R1[i]*R1[j]/324))
A2=s.Matrix(4,4,lambda i,j:total(P[i]*P[j]))
A3=s.Matrix(3,3,lambda i,j:total(k*(k+21)*R3[i]*R3[j]))
c=[s.Integer(1),s.Rational(-461,1000),s.Rational(7,125),s.Rational(-693,500000)]
v=s.Matrix([c[j]*lam**(2*j+1) for j in range(4)])
m=s.Integer(18);N1=1/m;N2=2*(m-1)/(m*m*(m+2));N3=6*(m-1)/(m*(m+2)**2*(m+4))
b=[2*(m-1)/m+4*j*(m-1)/(m*(m+2)) for j in range(4)]
u1=s.Matrix([b[j]*v[j] for j in range(4)]);u3=s.Matrix([2*j*v[j] for j in range(1,4)])
k2=[2*j*b[j]+6*j*m/(m+2)+12*j*(j-1)*m/((m+4)*(m+2)) for j in range(4)]
sec=s.Matrix([k2[j]*v[j] for j in range(1,4)]+[0])
Hpar=s.expand(2*(N1*(u1.T*A1*u1)[0]+N3*(u3.T*A3*u3)[0]+N2*(v.T*A2*sec)[0]))
u1sum=s.Matrix([(1+2*j/(m+2))*v[j] for j in range(4)])
lap=s.Matrix([2*j*(m+2*j+2)*v[j] for j in range(1,4)]+[0])
Htrace=s.expand(2*N2*(2*(m+2)*(u1sum.T*A1*u1sum)[0]+m/(m+2)*(u3.T*A3*u3)[0]+(v.T*A2*lap)[0]))
Hper=s.expand((Htrace-Hpar)/(m-1))
E=s.expand(N2*(v.T*A2*v)[0]);Hscale=s.diff(E,lam,2)
C=s.factorial(9)**2/4
for name,h in [('E',E),('Hscale',Hscale),('Hpar',Hpar),('Hper',Hper)]:
 print(name,(C*h).subs(lam,s.Rational(9519023235,10**10)).evalf(18))
Path('workspace/agent4_exact_full_hessian.txt').write_text('A1='+repr(A1)+'\nA2='+repr(A2)+'\nA3='+repr(A3)+'\nE='+str(E)+'\nHscale='+str(Hscale)+'\nHpar='+str(Hpar)+'\nHper='+str(Hper))
from fractions import Fraction as F

def atan_bounds(q,terms):
 a=sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(terms)),F(0))
 nxt=F((-1)**terms,(2*terms+1)*q**(2*terms+1))
 return min(a,a+nxt),max(a,a+nxt)
a0,a1=atan_bounds(5,60);b0,b1=atan_bounds(239,20)
pl,ph=16*a0-4*b1,16*a1-4*b0

def rat(x):
 x=s.Rational(x);return F(int(x.p),int(x.q))
def mul(iv,jv):
 vals=[a*b for a in iv for b in jv];return min(vals),max(vals)
def bounds(h,lo,hi):
 out=(F(0),F(0))
 for (degree,),cc in s.Poly(s.expand(C*h),lam).terms():
  cp=s.expand(cc*pi)
  aa=rat(cp.coeff(pi,2));bb=rat(cp.subs(pi,0))
  assert s.simplify(cp-aa*pi*pi-bb)==0
  x=mul((aa,aa),(pl,ph));y=mul((bb,bb),(1/ph,1/pl))
  coeff=(x[0]+y[0],x[1]+y[1]);term=mul(coeff,(lo**degree,hi**degree))
  out=(out[0]+term[0],out[1]+term[1])
 return out
lo=F(951902323,10**9);hi=F(951902324,10**9)
left=bounds(s.diff(E,lam),lo,lo);right=bounds(s.diff(E,lam),hi,hi)
assert left[0]>0 and right[1]<0
print('CERTIFIED Eprime endpoint signs:',[float(t) for t in left],[float(t) for t in right])
for name,h,sgn in [('Hscale',Hscale,-1),('Hpar',Hpar,-1),('Hper',Hper,-1)]:
 iv=bounds(h,lo,hi)
 assert (iv[0]>0 if sgn>0 else iv[1]<0)
 print('CERTIFIED',name,tuple(float(t) for t in iv))
print('Thus a unique scale-critical root in [0.951902323,0.951902324] has nondegenerate full Hessian.')
Path('workspace/agent4_exact_full_hessian.py').write_text(Path(__file__).read_text())