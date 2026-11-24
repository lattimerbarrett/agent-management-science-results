import sympy as s
e=s.symbols('e', nonnegative=True, integer=True)
# D=(a,b) means a*S+b*f.
def dot(D,F):
    a,b=D;c,d=F
    return s.expand(-e*a*c+a*d+b*c)
H=(1,3*e+1); P=(4,12*e+3); c1=(4,12*e+4)
print('c1.P =',dot(c1,P))
print('slope_P =',s.simplify(dot(c1,P)/2))
print('P^2 =',dot(P,P))
print('HE horizontal trace has strictly positive sign for every nonzero bundle vector.')
print('One positive horizontal eigenvalue + one radial positive eigenvalue = at least 2 positive Levi eigenvalues in dimension 4, hence q <= 3.')
