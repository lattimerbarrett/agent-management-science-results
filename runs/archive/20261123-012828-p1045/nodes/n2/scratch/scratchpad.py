import sympy as s
a=s.Rational(1,5)
p=(s.sqrt(3*a-2*a*a)-2*a)/(1-2*a)
structured=s.simplify(3/(1+2*(1-p)**2))
random=(1+s.sqrt(a))**2
print('p =',p)
print('three-part lower bound =',structured, '=',s.N(structured,15))
print('random lower bound =',s.simplify(random),'=',s.N(random,15))
print('difference =',s.N(structured-random,15))