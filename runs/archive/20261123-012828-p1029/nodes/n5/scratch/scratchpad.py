import sympy as s
eta,r,N=s.symbols('eta r N', positive=True)
ambient_increment=r*eta/N
corner_weight=r/N
print('Repeated diagonal amplification: ambient increment =', ambient_increment)
print('Normalized corner increment =', s.simplify(ambient_increment/corner_weight))
print('Known attainment covers all eta in (0,1/2).')
print('Two successive increments give 2*eta <= 1; endpoint requires a separate argument.')