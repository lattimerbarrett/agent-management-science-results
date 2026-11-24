import sympy as s
p,a=s.symbols('p a', real=True)
R=p**2/3
Bwithin=(1+2*(1-p)**2)/3
Bbetween=(2*(1-p)+(1-p)**2)/3
print('difference:',s.factor(Bwithin-Bbetween))
print('roots:',s.solve(R-a*Bwithin,p))
pstar=(s.sqrt(3*a-2*a*a)-2*a)/(1-2*a)
c=1+2*a/3+4*s.sqrt(3*a-2*a*a)/3
print('constraint check:',s.simplify((R-a*Bwithin).subs(p,pstar)))
print('coefficient check:',s.simplify(c*Bwithin.subs(p,pstar)-1))
p5=s.simplify(pstar.subs(a,s.Rational(1,5)))
c5=s.simplify(c.subs(a,s.Rational(1,5)))
diff=s.simplify(c5-(1+1/s.sqrt(5))**2)
print('p at 1/5:',p5, s.N(p5,18))
print('c at 1/5:',c5,s.N(c5,18))
print('diff at 1/5:',diff,s.N(diff,18))
print('probability boundaries:',s.simplify(pstar.subs(a,s.Rational(1,6)))),s.simplify(pstar.subs(a,s.Rational(1,4)))
