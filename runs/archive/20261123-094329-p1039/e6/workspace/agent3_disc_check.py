import sympy as s
# Analytic-disc certificate for a negative Levi direction in normalized coordinates.
# rho(z)=Re z_n-mu |z1|²+R(z), |R(z)|<=C ||z||³.
# Choose a>0 with mu*a<=1 and 27*C*a<=mu.
mu,C,a=s.symbols('mu C a',positive=True)
# On disk z1=a*zeta, z_n=mu*a²/2, the l1 norm is <=3a/2.
assert s.expand((s.Rational(3,2)*a)**3)==s.Rational(27,8)*a**3
rem_bound=s.Rational(27,8)*C*a**3
assert s.simplify(rem_bound.subs(C,mu/(27*a)))==mu*a*a/8
assert s.simplify(mu*a*a/2-mu*a*a+mu*a*a/8)==-3*mu*a*a/8
assert s.simplify(mu*a*a/2-mu*a*a/8)==3*mu*a*a/8
print('Negative-Levi disc margins: boundary <= -3*mu*a²/8; center >= 3*mu*a²/8')
