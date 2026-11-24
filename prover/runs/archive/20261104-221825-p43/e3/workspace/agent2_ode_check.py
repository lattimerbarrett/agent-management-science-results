import sympy as s
r,p=s.symbols('r p', positive=True)
D=s.sqrt(1-p*p);u=s.sqrt(4*D*D-r*r)
e=p*r/(D*s.sqrt(4-r*r))
# On domain 0<p<1 and 0<r<2D the square roots are positive.
# Derivative asin(e)=4p/((4-r²)*sqrt(4D²-r²)).
Eprime=4*p/((4-r*r)*u)
# Verify by squaring, then positivity fixes the square-root branch.
assert s.simplify((s.diff(e,r)**2/(1-e*e))-Eprime**2)==0
# Differentiate primitive using the above verified positive derivative.
result=2*s.asin(e)+2*r*Eprime+4*s.diff(s.atan(u/(2*p)),r)
assert s.simplify(result-2*s.asin(e))==0
print('Exact ODE primitive derivative verified on 0<r<2sqrt(1-p²)')
