import sympy as S
x=S.symbols('x')
def step(nodes,w,s=2):
 c=S.symbols('c:'+str(s))
 p=x**s+sum(c[j]*x**j for j in range(s))
 sol=S.solve([sum(wi*p.subs(x,t)*t**j for t,wi in zip(nodes,w)) for j in range(s)],c)
 p=S.Poly(p.subs(sol),x).as_expr()
 h=S.factor(sum(wi*p.subs(x,t)**2 for t,wi in zip(nodes,w)))
 return p,h,[S.factor(wi*p.subs(x,t)**2/h) for t,wi in zip(nodes,w)]
for n in [4,5,6]:
 nodes=list(map(S.Rational,range(1,n+1)));w=[S.Rational(i+1,n*(n+1)//2) for i in range(n)]
 p,h,v=step(nodes,w);q,hp,u=step(nodes,v);r,hpp,_=step(nodes,u)
 e=p*q-h
 assert S.factor(sum(wi*e.subs(x,t)**2 for t,wi in zip(nodes,w))-h*(hp-h))==0
 for f in [S.Integer(1),x]:
  lhs=sum(ui*(r-p).subs(x,t)*f.subs(x,t) for t,ui in zip(nodes,u))
  rhs=-sum(wi*(e**2*p*f).subs(x,t) for t,wi in zip(nodes,w))/(h*hp)
  assert S.factor(lhs-rhs)==0
 if n==4:
  d=[1/S.prod(t-a for a in nodes if a!=t) for t in nodes]
  def theta(w): return S.factor(sum(t*di**2/wi for t,di,wi in zip(nodes,d,w))/sum(di**2/wi for di,wi in zip(d,w)))
  a,b,c=theta(w),theta(v),theta(u)
  z=[di**2/wi for di,wi in zip(d,w)]
  rhs=(b-a)*sum(zi*(t-a)/(t-b) for zi,t in zip(z,nodes))/sum(zi*((t-a)/(t-b))**2 for zi,t in zip(z,nodes))
  assert S.factor((c-b)-rhs)==0
  ratios=[S.factor(vi/(di**2/wi*(t-a)**2)) for vi,di,wi,t in zip(v,d,w,nodes)]
  assert len(set(ratios))==1
 print('Exact identities passed: n=',n)
print('These checks verify algebraic samples, not a boundary-itinerary certificate.')
