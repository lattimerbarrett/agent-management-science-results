import sympy as s
z,w,e,p,N=s.symbols('z w e p N');D=s.Rational(4,3);A=2;B=s.Rational(41,6);C=-s.Rational(16,3);kap=-s.Rational(5,12);lam=s.Rational(7,12)
def polys(kind,d):
 if kind=='star':
  a1=2*d*w;a2=2*s.binomial(d,2)*w;a3=0
 else:
  def co(k):return sum(s.binomial(k-1,j-1)*s.binomial(d-k+1,j)*2**j*w**j for j in range(1,min(k,d-k+1)+1))
  a1=co(1);a2=co(2);a3=co(3)
 return a1,s.expand(a2-a1*a1/2),s.expand(a3-a1*a2+a1**3/3)
def H(kind,b,extrad):
 a1,b2,b3=polys(kind,7);c1,c2,_=polys(kind,extrad)
 return s.expand(z*(b*a1+c1)*D+s.Rational(1,32)*b2*D**2*z*z),s.expand(b*b2*D**2*z*z+s.Rational(1,32)*b3*D**3*z**3+c2*D**2*z*z)
def poismoment(k):return sum(s.functions.combinatorial.numbers.stirling(k,j,kind=2)*lam**j for j in range(k+1))
def EPo(poly):return sum(v*poismoment(ex[0]) for ex,v in s.Poly(s.expand(poly),N).terms())
def T(P,H):
 return s.simplify(sum(v*EPo(P.subs({e:N+ij[0],p:N+ij[1]},simultaneous=True)) for ij,v in s.Poly(H,z,w).terms()))
def coeffs(offset,kind,b,extrad):
 sp=[x-e*(s.Rational(3,4) if i==0 else -s.Rational(1,4)) for i,x in enumerate(offset)]
 S2=sum(x*x for x in sp);S3=sum(x*x*x for x in sp)
 L1=e*(e+1)/2-A*S2
 L2=e*(e+1)*(2*e+1)/12+kap*e-A*e*S2+B*S2+C*S3
 P1=L1-p*D
 P2=s.expand(L2+L1**2/2-p*D*L1.subs(e,e+1)+p*(p-1)*D**2/2)
 h1,h2=H(kind,b,extrad)
 v1=T(P1,s.Integer(1))+h1.subs({z:1,w:1})
 v2=T(P2,s.Integer(1))+T(P1,h1)+h2.subs({z:1,w:1})+h1.subs({z:1,w:1})**2/2
 return s.simplify(v1),s.simplify(v2)
if __name__=='__main__':
 sa=[s.Rational(1,2)]*2+[-s.Rational(1,2)]*2
 sb=[s.Rational(3,2)]+[-s.Rational(1,2)]*3
 a=coeffs(sa,'star',-s.Rational(21,16),10)
 b=coeffs(sb,'path',-s.Rational(5,16),3)
 assert a[0]==b[0]==-s.Rational(51,16)
 assert b[1]-a[1]==s.Rational(760,27)
 print('star coefficients',a,'path coefficients',b,'ratio second coefficient',b[1]-a[1])
