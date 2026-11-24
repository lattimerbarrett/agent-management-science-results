import sympy as s
eta=s.symbols('eta', positive=True)
k,r=s.symbols('k r', positive=True, integer=True)
ambient_gap=r*eta/k
corner_dimension=r/k
print('Gap after embedding r copies in M_k(M):',ambient_gap)
print('Gap after normalizing the supporting corner:',s.simplify(ambient_gap/corner_dimension))
u=s.symbols('u', real=True)
print('Two-increment upper-bound certificate:',s.expand((u-eta)+(1-u-eta)))
