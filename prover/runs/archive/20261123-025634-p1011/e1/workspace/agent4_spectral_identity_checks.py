"""Exact checks for auxiliary identities in agent4_spectral_full_proof.md."""
import sympy as s
z=s.symbols('z',positive=True)
L,n=s.symbols('L n',positive=True)
f=s.Function('f')(z)
v=z**(L/2)*f
radial=4*z*(1-z)*s.diff(v,z,2)+(2*n-2*(n+1)*z)*s.diff(v,z)+(n-L*(L+n-2)/z)*v
a=(L-1)/2;b=(L+n)/2;c=L+n/2
hyp=4*z**(L/2)*(z*(1-z)*s.diff(f,z,2)+(c-(a+b+1)*z)*s.diff(f,z)-a*b*f)
assert s.simplify(radial-hyp)==0
count=0
for alpha in [9,10,11]:
 for p in [1,2,3,4]:
  for k in range(9):
   # All exponents are nonnegative integers, so this is exact polynomial integration.
   integrand=s.Poly(s.expand((1-z)**alpha*(1+z)**(alpha-p)*s.jacobi(k,alpha,alpha,z)),z)
   value=sum(coeff*s.Rational(1-(-1)**(degree+1),degree+1) for (degree,),coeff in integrand.terms())
   claimed=(-1)**k*2**(2*alpha-p+1)*s.factorial(k+alpha)*s.factorial(alpha-p)*s.factorial(k+p-1)/(s.factorial(p-1)*s.factorial(k)*s.factorial(k+2*alpha-p+1))
   assert value==claimed,(alpha,p,k,value,claimed)
   count+=1
for alpha in [9,10,11]:
 for k in range(6):
  poly=s.Poly(s.expand((1-z*z)**alpha*s.jacobi(k,alpha,alpha,z)**2),z)
  value=sum(coeff*s.Rational(1-(-1)**(degree+1),degree+1) for (degree,),coeff in poly.terms())
  claimed=s.Rational(2**(2*alpha+1),2*k+2*alpha+1)*s.factorial(k+alpha)**2/(s.factorial(k)*s.factorial(k+2*alpha))
  assert value==claimed
m=s.symbols('m',positive=True)
M2=1/m;M4=3/(m*(m+2));M6=15/(m*(m+2)*(m+4))
assert s.simplify(M4-2*M2/m+1/m**2-2*(m-1)/(m*m*(m+2)))==0
assert s.simplify(M6-6*M4/(m+2)+9*M2/(m+2)**2-6*(m-1)/(m*(m+2)**2*(m+4)))==0
print('PASS: all-n radial-to-hypergeometric identity;',count,'exact Jacobi moments;18 exact Jacobi norms;angular norm formulas.')

# Exact transfer from target-normalized Euclidean action to unit hemisphere.
A=4*(n-1)/(n-2); cn=(n-2)/(4*(n-1))
assert s.simplify(A*cn-1)==0
assert s.simplify(A*n*(n-2)-4*n*(n-1))==0
assert s.simplify(2/(A*A*2**(n-2))-2**(3-n)/A**2)==0
assert s.simplify((2**(3-n)/A**2).subs(n,19))==s.Rational(289,339738624)
print('PASS: exact all-n conformal action normalization; n19 coefficient289/339738624.')
