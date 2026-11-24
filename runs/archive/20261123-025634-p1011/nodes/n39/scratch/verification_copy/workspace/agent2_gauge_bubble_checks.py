import sympy as s
n,eps,R,t=s.symbols('n eps R t', nonzero=True)
a=(n-2)/2
z2,zw,w2=s.symbols('z2 zw w2')
identity=2*(z2-zw)-(z2-2*zw+w2)
assert s.expand(identity-z2+w2)==0
assert s.expand((R**2-(R-t)**2)-(2*R*t-t**2))==0
assert s.simplify((s.Rational(1,2)-(R**2-zw)/(eps**2+R**2-2*zw+(R-t)**2)).subs(eps**2,2*R*t-t**2))==0
k,e=s.symbols('k e',real=True)
shift=k*e**2/(1+s.sqrt(1-k**2*e**2))
assert s.simplify(2*shift-k*shift**2-k*e**2)==0
assert s.limit(shift,k,0)==0
assert s.simplify(s.limit(shift/e**2,e,0)-k/2)==0
print('Exact signed osculating-sphere adapted-bubble Robin identity and smooth small-width shift checked.')
