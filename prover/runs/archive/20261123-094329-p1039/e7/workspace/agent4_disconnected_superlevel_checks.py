import sympy as s
h,g=s.symbols("h g")
T=s.Matrix([s.exp(h*h),s.exp(h*h)*g])
assert s.factor(T.jacobian([h,g]).det())==2*h*s.exp(2*h*h)
v=s.symbols("v",nonnegative=True)
assert s.simplify(s.diff(s.exp(-2*v)*(1+v),v))==(-1-2*v)*s.exp(-2*v)
barrier=(s.exp(-h*h)-s.exp(-2*h*h))/(h*h)
assert s.limit(barrier,h,0)==1
assert s.Rational(5,16)<s.Rational(1,2)
assert s.E<4
print("Exact determinant, monotonicity, and barrier checks passed.")
