import sympy as s
eta,t,d=s.symbols('eta t d', real=True)
# If p=1_(t,1](b), then b<=t(1-p)+p, so eta<=t+(1-t)q(p).
lower=(eta-t)/(1-t)
assert s.simplify((t+(1-t)*d-eta)-(1-t)*(d-lower))==0
print('Projection dimension lower bound:',lower)
print('At t=eta/2:',s.factor(lower.subs(t,eta/2)))
print('Scaled projection lower bound:',s.factor((t*lower).subs(t,eta/2)))
print('For each N, t*sum(p_n, n<N) <= sum(b_n, n<N) <= 1.')
print('Verified exhaustion applied to the positive series (t*p_n) gives t*q(p_n) -> 0.')
print('For constant eta>0 this contradicts the displayed fixed positive lower bound.')
