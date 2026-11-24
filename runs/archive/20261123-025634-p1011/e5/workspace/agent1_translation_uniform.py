import sympy as s
x,n,g=s.symbols('x n g');a=n/2;q=x*x-a*a

def anti(F):
 rem=s.Poly(s.cancel(F),x);P=0
 if rem.is_zero:return s.Integer(0)
 for j in range((rem.degree()-1)//2,-1,-1):
  c=s.factor(rem.nth(2*j+1)/(4*(a-j)));P+=c*x**(2*j)
  rem=s.Poly(s.cancel(rem.as_expr()-c*((x+a)**2*(x-1)**(2*j)-(x-a)**2*(x+1)**(2*j))),x)
 assert rem.is_zero
 return P

def mom(F):
 P=anti(x*q*q*F)
 return s.factor(P.subs(x,a)+g*P.subs(x,a+1))
R=2*q/(n-1)-1
A=mom(1);B=mom(R);C=mom(R*R)
L=s.factor(mom(q*4)/(n-1)**2)
M=s.factor((n+1)**2*mom((x*x-(a+1)**2)/(n+1)**2))
# R1_1=2; R3_0=(x²−(a+1)²)/(n+1).
for name,v in [('A',A),('B',B),('C',C),('L',L),('M',M)]:print(name,s.factor(v))
T1=s.factor(B-2*M/(n+3))
T2=s.factor(3*B-(n+3)**2*L/(2*(n+1))-4*n*M/((n+1)*(n+3)))
for name,v in [('T1',T1),('T2',T2)]:
 print(name,s.factor(v))
 numer,denom=s.fraction(v)
 p=s.Poly(numer,g)
 c0,c1=p.nth(0),p.nth(1)
 assert all(c>0 for c in s.Poly(c1.subs(n,n+33),n).all_coeffs())
 assert all(c>0 for c in s.Poly(c0.subs(n,n+33),n).all_coeffs())
 print('PASS:',name,'positive for all n>=33 and all g>0.')
 glo=2/(s.Rational(22,7)*(n+1));ghi=2/(s.Rational(314,100)*n)
 for bound in [glo,ghi]:
  N,D=s.fraction(s.factor(v.subs(g,bound)))
  assert all(c>0 for c in s.Poly(N.subs(n,n+33),n).all_coeffs())
  assert all(c>0 for c in s.Poly(D.subs(n,n+33),n).all_coeffs())
assert s.factor(T2-(n-9)/(n-1)*T1)==0
print('PASS: exact identity T2=(n-9)/(n-1)*T1.')
from pathlib import Path
Path('workspace/agent1_translation_uniform.py').write_text(Path(__file__).read_text())
