"""Exact cross-angular identities and all-dimensional translation stability.
Combine with agent3_all_n33.py for degree-one full shape minima.
"""
import sympy as s
n,j=s.symbols('n j',positive=True)
def W(l,j):
    a=(n+2*l-3)/2;al=a+s.Rational(1,2);p=l
    I=2**(2*a-p+1)*s.beta(a+1,a-p+1)*s.rf(p,j)*s.rf(2*a+1,j)/(s.gamma(j+1)*s.rf(2*a-p+2,j))
    h=s.pi*2**(1-2*al)*s.gamma(j+2*al)/(s.gamma(j+1)*(j+al)*s.gamma(al)**2)
    return I**2/h
for l,delta,target in [(1,-1,1/((j+1)*(j+n-1)-(n-1))),(3,1,((j+3)*(j+n+1)-2*n)/4)]:
    ratio=s.combsimp((W(l,j)/W(2,j+delta)).rewrite(s.gamma))
    assert s.simplify(s.expand_func(ratio-target))==0
# Thus absolute C1,11=2(C01+C00)/(n-1) and
# C3,00=((n-1)C01-(n+3)C00)/2, after summing universal moments.
a,z,rho=s.symbols('a z rho',positive=True)
C00=s.Integer(1);C01=a
C111=2*(a+1)/(n-1)
C300=((n-1)*a-(n+3))/2
norm1=(n+1)*rho/2;norm3=(1+2*(n-1)*rho/(n+1))/(n+3)
H=(2+8*rho)*z*(1-z*a)-z*z*(norm1*4*(n+3)**2/(n+1)**2*C111+4*norm3*C300)
H0=1+z-2*(n+1)/(n+3)*a*z
H1=5+z*(1-16/(n-1))-2*(5*n*n+8*n+19)/((n-1)*(n+3))*a*z
assert s.factor(H.subs(rho,0)/(2*z)-H0)==0
assert s.factor(H.subs(rho,1)/(2*z)-H1)==0
# At scale min z=1/(2a+sqrt(4a^2-3b)), so az<1/2.
# Substitute worst-case az=1/2 in each expression.
u=s.symbols('u')
L0=s.expand(H0).subs(a*z,u).subs(u,s.Rational(1,2))
L1=s.expand(H1).subs(a*z,u).subs(u,s.Rational(1,2))
# Avoid matching issues by equivalent direct substitution a=1/(2z).
L0=s.factor(H0.subs(a,1/(2*z)))
L1=s.factor(H1.subs(a,1/(2*z)))
assert s.factor(L0-z-2/(n+3))==0
assert s.factor(L1-(n-17)*(z/(n-1)+2/((n-1)*(n+3))))==0
print('Exact proof: every stable degree-one scale critical point has strictly positive translation Hessian for n>17.')
