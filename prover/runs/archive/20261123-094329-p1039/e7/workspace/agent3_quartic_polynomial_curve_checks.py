import sympy as s
x,y,M=s.symbols("x y M",real=True)
zeta=x+s.I*y
# n=3 example q=(2,0;0), arbitrary sample tangent (3+2i,-1+i;2-i).
z1=2+(3+2*s.I)*zeta
z2=(-1+s.I)*zeta+M*zeta*zeta
w=(2-s.I)*zeta
sq=lambda p:s.expand(p*s.conjugate(p))
rho=sq(z1)+sq(z2)+(sq(w)-1)**2-2
assert s.expand(rho-(sq(z1)+sq(z2)+(5*(x*x+y*y)-1)**2-2))==0
assert s.expand(sq(z1)-(4+12*x-8*y+13*(x*x+y*y)))==0
# Near |zeta|<=delta, ignore nonnegative |z2|² and positive quartic term.
# |12x-8y| <= sqrt(208)*r < 15r.
delta=s.Rational(1,100)
assert 208<15**2
assert 3-15*delta-10*delta**2>0
# Far |zeta|>=delta, ||z'||>=M*r²-||v||*r-||q||.
# ||v||²=15<16, so use ||v||<=4 and M=100000.
MM=s.Integer(100000)
assert 15<16
assert MM*delta**2-4*delta-2>2
assert 2*MM*delta-4>0
print("Polynomial curve exact expansion and global near/far safety bounds verified.")
