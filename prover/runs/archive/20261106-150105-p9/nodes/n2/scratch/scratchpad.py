import sympy as s
p=s.symbols('p', positive=True)
q=p/(p-1)
# If K is the reducing-operator characteristic, the displayed
# characteristic is comparable (in fixed dimension) to K**p.
# A nonsharp bound K**(p+q) therefore has this exponent:
print('exponent from K^(p+q):', s.simplify((p+q)/p))
print('previous exponent:', s.simplify(1+1/(p-1)-1/p))
print('difference:', s.simplify((p+q)/p-(1+1/(p-1)-1/p)))
