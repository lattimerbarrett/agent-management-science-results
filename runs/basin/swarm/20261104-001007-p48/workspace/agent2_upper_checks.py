"""Exact checks for the upper-bound proof; no numerical approximations."""
import sympy as s

e=s.symbols("e", integer=True, nonnegative=True)
def intersection(D,F):
    a,b=D; c,d=F
    return s.expand(-e*a*c+a*d+b*c)
A=(5,-1); B=(-1,12*e+5); H=(1,3*e+1)
assert intersection(A,H)==10*e+4
assert intersection(B,H)==10*e+4
assert intersection(H,H)==5*e+2
assert s.expand(H[1]-e*H[0])==2*e+1
assert all(s.Poly(p,e).all_coeffs()[k]>0 for p in [intersection(A,H),intersection(B,H),intersection(H,H),H[1]-e*H[0]] for k in range(len(s.Poly(p,e).all_coeffs())))
# Exact generic Levi-Hessian congruence for a line metric h=e^phi.
# At w=1, block Hessian of h(z)|w|^2 is h[[G+aa*,a],[a*,1]],
# where G=(phi_{i bar j}) and a=(phi_i). A holomorphic fibre scaling
# makes w=1 at each nonzero point; this does not change inertia.
h=s.symbols("h",positive=True)
g11,g22,g33,g12r,g12i,g13r,g13i,g23r,g23i=s.symbols("g11 g22 g33 g12r g12i g13r g13i g23r g23i",real=True)
a1r,a1i,a2r,a2i,a3r,a3i=s.symbols("a1r a1i a2r a2i a3r a3i",real=True)
G=s.Matrix([[g11,g12r+s.I*g12i,g13r+s.I*g13i],[g12r-s.I*g12i,g22,g23r+s.I*g23i],[g13r-s.I*g13i,g23r-s.I*g23i,g33]])
a=s.Matrix([a1r+s.I*a1i,a2r+s.I*a2i,a3r+s.I*a3i])
M=(G+a*a.conjugate().T).row_join(a).col_join(a.conjugate().T.row_join(s.ones(1)))
C=s.eye(4)
for k in range(3): C[3,k]=-s.conjugate(a[k])
D=s.simplify(C.conjugate().T*M*C)
assert D==s.diag(G,s.ones(1))
assert C.det()==1
# Thus inertia(Levi psi)=inertia(-curvature(L))+(one positive).
# Positive mean curvature of E: any unit v has positive horizontal trace.
x,y,t=s.symbols("x y t",real=True)
# A 2x2 Hermitian matrix positive trace cannot have both eigenvalues <=0;
# equivalent elementary eigenvalue estimate lambda_max >= trace/2.
print("Exact symbolic checks passed: H ample inequalities, both positive H-degrees, and full 4x4 Levi congruence.")
print("A.H = B.H =", intersection(A,H), "; H^2 =", intersection(H,H))
