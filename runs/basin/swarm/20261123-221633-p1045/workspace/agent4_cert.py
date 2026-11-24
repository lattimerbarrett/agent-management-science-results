"""Exact symbolic certificates for book-Ramsey all-blue-type graphon bound."""
import sympy as s
x=s.symbols('x:4', real=True)
lam=s.symbols('lam', real=True)
for k in (3,4):
    xs=x[:k]; S=sum(xs); t=lam*(k-1)/2
    lhs=sum((1-z)**2 for z in xs)+lam*sum(xs[i]*xs[j] for i in range(k) for j in range(i+1,k))
    rhs=k*t/(1+t)+(1-lam/2)*sum((z-S/k)**2 for z in xs)+(1+t)/k*(S-k/(1+t))**2
    assert s.factor(lhs-rhs)==0
X,Y=s.symbols('X Y',real=True)
lhs=(1-X)**2+(1-Y)**2+1+lam*X*Y
rhs=1+2*lam/(2+lam)+(2+lam)/4*(X+Y-4/(2+lam))**2+(2-lam)/4*(X-Y)**2
assert s.factor(lhs-rhs)==0
A=s.symbols('A',positive=True)
optimal_lam=2/s.sqrt(3*A)-2
bound=s.factor(((2+3*lam)/(3*(2+lam))-lam*A).subs(lam,optimal_lam))
assert s.simplify(bound-(1+2*A-4*s.sqrt(A/3)))==0
alpha=s.symbols('alpha',positive=True)
c3=(s.sqrt(3-2*alpha)+2*s.sqrt(alpha))**2/3
p=3*s.sqrt(alpha)/(s.sqrt(3-2*alpha)+2*s.sqrt(alpha))
assert s.simplify(p*p*c3/3-alpha)==0
assert s.simplify(c3*(1+2*(1-p)**2)/3-1)==0
assert s.simplify(c3.subs(alpha,s.Rational(1,6))-2)==0
t=(4*s.sqrt(3)-2)/11
star=s.simplify(t*t)
assert star==(52-16*s.sqrt(3))/121
# Derive exact curve crossover without nested-radical simplification.
# c3 = (1+t)^2 iff sqrt((2-2t-t^2)/2) = 1+(1-sqrt(3))*t.
T=s.symbols('T')
crosspoly=s.expand((1+(1-s.sqrt(3))*T)**2-(2-2*T-T*T)/2)
assert s.simplify(crosspoly.subs(T,t))==0
assert s.ask(s.Q.positive(1+(1-s.sqrt(3))*t))
print('All exact algebraic certificates passed.')
print('alpha_star =',star,'=',s.N(star,16))
print('c3(alpha) =',s.expand(c3))
