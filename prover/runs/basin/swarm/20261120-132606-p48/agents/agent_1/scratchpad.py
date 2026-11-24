import itertools
import sympy as s

e = s.symbols('e', integer=True, nonnegative=True)
def dot(a, b):
    return s.expand(-e*a[0]*b[0] + a[0]*b[1] + a[1]*b[0])

S, f = (1, 0), (0, 1)
A, B = (5, -1), (-1, 12*e+5)
H, P = (1, 3*e+1), (4, 12*e+3)
C, N = (4, 12*e+4), (1, e)
assert tuple(s.expand(A[i]+B[i]-4*H[i]) for i in range(2)) == (0, 0)
assert dot(A, N) == -1
assert dot(B, f) == -1
assert dot(C, P) == 80*e+28
assert s.expand(P[1]-e*P[0]) == 8*e+3
# A polynomial with nonnegative coefficients and positive constant term
# is strictly positive at every e >= 0.
for polynomial in (80*e+28, 8*e+3):
    coeffs = s.Poly(polynomial, e).all_coeffs()
    assert all(c >= 0 for c in coeffs)
    assert polynomial.subs(e,0) > 0
assert dot(A, B) == 65*e+26
assert dot(C, C) == 80*e+32
print('Intersection and ampleness checks passed.')

# Differential of the incidence map along a disc of projective lines:
# (tau,z) -> (x1(tau),x2(tau),eta1(tau)+eta2(tau)*z,z).
a1,a2,b1,b2,z,eta2 = s.symbols('a1 a2 b1 b2 z eta2')
J = s.Matrix([[a1,0],[a2,0],[b1+b2*z,eta2],[0,1]])
minors = {rows:s.expand(J[list(rows),:].det())
          for rows in itertools.combinations(range(4),2)}
assert minors[(0,3)] == a1
assert minors[(1,3)] == a2
assert minors[(2,3)] == b1+b2*z
for minor in minors.values():
    assert s.expand(minor.subs({a1:0,a2:0,b1:-b2*z})) == 0
print('Incidence rank-one criterion checked:', minors)

# Dimension count: restriction of a Hermitian form with >=3 positive
# directions in C^4 to a complex 2-plane has >=1 positive direction.
for positive_index in (3,4):
    assert positive_index + 2 - 4 >= 1

# Exact formal complex Hessian of inverse squared norm in Chern-normal
# coordinates. Barred coordinates are independent formal variables.
z1,z2,w1,w2,u1,u2,v1,v2 = s.symbols('z1 z2 w1 w2 u1 u2 v1 v2')
zs, ws, us, vs = (z1,z2),(w1,w2),(u1,u2),(v1,v2)
R = [[s.Matrix(2,2,lambda a,b:s.Symbol(f'R{i}{j}{a}{b}'))
      for j in range(2)] for i in range(2)]
rho = u1*v1 + u2*v2
for i,j,a,b in itertools.product(range(2), repeat=4):
    rho -= zs[i]*ws[j]*vs[a]*R[i][j][a,b]*us[b]
psi = 1/rho
r, lam = s.symbols('r lam', positive=True)
at = {z1:0,z2:0,w1:0,w2:0,u1:r,v1:r,u2:0,v2:0}
coords, bars = (z1,z2,u1,u2), (w1,w2,v1,v2)
Levi = s.Matrix(4,4,lambda i,j:
    s.simplify(s.diff(psi,coords[i],bars[j]).subs(at)))
expected = s.zeros(4)
for i,j in itertools.product(range(2), repeat=2):
    expected[i,j] = R[i][j][0,0]/r**2
expected[2,2], expected[3,3] = r**-4, -r**-4
assert s.simplify(Levi-expected) == s.zeros(4)
trace_horizontal = Levi[0,0]+Levi[1,1]
assert s.simplify(trace_horizontal.subs(
    R[1][1][0,0],lam-R[0][0][0,0])) == lam/r**2
print('Full inverse-norm Levi formula checked exactly:')
print(Levi)
print('Positive horizontal trace:', lam/r**2)
print('All checks passed.')
