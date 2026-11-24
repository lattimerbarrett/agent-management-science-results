import sympy as s
from pathlib import Path
for n in range(4,11):
 d=n-1
 # Linearized metric variation h_ab=t² B_ab with tracefree B diagonal.
 diag=[s.Integer(1),s.Integer(-1)]+[s.Integer(0)]*(d-2)
 delta=lambda i,j:s.Integer(i==j)
 B=lambda i,j:diag[i]*delta(i,j) if i<d and j<d else s.Integer(0)
 # R_{a n b n}= -B_ab; generate tensor by standard symmetries.
 def R(i,j,k,l):
  if j==d and l==d and i<d and k<d:return -B(i,k)
  if i==d and l==d and j<d and k<d:return B(j,k)
  if j==d and k==d and i<d and l<d:return B(i,l)
  if i==d and k==d and j<d and l<d:return -B(j,l)
  return s.Integer(0)
 Ric=s.Matrix(n,n,lambda j,l:sum(R(i,j,i,l) for i in range(n)))
 scalar=s.trace(Ric)
 Sch=(Ric-scalar/(2*(n-1))*s.eye(n))/(n-2)
 def W(i,j,k,l):return s.simplify(R(i,j,k,l)-(Sch[i,k]*delta(j,l)-Sch[i,l]*delta(j,k)-Sch[j,k]*delta(i,l)+Sch[j,l]*delta(i,k)))
 assert scalar==0
 assert all(s.simplify(W(a,d,b,d)+s.Rational(n-3,n-2)*B(a,b))==0 for a in range(d) for b in range(d))
 assert W(0,d,0,d)!=0
print('Actual linearized Riemann/Ricci/Weyl contractions checked n4..10: W_anbn=−(n−3)/(n−2)B_ab.')
Path('workspace/agent4_mixed_normal_Weyl_checks.py').write_text(Path(__file__).read_text())
