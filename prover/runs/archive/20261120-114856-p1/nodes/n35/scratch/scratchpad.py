import sympy as S
nodes=list(map(S.Rational,[-3,-1,1,3]));a,b,c=S.symbols('a b c');coords=S.Matrix([a,b,c]);w=S.Matrix([a,b,c,1-a-b-c])
def step(w):
 m=[sum(wi*x**j for wi,x in zip(w,nodes)) for j in range(5)]
 B=S.Matrix([[m[0],m[1]],[m[1],m[2]]]); co=-B.inv()*S.Matrix([m[2],m[3]])
 vals=S.Matrix([x*x+co[1]*x+co[0] for x in nodes]);h=sum(w[i]*vals[i]**2 for i in range(4))
 return S.Matrix([S.cancel(w[i]*vals[i]**2/h) for i in range(4)])
# Chain rule: evaluate the two one-step Jacobians separately, avoiding composition.
T=step(w);J=T[:3,0].jacobian(coords)
for t in [S.Rational(1,24),S.Rational(1,24)+S.Rational(1,100000),S.Rational(1,16),S.Rational(1,12)]:
 wc=S.Matrix([t,21*t-S.Rational(7,8),S.Rational(7,4)-21*t,S.Rational(1,8)-t]);sub=dict(zip(coords,wc[:3,0]));wp=T.subs(sub);D=S.simplify(J.subs(dict(zip(coords,wp[:3,0])))*J.subs(sub));N=D-S.eye(3)
 assert N*N==S.zeros(3)
 print('t=',t,' min weight=',min(wc),' determinant DF=',D.det(),' max abs entry=',max(map(abs,D)))
print('Boundary audit: in this stationary family, the ambient inverse derivative remains finite at zero weights. Boundary positivity alone is not a valid diagnosis of a flaw.')
