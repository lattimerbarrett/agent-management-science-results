# Audit a non-reductive automorphism kernel: E = O + O(1) on P^2.
# A global endomorphism is [[a, 0], [ell(x), d]], with ell linear.
import sympy as s
a,d,u,v,w,x,y,z=s.symbols('a d u v w x y z')
M=s.Matrix([[a,0],[u*x+v*y+w*z,d]])
print('Endomorphism matrix:', M)
print('Determinant:', s.factor(M.det()))
print('Inverse over D(a*d):', M.inv())
print('Aut(E) is the affine principal open D(a*d) in A^5.')
print('Its unipotent radical is A^3; a Levi factor is G_m^2.')
