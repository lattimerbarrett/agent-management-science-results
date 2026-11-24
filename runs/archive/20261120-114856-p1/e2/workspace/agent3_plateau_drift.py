"""Exact general plateau quadratic-drift identities (agent 3).
No floating-point tests: Sympy rational polynomial identities.
"""
import sympy as S
x=S.symbols('x'); A,B,C=S.symbols('A B C')
nodes=list(map(S.Integer,[-3,-2,-1,1,2,3]))
w=[S.Rational(1,6)]*6
sigma=(x**3-7*x)/6
E=lambda f:S.expand(sum(wi*f.subs(x,ti) for wi,ti in zip(w,nodes)))
assert all(sigma.subs(x,t)**2==1 for t in nodes)
assert all(E(sigma*x**j)==0 for j in range(3))
M=S.Matrix([[E(x**(i+j)) for j in range(3)] for i in range(3)])
u=A*x*x+B*x+C
v=M.inv()*S.Matrix([E(sigma*u*u*x**j) for j in range(3)])
vpoly=sum(v[j]*x**j for j in range(3))
D=E(u*u)
K=2*(sigma*vpoly-u*u+D)
assert E(K)==0
assert all(E(K*sigma*x**j)==0 for j in range(3))
k1=S.factor(E(x*K));k2=S.factor(E(x*x*K))
assert S.expand(k1+S.Rational(800,147)*B*(7*A+C))==0
assert S.expand(k2+S.Rational(400,63)*(7*A*A+2*A*C+B*B))==0
center={C:-S.Rational(14,3)*A}
assert S.expand(k1.subs(center)+S.Rational(800,63)*A*B)==0
assert S.expand(k2.subs(center)-S.Rational(400,63)*(S.Rational(7,3)*A*A-B*B))==0
print('All plateau drift identities verified exactly.')
