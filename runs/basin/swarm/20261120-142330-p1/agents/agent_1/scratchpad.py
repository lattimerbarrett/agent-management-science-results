import sympy as S
lam=list(map(S.Rational,[1,2,4,7,11,13,17]))
def step(w,s):
 n=len(w);H=S.Matrix(s,s,lambda i,j:sum(w[t]*lam[t]**(i+j) for t in range(n)))
 a=H.inv()*S.Matrix([-sum(w[t]*lam[t]**(i+s) for t in range(n)) for i in range(s)])
 p=[lam[t]**s+sum(a[i]*lam[t]**i for i in range(s)) for t in range(n)]
 f=sum(w[t]*p[t]**2 for t in range(n))
 return [S.cancel(w[t]*p[t]**2/f) for t in range(n)],p,f,a
for s in [1,2,3,4]:
 w=[S.Rational(i,28) for i in range(1,8)]
 w1,p,f,a=step(w,s);w2,q,g,b=step(w1,s);w3,r,h,c=step(w2,s)
 e=[p[i]*q[i]-f for i in range(len(w))]
 for j in range(s):
  lhs=sum(w2[i]*lam[i]**j*(r[i]-p[i]) for i in range(len(w)))
  rhs=-sum(w[i]*p[i]*lam[i]**j*e[i]**2 for i in range(len(w)))/(f*g)
  assert S.cancel(lhs-rhs)==0
 print('Exact two-block polynomial-change identity checked for s=',s)
