import sympy as S
r=S.symbols("r",real=True)
B=4096
p=S.Poly(S.Rational(1,16)-S.Rational(7,2)*r-2*B*r**3+(B*B+1)*r**4,r)
assert p.count_roots(0,S.oo)==0
assert p.eval(0)>0
x,y=S.symbols("x y",real=True)
t=x+S.I*y
gamma=[S.Rational(7,4)+t,t+B*t*t,t]
norm=lambda z:S.expand_complex(z*S.conjugate(z)).expand()
rho=S.expand(norm(gamma[0])+norm(gamma[1])+(norm(gamma[2])-1)**2-4)
expected=S.Rational(1,16)+S.Rational(7,2)*x+2*B*x*(x*x+y*y)+(B*B+1)*(x*x+y*y)**2
assert S.expand(rho-expected)==0
# Write r=|t|. Since x>=-r, rho>=p(r)>0.
print("PASS: exact Sturm certificate, polynomial entire curve avoids K globally")
