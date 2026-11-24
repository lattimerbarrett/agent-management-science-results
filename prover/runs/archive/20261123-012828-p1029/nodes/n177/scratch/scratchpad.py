import sympy as s
n=s.symbols('n',integer=True,nonnegative=True)
d=s.symbols('delta',positive=True)
eps=d*2**(-n-4)
E=s.summation(eps,(n,0,s.oo))
print('error budget E =',E)
print('uniform lower bound delta - 2*epsilon_0 =',s.simplify(d-2*eps.subs(n,0)))
print('normalizing constant K =',1+E)
print('normalized positive increment lower bound =',s.factor((d-2*eps.subs(n,0))/(1+E)))
