import sympy as s
# Scalar version of the quadratic Schur-complement identity. The identical
# calculation holds for a self-adjoint Jacobi operator on its kernel complement.
A,e,w,d=s.symbols('A e w d', nonzero=True)
e_new=e+A*w
d_new=d+2*e*w+A*w*w
full=s.simplify(d_new-e_new**2/A-(d-e**2/A))
omitted=s.simplify(-e_new**2/A-(-e**2/A))
print('Full quadratic coefficient change under moving-base identification:',full)
print('Change if the direct quadratic term is discarded:',omitted)
print('Necessary compensating direct term:',s.expand(d_new-d))
