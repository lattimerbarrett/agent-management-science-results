import sympy as s
eta=s.symbols('eta',positive=True)
t=eta/2
dmin=s.simplify((eta-t)/(1-t))
C=1/t
scaled_lower=s.simplify(t*dmin)
assert s.simplify(t+(1-t)*dmin-eta)==0
assert s.simplify(t*C-1)==0
assert s.simplify(dmin-eta/(2-eta))==0
assert s.simplify(scaled_lower-eta**2/(2*(2-eta)))==0
print('For 0 < eta <= 1:')
print('cutoff t =',t)
print('dimension lower bound =',dmin)
print('projection partial-sum bound C =',C)
print('After scaling r_n = t*p_n, partial sums <= 1 and')
print('tau(r_n) >=',scaled_lower,'> 0.')
print('The verified exhaustion theorem applies to (r_n) and instead gives tau(r_n) -> 0.')
print('Conclusion: no constant positive eta is possible.')
