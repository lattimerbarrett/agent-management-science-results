import sympy as sp
eta, u, t = sp.symbols('eta u t', real=True)
print('Upper-bound certificate:', sp.expand((u-eta)+(1-u-eta)))
print('Scaling identity:', sp.expand(t*eta))
print('Trace obstruction: N*eta <= 1 for every positive integer N is impossible for eta > 0.')