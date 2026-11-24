import sympy as S
p,r,m,y,z=S.symbols('p r m y z');s=1-r;a=p*p/3
g=4*p/3-2*p*p/3
J=(2*a+r*(a-r)/s)/(3*m)+m*(s*(5-3*m)+3*r)/(3*(1+m))
P0=y*y*(y**4-12*y**3+46*y*y-60*y+25)+y*z*(y**4-18*y**3+100*y*y-126*y+43)+z*z*(-6*y**3+58*y*y-58*y+22)
P1=y*y*(2*y*y-20*y+50)+y*z*(y*y-82*y+97)+z*z*(-3*y*y-102*y+45-36*z)
left0=S.factor((g-J.subs(m,p/(3*(1-p)))).subs({p:(1+y)/2,r:y+z}))
left1=S.factor((g-J.subs(m,2*p/(3*(1-r)))).subs({p:(1+y)/2,r:y+z}))
assert S.cancel(left0-P0/(12*(2-y)*(1-y)*(1+y)*(1-y-z)))==0
assert S.cancel(left1-P1/(12*(1+y)*(4-2*y-3*z)))==0
print('Both far endpoint polynomial identities independently verified exactly.')
