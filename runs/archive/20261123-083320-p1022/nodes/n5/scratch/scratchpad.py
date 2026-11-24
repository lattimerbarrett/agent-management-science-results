# Explicit audit of composition and inversion in a family of lifts.
# For E=O+O(1) on P^2, write a lift over g as
# (x;s,t) -> (g*x; a*s, ell*x*s+d*t).
import sympy as s
x=s.Matrix(s.symbols('x0:3'))
g=s.Matrix(3,3,s.symbols('g0:9'))
h=s.Matrix(3,3,s.symbols('h0:9'))
ell=s.Matrix(1,3,s.symbols('l0:3'))
m=s.Matrix(1,3,s.symbols('m0:3'))
a,d,b,e=s.symbols('a d b e', nonzero=True)
Fg_hx=s.Matrix([[a,0],[(ell*h*x)[0],d]])
Fh_x=s.Matrix([[b,0],[(m*x)[0],e]])
product=Fg_hx*Fh_x
expected=s.Matrix([[a*b,0],[((b*ell*h+d*m)*x)[0],d*e]])
print('Composition formula verified:', all(s.expand(z)==0 for z in product-expected))
print('Parameters of product: (g*h, a*b, d*e, b*ell*h+d*m).')
print('Inverse parameters: (g^(-1), 1/a, 1/d, -ell*g^(-1)/(a*d)).')
print('On SL(3), g^(-1)=adj(g), so inversion is regular after inverting a*d.')
print('This test gives a finite-type affine lift group, not a counterexample.')
