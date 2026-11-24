import sympy as s
r=s.symbols('r',positive=True)
g=s.symbols('g',real=True)
new=s.exp(1-1/r**2)*g
print('Radial replacement boundary value:',s.simplify(new.subs(r,1)))
print('Radial replacement boundary normal derivative:',s.simplify(s.diff(new,r).subs(r,1)))
print('Old collar h=e^tau*g has derivative g at tau=0.')
print('Thus identifying tau=r-1 gives equal values but unequal first normal derivatives (2*g versus g). Direct gluing is not smooth under that identification.')
print('A collar reparametrization tau=1-1/r^2 does remove this particular mismatch locally; that alone does not prove the asserted global replacement is available.')
