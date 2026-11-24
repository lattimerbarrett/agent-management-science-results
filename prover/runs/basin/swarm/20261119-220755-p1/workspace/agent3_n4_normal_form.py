import sympy as S
from pathlib import Path
x,a,b,t=S.symbols('x a b t');P=x**4-10*x*x+9;f=x*x+a*x+b
u=a*(10+2*b-a*a)/(a*t-a*a+b-t*t+10);c=u-a;d=-10-b+a*a+u*(t-a);g=x*x+c*x+d;z=b*d-9;NN=z-t*(t*t-10)*u;tn=(t*z+9*u)/NN
assert S.cancel(f*g-P-u*(x**3+t*x*x+(t*t-10)*x)-z)==0
assert S.cancel(tn-t-u*P.subs(x,t)/NN)==0
R=S.rem((x-t)*f*g,P,x)
assert S.cancel(R-NN*(x-tn))==0
print('Exact rational n4 map identities checked')
