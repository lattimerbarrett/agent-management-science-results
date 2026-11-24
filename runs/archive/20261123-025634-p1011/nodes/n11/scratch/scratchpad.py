import sympy as s
m, a, H, q = s.symbols('m a H q', nonzero=True)
# g_tilde=e^(2f)g, a=e^f, q=nu(f).
# Express the coefficient of h in the trace-free second fundamental form.
coefficient = s.simplify(a*q - (H+m*q)/a * a**2/m)
print('II_tilde^0 = a*II + (coefficient)*h, coefficient =', coefficient)
print('Thus II_tilde^0 = a*(II - H*h/m).')
print('Conformal flattening therefore does not remove nonumbilicity.')
