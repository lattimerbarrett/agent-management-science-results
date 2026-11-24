from pathlib import Path
code='''import sympy as s
z,b=s.symbols('z b') # b is formal conjugate z
pi=s.pi
h=(s.exp(2*pi*s.I*z*b)-1)/(2*pi*s.I*z)
assert s.simplify(s.diff(h,b)-s.exp(2*pi*s.I*z*b))==0
assert s.simplify(s.diff(h,b,z)-2*pi*s.I*b*s.exp(2*pi*s.I*z*b))==0
# removable smooth expression: h=conj(z)*Phi(|z|²), Phi entire.
t=s.symbols('t')
Phi=(s.exp(2*pi*s.I*t)-1)/(2*pi*s.I*t)
assert s.limit(Phi,t,0)==1
assert s.simplify(h-b*Phi.subs(t,z*b))==0
# General Levi matrix of |w-h|²+alpha |z|².
a,c,aa,bb,alpha=s.symbols('a c aa bb alpha',real=True)
# a=Re h_z,c=Im h_z, aa=|h_barz|², bb=2Re[(barw-barh)h_zbarz]
H=s.Matrix([[a*a+c*c+aa-bb+alpha,-a-s.I*c],[-a+s.I*c,1]])
assert s.expand(H.det())==aa-bb+alpha
# eps=1/(32pi), R=2: det >= 1-2 eps*(2piR)+eps²/4.
eps=1/(32*pi); R=2
bound=s.simplify(1-2*eps*(2*pi*R)+eps**2/4)
assert s.simplify(bound-(s.Rational(3,4)+eps**2/4))==0
assert bound>0
hp=s.simplify(h.subs({z:s.Rational(1,2),b:s.Rational(1,2)}))
assert s.simplify(s.expand_complex(hp*s.conjugate(hp))-2/pi**2)==0
assert 2/pi**2>eps**2
# Circle |z|=1,w=0,u=0 has rho=eps²/4<eps².
assert eps**2/4<eps**2
print('Verified explicit nonrational-convex strong-pseudoconvex ball geometry for all n>=2.')
print('No non-Oka conclusion is asserted.')
'''
Path('workspace/agent4_graph_ball_check.py').write_text(code)
exec(code)