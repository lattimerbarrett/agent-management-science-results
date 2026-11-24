import sympy as s
R,L,r,t,h,shift=s.symbols('R L r t h shift',real=True)
x=h+shift
xt=-(1-t)*R/2+t*x
lower_h_t=h-(1-t)*L*r
margin=s.expand(lower_h_t+shift-xt)
assert s.factor(margin-(1-t)*(h+shift+R/2-L*r))==0
lower_margin=s.expand(margin.subs(h,-L*r))
assert s.factor(lower_margin-(1-t)*(shift+R/2-2*L*r))==0
eta=s.symbols('eta',positive=True)
assert s.simplify((R/2-2*L*R).subs(L,(1-eta)/4)-R*eta/2)==0
print('PASS: exact star-shapedness margin for small graph domains.')
