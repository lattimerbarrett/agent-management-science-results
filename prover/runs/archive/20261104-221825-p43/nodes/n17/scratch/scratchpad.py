import sympy as s
u,v,z,w,eps=s.symbols('u v z w eps',real=True)
A=s.Function('A')(u); d=s.Function('d')(u)
b=1+eps*s.diff(A,u)*s.diff(d,u)
Y=[-eps*A*s.diff(d,u),b*v,z/2,w/2]
h=A*v+z*w
D=d+v*v+z*z+w*w
act=lambda f:s.expand(sum(yi*s.diff(f,xi) for yi,xi in zip(Y,[u,v,z,w])))
print('Yh-h =',s.simplify(act(h)-h))
print('YD =',s.collect(act(D),[v,z,w]))
r=s.symbols('r',positive=True)
psi=s.exp(1-1/r**2)
print('flat radial factor derivative:',s.diff(psi,r))
