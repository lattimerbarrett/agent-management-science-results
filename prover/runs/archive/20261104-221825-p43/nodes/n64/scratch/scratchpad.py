import sympy as s
a,b,c,d,t=s.symbols('a b c d t',real=True)
# Exact angular/transverse chart around the meridian pair.
h=s.sqrt(1-c*c)*s.cos(a)-s.sqrt(1-d*d)*s.cos(b)
for endpoint in [0,s.pi]:
 H=s.hessian(h,[a,b,c,d]).subs({a:endpoint,b:endpoint,c:0,d:0})
 print('Endpoint',endpoint,'Hessian:',H)
 print('Transverse (c,d) block:',H[2:4,2:4])
print('Interior dh along diagonal:',[s.simplify(s.diff(h,z).subs({a:t,b:t,c:0,d:0})) for z in [a,b,c,d]])