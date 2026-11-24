import sympy as S
x=S.symbols('x'); nodes=list(map(S.Integer,[-3,-2,-1,1,2,3]));n=6;s=3
p=x**3-7*x+2;q=x**3-7*x-2;H=S.Integer(32)
chi=S.prod(x-t for t in nodes)
assert S.expand(p*q-chi-H)==0
pv=S.Matrix([p.subs(x,t) for t in nodes]);qv=S.Matrix([q.subs(x,t) for t in nodes])
X=S.Matrix([[t**j for j in range(s)] for t in nodes]); ww=S.symbols('w0:6')
C=S.ones(1,n).col_join(X.T*S.diag(*pv))
sol=S.linsolve((C,S.Matrix([1,0,0,0])),ww)
print('p*q=chi+32; p_i=',list(pv),'q_i=',list(qv))
print('stationary weight polygon:',sol)
w=S.Matrix([S.Rational(z,9) for z in [2,1,1,2,2,1]])
def step(w):
 W=S.diag(*list(w)); G=X.T*W*X
 mon=S.Matrix([t**s for t in nodes]);p=mon-X*G.inv()*X.T*W*mon
 p2=p.multiply_elementwise(p);h=(w.T*p2)[0]
 wp=w.multiply_elementwise(p2)/h
 J=S.diag(*list(p2))/h-2*S.diag(*list(w.multiply_elementwise(p)))*X*G.inv()*X.T*S.diag(*list(p))/h-w.multiply_elementwise(p2)*p2.T/h**2
 return wp,p,h,J
wp,pp,h,J=step(w);wpp,qq,hh,JJ=step(wp)
assert pp==pv and qq==qv and h==hh==H and wpp==w
B=S.zeros(n,n-1)
for j in range(n-1):B[j,j]=1;B[n-1,j]=-1
N=(JJ*J)[:n-1,:]*B-S.eye(n-1)
assert N*N==S.zeros(n-1)
print('two-step differential N=DF-I: rank',N.rank(),'N^2=0')
print('one-step weights:',list(wp))

