import sympy as s
r,d,n,A=s.symbols('r d n A',positive=True)
a=(n-2)/2
b=(n-2)/(2*(n-1))
# Angular integrals are normalized here by |S^(n-2)|.
H=r**d
L=s.simplify(a*b*r**(-(n-2))*(2*H/r-s.diff(H,r)))
rhs=-a*b*r**(-n)*(r*r*s.diff(H,r,2)-n*r*s.diff(H,r)+2*(n-1)*H)
assert s.simplify(s.diff(L,r)-rhs)==0
print('Linear counterterm L_h / angular area =',s.factor(L))
print('Resonant degree d=n-1:',s.factor(L.subs(d,n-1)))
# A flat minimal catenoidal end has F(R)=-A/(n-3)*R^(3-n)+...,
# and its inversion has h(r)=-A/(n-3)*r^(n-1)+... .
kap=-A/(n-3)
Lcat=s.factor(L.subs(d,n-1)*kap)
print('Catenoidal end L_h / angular area =',Lcat)
print('Fundamental harmonic pole G=r^(2-n) has P=0.')
print('Hence (P-L_h) / angular area =',-Lcat)
# Unnormalized mass from metric flux and codimension-two boundary edge.
C=4*(n-1)/(n-2)
print('Corresponding mass flux / angular area =',s.simplify(C/a*Lcat))
# The edge in the exact Robin Pohozaev identity:
# (b/2) int_edge H_g G^2 (x^T.eta), for h=kappa*r^d.
# H_g ~ kappa*d*(d+n-3)*r^(d-2), x^T.eta ~r.
edge=s.factor(b*s.Symbol('kappa')*d*(d+n-3)/2*r**(d+1-n))
print('Robin Pohozaev edge / angular area =',edge)
print('Its resonant value =',s.factor(edge.subs(d,n-1)))
print('n=5, A=1: L_h / angular area =',Lcat.subs({n:5,A:1}))
