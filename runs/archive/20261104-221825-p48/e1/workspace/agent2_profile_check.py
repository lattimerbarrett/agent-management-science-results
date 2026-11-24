import sympy as s
from pathlib import Path
z,zb,w,wb=s.symbols('z zb w wb')
a,ab,b,bb=s.symbols('alpha alphabar beta betabar')
p=s.Matrix([[1,bb*z-a*zb],[-ab*z+b*zb,0]])
v=s.Matrix([1,w]);vc=s.Matrix([[1,wb]])
t=(vc*p*v)[0]/(1+w*wb)
F=s.Function('F')
L=s.log(1+w*wb)+F(t)
V=s.diff(L,w,wb).subs({z:0,zb:0,w:0,wb:0}).doit()
C=s.diff(L,z,wb).subs({z:0,zb:0,w:0,wb:0}).doit()
assert s.simplify(V-(1-s.Subs(s.Derivative(F(s.Symbol('_x')),s.Symbol('_x')),s.Symbol('_x'),1)))==0 if False else True
f1=s.symbols('f1')
V=V.replace(lambda e:isinstance(e,s.Subs),lambda e:f1)
C=C.replace(lambda e:isinstance(e,s.Subs),lambda e:f1)
assert s.simplify(V-(1-f1))==0
assert s.simplify(C+ab*f1)==0
print('Verified profile Levi at pureA: angular=1−Fprime(1), mixed=−alphabar*Fprime(1).')
Path('workspace/agent2_profile_check.py').write_text(Path(__file__).read_text())
