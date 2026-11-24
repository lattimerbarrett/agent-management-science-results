import sympy as s
th,ph=s.symbols('theta phi',real=True)
g=2+s.cos(ph)
h=s.sin(ph)+s.I*s.sin(2*ph)
z=s.exp(2*s.I*th)*g*g
w=s.exp(s.I*th)*g*h
D=s.simplify(s.diff(z,th)*s.diff(w,ph)-s.diff(z,ph)*s.diff(w,th))
assert s.simplify(D-2*s.I*s.exp(3*s.I*th)*g**3*s.diff(h,ph))==0
assert s.simplify(z.subs({th:th+s.pi,ph:-ph})-z)==0
assert s.simplify(w.subs({th:th+s.pi,ph:-ph})-w)==0
# h'=cos(phi)+2i cos(2phi) never zero: cos(phi)=0 => cos(2phi)=-1.
c,d=s.symbols('c d',real=True)
assert (2*c*c-1).subs(c,0)==-1
assert s.expand(c*c+4*(2*c*c-1)**2-(16*(c*c-s.Rational(15,32))**2+s.Rational(31,64)))==0
# h² as a function of c=cos(phi), independent of sign(sin(phi)).
R=1-5*c*c+4*c**4
I=4*c-4*c**3
assert s.expand((R-R.subs(c,d))-(c-d)*(c+d)*(4*c*c+4*d*d-5))==0
assert s.expand((I-I.subs(c,d))+4*(c-d)*(c*c+c*d+d*d-1))==0
# Distinct c,d with equal h² either d=-c and c²=1,
# or c²+d²=5/4, cd=-1/4. The latter forces max(|c|,|d|)>1.
large=(s.sqrt(7)+s.sqrt(3))/4
assert s.simplify(large**2-1)==(-3+s.sqrt(21))/8
assert s.sqrt(21)>3
# At c=1 and c=-1, h=0 but |z|=9 and |z|=1, respectively.
assert ((2+c)**2).subs(c,1)==9
assert ((2+c)**2).subs(c,-1)==1
# Endpoint theta loops traverse z circles TWICE, so polynomial winding numbers
# at the two ends of the parameter cylinder are 2*N9 and 2*N1.
# Homotopy invariance forces N9=N1 whenever the polynomial is nonzero on K.
print('Verified Rudin Klein bottle immersion determinant, symmetry, and embedding algebra.')
print('Rational-hull annulus follows by argument principle as detailed in companion proof.')
print('NO claim about its neighborhood complement being non-Oka is established here.')
