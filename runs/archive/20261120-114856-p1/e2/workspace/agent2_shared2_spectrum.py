import sympy as S
x,h=S.symbols('x h',real=True)
beta=S.Rational(1,100)
chi=S.expand((x*x-1)**2*(x*x-beta)-beta)
assert chi.subs(x,0)==-2*beta
assert S.expand(S.diff(chi,x)-2*x*(x-1)*(x+1)*(3*x*x-1-2*beta))==0
assert S.expand((chi+h).subs(h,beta)-(x-1)**2*(x+1)**2*(100*x*x-1)/100)==0
# Sturm exact real-root isolation, 6 distinct roots and all in (-2,2).
I=S.Poly(chi,x).intervals(eps=S.Rational(1,1000000))
assert len(I)==6 and all(mult==1 for _,mult in I)
assert all(-2<a<b<2 for (a,b),_ in I)
assert all(not(a<=0<=b)for(a,b),_ in I)
print('beta=',beta,'chi=',chi)
print('exact rational root isolators=',I)
# Local maxima at x^2=(1+2beta)/3 have positive chi value.
tc=(1+2*beta)/3
maxvalue=S.factor((tc-1)**2*(tc-beta)-beta)
assert maxvalue>0
assert chi.subs(x,1)==-beta and chi.subs(x,-1)==-beta
print('noncentral local maximum=',maxvalue)
# For h>beta, the two outer local minima are positive, so chi+h
# cannot have all six roots real. This follows from derivative's exact
# five critical points: 0,+/-sqrt(tc),+/-1 and their ordering.
assert 0<tc<1
# Stationary-pair value at the missing node 0.
m0=S.factor((chi.subs(x,0)+h)/h)
assert S.factor(m0-(1-2*beta/h))==0
print('absent zero multiplier=',m0)
print('All exact shared-two-root spectral checks passed.')
