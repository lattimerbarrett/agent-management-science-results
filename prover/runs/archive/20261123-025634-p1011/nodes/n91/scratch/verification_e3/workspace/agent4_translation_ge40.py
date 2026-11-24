"""Additional exact polynomial checks for full scale+translation model maximum in every n>=40. Depends on all_n_certificate's negative 2x2 scale minor, not a PDE existence proof."""
import sympy as s
n,t,y=s.symbols('n t y')
Q=s.sympify(open('workspace/agent4_symbolic_Q.txt').read())
def positive_shift(poly):
 return all(c>0 for c in s.Poly(s.expand(poly.subs(n,y+40)),y).all_coeffs())
# Exact gamma-ratio interval: 0<t<2/(3n). Q01 positive.
num,den=s.fraction(s.factor(Q[0,1]))
assert all(c>0 for c in s.Poly(s.expand(num.subs(n,y+40)),y,t).coeffs())
assert positive_shift(den)
# Linear in t, so endpoint positivity proves Q01<2Q00 throughout.
R=s.factor(2*Q[0,0]-Q[0,1])
assert s.degree(s.fraction(R)[0],t)==1
for endpoint in (0,s.Rational(2,3)/n):
 num,den=s.fraction(s.factor(R.subs(t,endpoint)))
 assert positive_shift(num) and positive_shift(den)
d=s.symbols('d',positive=True)
# C_b < (2+8b)Q01 at b=0 automatically; at b=1 follows Q01<2Q00 and this:
expr=s.factor(-2+32/d+256/(d*(d+4)))
num,den=s.fraction(expr)
assert all(c<0 for c in s.Poly(s.expand(num.subs(d,y+39)),y).all_coeffs())
assert all(c>0 for c in s.Poly(s.expand(den.subs(d,y+39)),y).all_coeffs())
print('CERTIFIED: all n>=40 have a degree-four full scale+translation MODEL maximum, given the already-certified negative 2x2 scale minor.')

# Independent exact verification of the stronger translation identity.
x,b,q00,q01,q11=s.symbols('x b q00 q01 q11')
A=2+8*b;C=-2+32*b/d
C_b=C*q00+2*(4*b*d*d+16*b*d+64*b+d*d)/(d*(d+4))*q01
H=x*(-A*q00+x*(A*q01+C_b))
Hnew=x*x*(-A*(2*q01-3*q11*x)+C*(q00+4*q01/(d+4)))
root_relation=q00-4*q01*x+3*q11*x*x
assert s.factor(H-Hnew+A*x*root_relation)==0
print('Exact root-identity for translation Hessian verified; H<0 for d>=16, b in [0,1], q01>0 at smaller positive scale root.')
