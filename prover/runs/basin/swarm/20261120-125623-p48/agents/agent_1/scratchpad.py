import sympy as s

e = s.symbols('e', integer=True, nonnegative=True)
def dot(D, F):
    a, b = D
    c, d = F
    return s.expand(-e*a*c + a*d + b*c)

H = (1, 3*e + 1)
P = (4, 12*e + 3)
A = (5, -1)
B = (-1, 12*e + 5)
C = (1, e)
c1 = tuple(s.expand(x+y) for x, y in zip(A, B))
checks = [
    (dot(P, (1, 0)), 8*e + 3),
    (dot(P, (0, 1)), 4),
    (dot(P, P), 80*e + 24),
    (dot(c1, P), 80*e + 28),
    (dot(C, (1, 0)), 0),
    (dot(C, (0, 1)), 1),
    (dot(A, C), -1),
    (dot(B, (0, 1)), -1),
    (dot(A, B), 65*e + 26),
]
assert c1 == (4, 12*e + 4)
for lhs, rhs in checks:
    assert s.expand(lhs-rhs) == 0
assert (8*e+3).is_positive
assert (80*e+24).is_positive
assert (dot(c1, P)/2).is_positive
print('Intersection identities, ampleness inequalities, and positive slope: checked')

# Universal graph-line evaluation in a fibre chart v=(1,z).
x, y, l1, l2, z = s.symbols('x y l1 l2 z')
ev = s.Matrix([x, y, l1+l2*z, z])
J = ev.jacobian([x, y, l1, l2, z])
assert J.rank() == 4
assert J*s.Matrix([0, 0, 0, 0, 1]) == s.Matrix([0, 0, l2, 1])
assert J*s.Matrix([0, 0, -z, 1, 0]) == s.zeros(4, 1)
assert 3+2-4 == 1
print('Universal evaluation, its kernel, and the dimension count: checked')

# Wirtinger derivatives: barred variables are algebraically independent.
w1, w2, bw1, bw2 = s.symbols('w1 w2 bw1 bw2')
a = s.symbols('a', positive=True)
r = w1*bw1+w2*bw2
Lv = s.Matrix([[s.diff(1/r, u, v) for v in (bw1, bw2)]
               for u in (w1, w2)])
at_w = {w1:a, bw1:a, w2:0, bw2:0}
assert Lv.subs(at_w) == s.diag(a**-4, -a**-4)
print('Vertical Levi eigenvalues: checked by exact differentiation')

# A general horizontal curvature matrix contracted with w=(a,0).
z1, z2, bz1, bz2 = s.symbols('z1 z2 bz1 bz2')
k11, k12, k21, k22 = s.symbols('k11 k12 k21 k22')
K = s.Matrix([[k11, k12], [k21, k22]])
quad = k11*z1*bz1+k12*z1*bz2+k21*z2*bz1+k22*z2*bz2
r_model = (1-quad)*w1*bw1+w2*bw2
zero_base = {z1:0, z2:0, bz1:0, bz2:0}
Lh = s.Matrix([[s.diff(1/r_model, u, v)
                for v in (bz1, bz2)] for u in (z1, z2)])
assert Lh.subs(zero_base).subs(at_w) == K/a**2
mixed = s.Matrix([[s.diff(1/r_model, u, v)
                   for v in (bw1, bw2)] for u in (z1, z2)])
assert mixed.subs(zero_base) == s.zeros(2)
print('Horizontal curvature block and vanishing mixed block: checked')
print('All exact checks passed.')
