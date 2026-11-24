import sympy as s
x=s.symbols('x', positive=True)
a=x**2
F=1+s.Rational(2,3)*a+s.Rational(4,3)*s.sqrt(a*(3-2*a))
Q=(1+x)**2
# F=Q -> 4 sqrt(3-2x^2)=x+6 for x>0
poly=s.expand(16*(3-2*x*x)-(x+6)**2)
print('crossing polynomial:',poly)
print('positive roots:',s.solve(poly,x))
r=(-2+4*s.sqrt(3))/11
print('alpha star:',s.expand(r*r),s.N(r*r,16))
print('crossing value:',s.simplify((1+r)**2),s.N((1+r)**2,16))
print('at 1/6:',s.simplify(F.subs(x,1/s.sqrt(6))))
print('random crossing 2:',s.N((s.sqrt(2)-1)**2))
# red density parameter at crossing
print('red probability across triples:',s.simplify(s.sqrt(3)*r/(1+r)))
