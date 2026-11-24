import sympy as s
u,v,eps=s.symbols('u v eps', nonnegative=True, positive=True)
# Uniform block estimate for X-P_n, with
# X = (y+eps*e) + (1+1/eps)*(1-e).
# Top block >= eps, bottom block >= 1/eps, off-diagonal norm <= 1.
q=eps*u**2-2*u*v+v**2/eps
print('Compression certificate:', s.factor(q))
print('Difference from square:',s.simplify(q-(s.sqrt(eps)*u-v/s.sqrt(eps))**2))
print('Therefore X >= P_n for every n; an ambient self-adjoint supremum P gives ePe <= y+eps*e, then ePe <= y.')
