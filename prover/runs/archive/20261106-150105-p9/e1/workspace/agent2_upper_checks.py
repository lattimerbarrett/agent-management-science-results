import sympy as s
from pathlib import Path
p,d,K=s.symbols('p d K', positive=True)
q=p/(p-1)
a=s.factor(q*(1+d)/(q*(1+d)-1))
b=s.factor(p*(1+d)/(p*(1+d)-1))
assert s.simplify(1+1/(p-1)-1/p-(1/p+1/q+1/(p*(p-1))))==0
assert s.simplify(p-a-p*(p-1)*d/(1+p*d))==0
assert s.simplify(q-b-p*d/((p-1)*(p-1+p*d)))==0
assert s.simplify(1/a-1/p-d/(q*(1+d)))==0
assert s.simplify(1/b-1/q-d/(p*(1+d)))==0
# Exact geometric series used in scalar reverse Holder.
z,r=s.symbols('z r', positive=True)
assert s.simplify(1+(z-1)/(1-r*z)-z*(1-r)/(1-r*z))==0
# For z=1+t/4, r=1-t, ratio is <=2 for 0<t<=1.
t=s.symbols('t', positive=True)
ratio=s.factor((1+t/4)*t/(1-(1-t)*(1+t/4)))
assert s.simplify(ratio-(4+t)/(3+t))==0
assert s.simplify(2-ratio-(2+t)/(3+t))==0
print('Verified 8 exact symbolic upper-bound identities.')
print('a=',a,'; p-a=',s.factor(p-a))
print('b=',b,'; q-b=',s.factor(q-b))
print('reverse-Holder factor=',ratio)
