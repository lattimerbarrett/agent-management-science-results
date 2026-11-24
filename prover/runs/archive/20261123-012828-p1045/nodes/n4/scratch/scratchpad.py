import sympy as s
a=s.symbols('a', positive=True)
p=3*a/(s.sqrt(3*a-2*a*a)+2*a)
L=1+s.Rational(2,3)*a+s.Rational(4,3)*s.sqrt(3*a-2*a*a)
print('p relation:',s.simplify(p**2-a*(1+2*(1-p)**2)))
print('bound relation:',s.simplify(L*(1+2*(1-p)**2)-3))
for x in [s.Rational(1,6),s.Rational(1,5),s.Rational(1,4),s.Integer(1)]:
    print('alpha:',x,'three-part bound:',s.simplify(L.subs(a,x)), 'random bound:',s.simplify((1+s.sqrt(x))**2))
print('These calculations verify constructions only, not upper bounds or existence of a limit.')