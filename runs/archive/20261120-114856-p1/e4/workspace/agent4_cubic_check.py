import sympy as S,os
x,e=S.symbols('x e');p=(x*x-1)*(x*x-4);L=(7*x-x**3)/6;Q=(x*x-9)/36;P=S.Poly(p*p-1,x); n=8
# Newton trace moments: derive via companion matrix
C=S.zeros(n)
for j in range(n-1):C[j+1,j]=1
for j in range(n):C[j,n-1]=-P.nth(j)
mu=[S.Rational(n,n)]; powC=S.eye(n)
for j in range(1,25):powC=powC*C;mu.append(S.trace(powC)/n)
def E(f):
 f=S.Poly(S.rem(S.Poly(S.expand(f),x),P).as_expr(),x)
 return S.expand(sum(c*mu[k[0]] for k,c in f.terms()))
f=S.Matrix([1,x,x*x,x**3]);G=S.Matrix(4,4,lambda i,j:E(f[i]*f[j]));B=S.Matrix(4,4,lambda i,j:E(p*L*f[i]*f[j]));qc=S.Matrix([S.expand(Q).coeff(x,j)for j in range(4)]);DQ=(f.T*G.inv()*B*qc)[0]
assert S.expand(L*L-1-p*Q)==0
assert all(E(p*x**j)==0 for j in range(4))
q1=p+e*L+e**2*Q+e**3*DQ
raw=S.Poly(S.expand((1-e*p*L)*q1*q1),e)
rawc=[S.rem(S.Poly(raw.nth(j),x),P).as_expr()for j in range(4)]
hc=[E(z)for z in rawc]
# divide raw by its expectation to order3
w2=[]
for j in range(4):w2.append(S.expand((rawc[j]-sum(hc[k]*w2[j-k]for k in range(1,j+1)))/hc[0]))
vc=[S.rem(S.Poly((p*L)**j,x),P).as_expr()for j in range(4)];cc=[E(z)for z in vc];we=[]
for j in range(4):we.append(S.expand(vc[j]-sum(cc[k]*we[j-k]for k in range(1,j+1))))
for j in range(3):assert S.rem(S.Poly(w2[j]-we[j],x),P).is_zero
expected=2*(p*DQ-L*Q+E(L*Q));assert S.rem(S.Poly(w2[3]-we[3]-expected,x),P).is_zero
print('PASS exact cubic drift identity; DQ=',S.factor(DQ),'drift=',S.factor(S.rem(S.Poly(expected,x),P).as_expr()))
