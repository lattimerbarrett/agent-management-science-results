import sympy as s
u,v,p,t,eps=s.symbols('u v p t eps', real=True)
A=s.Function('A')(u); d=s.Function('d')(u)
h=A*v+p*t; D=d+v*v+p*p+t*t
b=1+eps*s.diff(A,u)*s.diff(d,u)
Y=[-eps*A*s.diff(d,u),b*v,p/2,t/2]
def apply(f): return s.expand(sum(y*s.diff(f,x) for x,y in zip([u,v,p,t],Y)))
print('Yh-h =', s.simplify(apply(h)-h))
print('YD =',s.collect(apply(D),[eps,v*v,p*p,t*t]))
r=s.symbols('r',positive=True); chi=s.Function('chi')(r)
psi=r*s.exp(-chi/r**2)
print('psi derivative / psi =',s.simplify(s.diff(psi,r)/psi))
print('For chi>=0 and chi_prime<=0 this is positive.')
