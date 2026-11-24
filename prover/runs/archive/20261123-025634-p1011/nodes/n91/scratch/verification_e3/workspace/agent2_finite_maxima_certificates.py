import sympy as s,sys
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_general_blocks import polynomial_interval
M,k,r=s.symbols('M k r')
WITNESSES=s.sympify(Path('workspace/agent2_finite_profiles.txt').read_text())

def blocks(n,J=3):
 alpha=s.Rational(n+2,2)
 def telescope(P,p):
  b=s.Rational(p+3,2);c=s.Rational(p+n+1,2)
  rem=s.expand((2*k+p+alpha)*P.subs(M,2*k+p));A=0
  for v in range(s.degree(P,M),-1,-1):
   L=s.expand((k+c-1)**2*k**v-(k+b)**2*(k+1)**v)
   av=s.expand(rem).coeff(k,v+1)/L.coeff(k,v+1)
   A+=av*k**v;rem=s.expand(rem-av*L)
  assert rem==0
  return 16*s.gamma(b)**2/s.gamma(c-1)**2*s.expand(A).coeff(k,0)
 def matrix(ell):
  al=s.Rational(n-2,2)+ell;m=M-ell+2
  def I(q):
   return 2**(2*al-q)*s.gamma(al-q+s.Rational(1,2))*s.gamma(al+s.Rational(1,2))/s.gamma(2*al)/s.gamma(q)*s.rf(m+1,q-1)*s.rf(m+2*al-q+1,q-1)
  Is=[s.expand(sum((-1)**(j-q)*s.binomial(j,q)*2**q*I(ell-1+q) for q in range(j+1) if ell-1+q>=1)) for j in range(J+1)]
  R={1:(M+1)*(M+n+1)/(4*(alpha-1)**2),2:s.Integer(1),3:4*alpha**2/(M*(M+n+2))}[ell]
  Q=s.zeros(J+1)
  for i in range(J+1):
   for j in range(i,J+1):
    P=s.cancel(R*Is[i]*Is[j]);assert not s.denom(P).has(M)
    Q[i,j]=Q[j,i]=s.factor(telescope(s.expand(P),0)+telescope(s.expand(P),1)) if P!=0 else 0
  return Q
 return [None]+[matrix(ell) for ell in range(1,4)]

def interval_const(v):
 num,den=s.fraction(s.factor(v));nl,nh=polynomial_interval(num);dl,dh=polynomial_interval(den)
 assert dl>0 or dh<0
 vs=[nl/dl,nl/dh,nh/dl,nh/dh]
 return min(vs),max(vs)

def interval(poly,lo,hi):
 anslo=anshi=s.Integer(0)
 for (p,),v in s.Poly(s.expand(poly),r).terms():
  vl,vh=interval_const(v);vv=[vl*lo**p,vl*hi**p,vh*lo**p,vh*hi**p]
  anslo+=min(vv);anshi+=max(vv)
 return anslo,anshi

def certificate(n):
 Qs=blocks(n);Q=Qs[2]
 a=s.Matrix(WITNESSES[n][0])
 c=s.Matrix([a[j]*r**j for j in range(4)])
 D=s.expand(sum((i+j+1)*Q[i,j]*c[i]*c[j] for i in range(4) for j in range(4)))
 lo,hi=WITNESSES[n][1:]
 assert interval_const(D.subs(r,lo))[0]>0
 assert interval_const(D.subs(r,hi))[1]<0
 assert interval(s.diff(D,r),lo,hi)[1]<0
 Fp=s.Matrix([c[j+1]*(j+1) if j<3 else 0 for j in range(4)])
 sFpp=s.Matrix([c[j+1]*(j+1)*j if j<3 else 0 for j in range(4)])
 d=n-1;Lrad=s.Matrix([c[j]*(1+s.Rational(2*j,d+2)) for j in range(4)])
 for b in [s.Rational(0),s.Rational(1)]:
  G=(2+8*b)*Fp+(4+16*b)/(d+4)*sFpp
  normL=b*(d+2)/2;normT=s.Rational(1,d+4)+2*d*b/((d+4)*(d+2))
  H=s.expand(4*normL*(Lrad.T*Qs[1]*Lrad)[0]+4*normT*(Fp.T*Qs[3]*Fp)[0]+(c.T*Qs[2]*G)[0])
  assert interval(H,lo,hi)[1]<0
 print('CERTIFIED full model strict maximum',n,'profile',list(a),'scale bracket',lo,hi,flush=True)
 return list(a),lo,hi
if __name__=='__main__':
 result={n:certificate(n) for n in range(19,40)}
