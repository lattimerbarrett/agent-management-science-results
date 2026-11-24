# Logical consequence of the supplied homogeneity theorem:
# For n >= 2 and 1 <= r < 2*n, uniform E implies invariance
# under every element of PGL(n+1,C).
# The question defines non-homogeneity as failure of that invariance.
import sympy as sp
U, H = sp.symbols('U H')
condition = sp.And(sp.Implies(U, H), U, sp.Not(H))
print('Existence condition compatible with the supplied theorem:', sp.satisfiable(condition))
print('Therefore the defining set is empty, and min(empty) = +infinity.')
