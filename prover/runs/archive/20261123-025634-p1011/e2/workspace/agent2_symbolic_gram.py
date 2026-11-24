import sympy as s
from pathlib import Path
x,z,q=s.symbols('x z q')

def symbolic_gram(l,J):
 a=x+l
 def R(v):
  if v==0:return s.Integer(0)
  return 2**s.Integer(1-v)*s.prod(z-(a-1-t)**2 for t in range(v-1))/(s.factorial(v-1)*s.rf(a+s.Rational(1,2)-v,v-1))
 b=[s.expand(sum((-1)**(j-r)*s.binomial(j,r)*2**r*R(l-1+r) for r in range(j+1))) for j in range(J+1)]
 maxr=2*J+l-2
 U=[s.prod(z-(a-l-1-2*t)**2 for t in range(r)) for r in range(maxr+1)]
 # Output is exact shape Gram / pi, with q=Gamma(x+3/2)^2/(pi Gamma(x+1)^2).
 preE={1:2*q*x*x/(x+s.Rational(1,2))**2,2:2*(x+s.Rational(1,2))**2,3:32*(x+s.Rational(3,2))**2*q}[l]
 preO={1:s.Rational(1,2),2:8*q,3:18*(x+s.Rational(3,2))**2}[l]
 beta=s.Rational(l+1,2)
 moments=[s.factor(4**r*(preE*s.rf(beta,r)*s.rf(a-beta-r,r)+preO*s.rf(beta+s.Rational(1,2),r)*s.rf(a+s.Rational(1,2)-beta-r,r))/(a-l-1-r)) for r in range(maxr+1)]
 G=s.zeros(J+1)
 for i in range(J+1):
  for j in range(i,J+1):
   p=b[i]*b[j]
   if l==1:p*=z-a*a
   if l==3:p=s.cancel(p/(z-(a-1)**2))
   p=s.Poly(s.expand(p),z);v=0
   for r in range(p.degree() if not p.is_zero else -1,-1,-1):
    c=p.nth(r);v+=c*moments[r];p=s.Poly(p.as_expr()-c*U[r],z)
   assert p.is_zero
   G[i,j]=G[j,i]=s.factor(v)
 return G
if __name__=='__main__':
 import sys
 sys.path.insert(0,'workspace')
 from agent1_exact_cross_gram import exact_shape_gram
 for l in [1,2,3]:
  G=symbolic_gram(l,2)
  for n in [21,24,25,30]:
   xx=s.Rational(n-2,2);qq=s.gamma(xx+s.Rational(3,2))**2/(s.pi*s.gamma(xx+1)**2)
   D=G.subs({x:xx,q:qq})*s.pi-exact_shape_gram(n,l,2)
   assert all(s.simplify(v)==0 for v in D)
  print('verified symbolic Gram l=',l)
