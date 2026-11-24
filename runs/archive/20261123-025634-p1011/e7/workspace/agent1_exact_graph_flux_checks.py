import sympy as s
r=s.symbols('r',positive=True)
for n in range(3,11):
 a=s.Rational(n-2,2); beta=s.Rational(n-2,2*(n-1)); c=beta/2
 V=(1+r*r)**(-(n-2))
 for j in range(2,9):
  I=r**(n-2)*(-beta*j*(j+n-3)*r**(j-2)*(r*s.diff(V,r)/2+a*V)
      -2*a*a*(j-1)*r**(j+2)*V/(1+r*r)**2
      +2*a*a*(j-1)*r**j*V/(1+r*r)**2)
  edge=c*(-(j-1)*r**(j+n-2)*s.diff(V,r)-j*(n-2)*r**(j+n-3)*V)
  assert s.cancel(s.diff(edge,r)-I)==0,(n,j)
  assert s.limit(edge,r,0)==0
  coeff=s.limit(edge/r**(j+1-n),r,s.oo)
  assert coeff==s.Rational((n-2)**2*(j-2),4*(n-1)),(n,j,coeff)
# General graph outward-normal algebra with arbitrary formal variables.
S,T,beta,w,zDu,F,wt,a,Dw2,kappa,wq=s.symbols('S T beta w zDu F wt a Dw2 kappa wq')
normal_derivative_times_area=-beta*T*w
xdu=zDu+F*wt
flux=(a*w+xdu)*normal_derivative_times_area-S*Dw2/2+kappa*S*wq
assert s.expand(flux-(-beta*T*w*(zDu+F*wt+a*w)-S*Dw2/2+kappa*S*wq))==0
print('Exact outward graph flux and 56 radial edge identities/asymptotic coefficients checked')
