import sympy as S,os
x=S.symbols('x'); nodes=[S.Rational(z)for z in [1,2,4,7,11,16,22]]; w=[S.Rational(z,28)for z in range(1,8)]
def op(w,s):
 G=S.Matrix(s,s,lambda j,k:sum(ww*xx**(j+k)for ww,xx in zip(w,nodes)));bb=S.Matrix([-sum(ww*xx**(s+j)for ww,xx in zip(w,nodes))for j in range(s)]);c=G.inv()*bb;q=x**s+sum(c[j]*x**j for j in range(s));h=sum(ww*q.subs(x,xx)**2for ww,xx in zip(w,nodes));return q,h
for s in [1,2,3,4]:
 q,h=op(w,s);wp=[ww*q.subs(x,xx)**2/h for ww,xx in zip(w,nodes)];r,hn=op(wp,s)
 for xi in [0,1,3,10]:
  Z=sum(ww/(xx+xi)for ww,xx in zip(w,nodes));v=[ww/(xx+xi)/Z for ww,xx in zip(w,nodes)];p=q/q.subs(x,-xi);pn=r/r.subs(x,-xi);gamma=sum(vv*p.subs(x,xx)**2for vv,xx in zip(v,nodes));vp=[vv*p.subs(x,xx)**2/gamma for vv,xx in zip(v,nodes)];gamman=sum(vv*pn.subs(x,xx)**2for vv,xx in zip(vp,nodes))
  assert gamman>=gamma
  cross=sum(vv*p.subs(x,xx)*pn.subs(x,xx)for vv,xx in zip(v,nodes));assert cross==gamma
  var=sum(vv*(p.subs(x,xx)*pn.subs(x,xx)-gamma)**2for vv,xx in zip(v,nodes));assert var==gamma*(gamman-gamma)
print('PASS shifted-error Lyapunov/Cauchy exact rational checks for s1..4,4shifts')
