# Check how the scalar increment can be enlarged under the
# fractional-linear order automorphism f_t(x)=x/(t+(1-t)*x).
import sympy as s
x,y,t=s.symbols('x y t', positive=True)
f=lambda z:z/(t+(1-t)*z)
print(s.factor(f(y)-f(x)))
print(s.limit(f(x),t,0,dir='+'))
