import sympy as s
eta,r,eps=s.symbols('eta r eps', positive=True)
loss=eps+2*s.sqrt(eps)
lower=(eta-loss)/(1-r)
print('Retained normalized increment lower bound:',lower)
print('Gain over eta:',s.factor(lower-eta))
print('Improvement condition: eps + 2*sqrt(eps) < r*eta, with 0<r<1.')
print('If the removed corner is norm-convergent, eps_n -> 0.')
print('Then limiting lower bound =',s.limit(lower,eps,0,dir='+'))
print('Using exact-gap interpolation plus the universal 1/2 bound gives:')
print('eta/(1-r) <= 1/2, equivalently r <= 1-2*eta.')
# Numerical examples illustrate why spectral mass matters.
for E,R,H in [(1e-6,.1,.1),(.01,.001,.1), (1e-8,.01,.4)]:
 L=(H-E-2*E**.5)/(1-R)
 print({'epsilon':E,'removed_dimension':R,'original_eta':H,'guaranteed_new_increment':L,'guaranteed_gain':L>H})
