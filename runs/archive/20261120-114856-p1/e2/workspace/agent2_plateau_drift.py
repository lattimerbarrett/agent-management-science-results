import sympy as S
x,M,a,b=S.symbols('x M a b',real=True)
L=list(map(S.Integer,[-2,-1,1,2]));sig=[(2*l*l-5)/3 for l in L]
w=S.Matrix(S.symbols('w:4'))
sol=S.solve([sum(w)-1,sum(wi*si for wi,si in zip(w,sig)),sum(wi*si*li for wi,si,li in zip(w,sig,L)),sum(wi*li for wi,li in zip(w,L))-M],list(w));w=w.subs(sol)
E=lambda f:S.factor(sum(wi*f.subs(x,li) for wi,li in zip(w,L)))
u=a*x+b;D=E(u*u);Gram=S.Matrix([[E(x**(i+j)) for j in range(2)] for i in range(2)])
v=S.Matrix([E(x**j*(2*x*x-5)/3*u*u) for j in range(2)])
c=S.simplify(Gram.inv()*v);proj=c[0]+c[1]*x
K=[S.factor(2*wi*(si*proj.subs(x,li)-u.subs(x,li)**2+D)) for wi,si,li in zip(w,sig,L)]
dM=S.factor(sum(ki*li for ki,li in zip(K,L)))
meanfree=S.factor(dM.subs(b,-a*M))
assert S.factor(dM-8*a*b*(M*M-4)*(M*M-1)/(2*M*M-5))==0
assert S.factor(meanfree+8*M*a*a*(M*M-4)*(M*M-1)/(2*M*M-5))==0
print('w=',w);print('dM=',dM);print('meanfree=',meanfree)
