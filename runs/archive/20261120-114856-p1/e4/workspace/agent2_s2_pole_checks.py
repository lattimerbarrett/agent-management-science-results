import sympy as S
from pathlib import Path
x=S.symbols('x');nodes=list(map(S.Rational,[-3,-1,1,3]));P=S.prod(x-z for z in nodes)
w=[S.Rational(1,10),S.Rational(1,5),S.Rational(3,10),S.Rational(2,5)]
def block(w):
 G=S.Matrix(2,2,lambda i,j:sum(t*z**(i+j) for z,t in zip(nodes,w)))
 rhs=S.Matrix([sum(t*z**(i+2) for z,t in zip(nodes,w)) for i in range(2)])
 coef=-G.inv()*rhs;q=x*x+coef[1]*x+coef[0]
 M=S.expand(sum(t*S.div(P,x-z,x)[0] for z,t in zip(nodes,w)))
 a,t=S.div(S.expand(q*M),P,x);h=S.Poly(t,x).nth(1)
 eta=-S.Poly(a,x).nth(0);zeta=-S.Poly(t,x).nth(0)/h
 wn=[S.cancel(t*q.subs(x,z)**2/h) for z,t in zip(nodes,w)]
 return q,M,h,eta,zeta,wn
for k in range(5):
 q,M,h,eta,zeta,wn=block(w);qn,Mn,hn,en,zn,_=block(wn)
 K=hn-h;R=zeta-eta
 assert S.expand(hn*(x-zn)*(x-eta)-h*(x-en)*(x-zeta)-K*q)==0
 assert S.cancel((zn-zeta)+K*q.subs(x,zeta)/(hn*R))==0
 assert S.cancel((en-eta)+K*q.subs(x,eta)/(h*R))==0
 Cden=h*q.subs(x,zeta)+q.subs(x,eta)*P.subs(x,zeta)
 assert S.cancel(K*Cden+h*R*R*P.subs(x,zeta))==0
 assert K>=0
 w=wn
print('Exact n4 s2 scalar pole drift identities, five rational steps: PASS')
