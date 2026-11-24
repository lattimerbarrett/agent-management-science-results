import sympy as s
u,v,p,q,e=s.symbols('u v p q e', real=True)
A=s.Function('A')(u); d=s.Function('d')(u)
h=A*v+p*q; D=d+v*v+p*p+q*q
b=1+e*s.diff(A,u)*s.diff(d,u)
Y=[-e*A*s.diff(d,u), b*v,p/2,q/2]
Yh=s.expand(sum(c*s.diff(h,z) for c,z in zip(Y,[u,v,p,q])))
YD=s.expand(sum(c*s.diff(D,z) for c,z in zip(Y,[u,v,p,q])))
print('Yh-h =',s.simplify(Yh-h))
print('YD-claimed =',s.simplify(YD-(-e*A*s.diff(d,u)**2+2*b*v*v+p*p+q*q)))
r=s.symbols('r',positive=True)
psi=s.exp(-1/r**2)
print('flat radial factor derivative:',s.diff(psi,r))