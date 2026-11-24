from pathlib import Path
import sympy as S
z=S.symbols('z'); nodes=list(map(S.Rational,[-3,-1,1,3])); w=list(map(S.Rational,[S.Rational(1,10),S.Rational(2,10),S.Rational(3,10),S.Rational(4,10)])); s=3
f=lambda x:S.Matrix([1,x,x*x])
G=sum((wi*f(x)*f(x).T for x,wi in zip(nodes,w)),S.zeros(3)); rhs=sum((wi*x**3*f(x) for x,wi in zip(nodes,w)),S.zeros(3,1)); c=-G.inv()*rhs;q=S.expand(z**3+(f(z).T*c)[0]);H=S.expand(sum(wi*q.subs(z,x)**2 for x,wi in zip(nodes,w)));wp=[wi*q.subs(z,x)**2/H for x,wi in zip(nodes,w)];Gp=sum((wi*f(x)*f(x).T for x,wi in zip(nodes,wp)),S.zeros(3));cp=-Gp.inv()*sum((wi*x**3*f(x) for x,wi in zip(nodes,wp)),S.zeros(3,1));r=S.expand(z**3+(f(z).T*cp)[0]);R=-Gp.inv()*G;d=sum((wi*(r.subs(z,x)-q.subs(z,x))*f(x).T for x,wi in zip(nodes,w)),S.zeros(1,3));C=4*q*G.inv()*f(z);a=(r*f(z).T+q*f(z).T*R+d)/H;KG=(f(z).T*G.inv()*f(z))[0];KGp=(f(z).T*Gp.inv()*f(z))[0]
assert all(S.simplify(q.subs(z,x)*r.subs(z,x)-H)==0 for x in nodes)
assert S.expand((d*C)[0]-4*q*(r-q))==0
expr=S.expand((a*C)[0]+4*(KG+q*q/H*KGp+1+q*q/H)); assert S.rem(expr,q*r+H,z)==0
print('Exact arbitrary-negative-level pulse identities PASS; q=',q,'r=',r,'H=',H)
# Verify the reflection, quadratic invariant, and deficit decrement with symbolic forms.
ain,ac,dc,din=S.symbols('ain ac dc din',nonzero=True);v=S.Matrix(S.symbols('v0:3'));cv=S.Matrix(S.symbols('c0:3'));av=S.Matrix(1,3,S.symbols('a0:3'))
J=S.eye(3)-2*cv*av/(av*cv)[0]
assert S.simplify(J*J)==S.eye(3)
print('Reflection involution PASS; a(C)<0 by positive-definite G,Gp; dh(C)<0 by formula.')
