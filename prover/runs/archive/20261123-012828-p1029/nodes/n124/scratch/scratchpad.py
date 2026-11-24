import sympy as s
# Algebra underlying the upper-bound-preserving interpolation.
x,u,v,t=s.symbols('x u v t', real=True)
a=(1-t)*x+t*u
print('increment:',s.expand(a-x))
print('upper-bound slack:',s.expand(v-a))
P,r=s.symbols('P r', real=True)
print('residual after another step:',s.expand((1-r)*(P*x+(1-P)*u)+r*u-(P*(1-r)*x+(1-P*(1-r))*u)))
