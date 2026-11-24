import sympy as s
a1,a2=s.symbols('a1 a2',nonzero=True)
r0,r1,r2,w0,w1,w2,B=s.symbols('r0 r1 r2 w0 w1 w2 B')
A=s.diag(0,a1,a2);Ai=s.diag(0,1/a1,1/a2)
R=s.Matrix([r0,r1,r2]);W=s.Matrix([w0,w1,w2])
Bp=B+(R.T*W)[0]+s.Rational(1,2)*(W.T*A*W)[0]
Rp=R+A*W
reduced=B-s.Rational(1,2)*(R.T*Ai*R)[0]
reducedp=Bp-s.Rational(1,2)*(Rp.T*Ai*Rp)[0]
assert s.simplify(reducedp-reduced-r0*w0)==0
assert s.simplify((reducedp-reduced).subs(w0,0))==0
print('Joint forced Schur invariance exact on Kperp; kernel reparametrization defect R_K W_K checked.')
