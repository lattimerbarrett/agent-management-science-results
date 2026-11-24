import sympy as s
from pathlib import Path
k=s.symbols('k')
P=[s.Integer(1),(k*k+21*k+11)/9,(k**4+42*k**3+467*k*k+546*k+264)/144,(k**6+63*k**5+1372*k**4+11319*k**3+22855*k*k+26166*k+10296)/3024]
w0=8400*s.pi/s.factorial(10)**2;w1=23*4*441*(4**11*s.factorial(11)/s.factorial(22))**2/s.pi
A=s.zeros(4)
for i in range(4):
 for j in range(i,4):
  target=s.expand(P[i]*P[j]);R=s.Poly((2*k+21)*target,k);B=0
  for z in range(s.degree(target,k),-1,-1):
   b=R.nth(z+1)/(30-2*z);B+=b*k**z
   R-=s.Poly(b*((k+18)**2*k**z-(k+3)**2*(k+2)**z),k)
  assert R.is_zero
  q=(k+18)**2*B/(2*k+21)
  A[i,j]=A[j,i]=s.factor(w0*q.subs(k,0)+w1*q.subs(k,1))
  print(i,j,A[i,j])
print('numeric matrix');print(A.evalf(15))
l=s.symbols('l');v=s.Matrix([l,l**3,l**5,l**7]);c=s.diag(1,s.Rational(-461,1000),s.Rational(7,125),s.Rational(-693,500000))
E=s.expand((v.T*c*A*c*v)[0]);print('E roots',s.polys.polytools.nroots(s.Poly(s.diff(E,l)/l,l),maxsteps=100))
Path('workspace/agent4_exact_A.txt').write_text(repr(A)+'\n\nEnergy='+str(E))
Path('workspace/agent4_exact_A.py').write_text(Path(__file__).read_text())