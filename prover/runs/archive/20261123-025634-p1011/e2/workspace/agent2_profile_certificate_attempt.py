import sys
sys.path.insert(0,'workspace')
from agent2_symbolic_gram import symbolic_gram,x,q
import sympy as s
from pathlib import Path
v,t,rr=s.symbols('v t rr');m=2*x+1
G=symbolic_gram(2,2);G1=symbolic_gram(1,2);G3=symbolic_gram(3,1)
c=[s.Integer(1),-s.Rational(1,2),s.Rational(1,20)]
P=s.factor(sum((i+j+1)*G[i,j]*c[i]*c[j]*rr**(i+j) for i in range(3) for j in range(3)))
qlo=s.Rational(7,22)*(x+1)**2/(x+s.Rational(3,2));qhi=s.Rational(106,333)*(x+1)

def positive_x(e):
 num,den=s.fraction(s.factor(e))
 nu=s.Poly(num.subs(x,t+s.Rational(23,2)),t);de=s.Poly(den.subs(x,t+s.Rational(23,2)),t)
 if all(a<0 for a in de.all_coeffs()):nu=-nu;de=-de
 return all(a>=0 for a in nu.all_coeffs()) and nu.eval(0)>0 and all(a>=0 for a in de.all_coeffs()) and de.eval(0)>0

def bernstein_positive(e):
 num,den=s.fraction(s.factor(e))
 if den.has(rr):raise ValueError('rr denominator')
 pol=s.Poly(num,rr)
 coeff=[sum(pol.nth(j)*s.binomial(j,k)*s.Rational(7,10)**(j-k)*s.Rational(1,10)**k for j in range(k,pol.degree()+1)) for k in range(pol.degree()+1)]
 d=pol.degree()
 bs=[sum(coeff[j]*s.binomial(k,j)/s.binomial(d,j) for j in range(k+1))/den for k in range(d+1)]
 return [positive_x(s.factor(b)) for b in bs]
for qq in [qlo,qhi]:
 pp=P.subs(q,qq)
 print('scale bracket',positive_x(pp.subs(rr,s.Rational(7,10))),positive_x(-pp.subs(rr,s.Rational(4,5))))
 print('scale concavity Bernstein',bernstein_positive(-s.diff(pp,rr)))
for ak in [(m-1)/(m*(m+1)),(m+1)/(m*(m-1))]:
 T=s.zeros(3)
 for i in range(3):
  for j in range(3):
   T[i,j]=(2+4*i/(m+2))*(2+4*j/(m+2))*ak*(m+2)/2*G1[i,j]
   if i*j:T[i,j]+=4*i*j*(1/(m+4)+2*m*ak/((m+4)*(m+2)))*G3[i-1,j-1]
   if j:T[i,j]+=(2*j+8*j*ak+4*j*(j-1)*(1+4*ak)/(m+4))*G[i,j-1]
 e=-sum(T[i,j]*c[i]*c[j]*rr**(i+j) for i in range(3) for j in range(3))
 for qq in [qlo,qhi]:print('center Bernstein',bernstein_positive(e.subs(q,qq)))
Path('workspace/agent2_profile_certificate_attempt.py').write_text(Path('scratchpad.py').read_text())
