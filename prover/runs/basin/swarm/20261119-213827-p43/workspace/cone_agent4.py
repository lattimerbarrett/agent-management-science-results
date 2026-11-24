import sympy as s
r=s.symbols("r", positive=True)
rho=s.exp(-1/r**2)
assert s.simplify(s.diff(rho,r)-2*rho/r**3)==0
# Every radial derivative is a Laurent polynomial times exp(-1/r^2).
P=s.Integer(1)
D=rho
for n in range(13):
    assert s.expand(D/rho-P)==0
    for term in s.Add.make_args(s.expand(P)):
        coeff,power=term.as_coeff_exponent(r)
        assert power.is_integer
        assert s.limit(r**power*rho,r,0,dir="+")==0
    P=s.expand(s.diff(P,r)+2*P/r**3)
    D=s.diff(D,r).expand()
# Full Euclidean gradient norm identity for a radially constant angular function.
x=s.Matrix(s.symbols("x0:4",real=True)); dg=s.Matrix(s.symbols("d0:4",real=True))
a,b,g=s.symbols("a b g",real=True)
D=a*g*x/r+b*dg
rhs=a*a*g*g*x.dot(x)/r**2+b*b*dg.dot(dg)+2*a*b*g*x.dot(dg)/r
assert s.expand(D.dot(D)-rhs)==0
# On |x|=r and x.dot(dg)=0, this is a^2*g^2+b^2*|dg|^2.
print("Flatness derivative recurrence verified through order 12; exact gradient norm identity verified.")
