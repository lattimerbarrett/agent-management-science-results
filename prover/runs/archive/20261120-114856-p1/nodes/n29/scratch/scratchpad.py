import sympy as S
x=S.symbols('x')
def inner(w,l,f):
 return S.expand(sum(wi*f.subs(x,li) for wi,li in zip(w,l)))
def poly(w,l,s):
 G=S.Matrix([[sum(wi*li**(i+j) for wi,li in zip(w,l)) for j in range(s)] for i in range(s)])
 b=S.Matrix([-sum(wi*li**(s+i) for wi,li in zip(w,l)) for i in range(s)])
 c=G.inv()*b
 p=x**s+sum(c[j]*x**j for j in range(s))
 h=inner(w,l,p*p)
 wn=[S.cancel(wi*p.subs(x,li)**2/h) for wi,li in zip(w,l)]
 return S.expand(p),h,wn
for s in range(1,5):
 l=list(map(S.Integer,range(1,s+4)))
 raw=list(map(S.Integer,range(2,s+5)))
 w=[t/sum(raw) for t in raw]
 p,h,wp=poly(w,l,s)
 q,hp,wpp=poly(wp,l,s)
 r,hpp,wppp=poly(wpp,l,s)
 e=S.expand(p*q-h)
 assert S.cancel(inner(w,l,e*e)-h*(hp-h))==0
 for j in range(s):
  lhs=inner(wpp,l,(r-p)*x**j)
  rhs=-inner(w,l,e*e*p*x**j)/(h*hp)
  assert S.cancel(lhs-rhs)==0
 print('Exact Lyapunov and polynomial finite-variation identities verified for s=',s)
# Check the purported isolating data on a continuum of exact cycles.
a=S.symbols('a')
l=[S.Integer(v) for v in [1,3,5,7]]
w=[a,3*a-S.Rational(1,2),1-3*a,S.Rational(1,2)-a]
p,h,wp=poly(w,l,2)
q,hp,wpp=poly(wp,l,2)
assert all(S.simplify(u-v)==0 for u,v in zip(w,wp))
assert S.simplify(p-(x*x-8*x+11))==0 and S.simplify(h-16)==0 and S.simplify(q-p)==0
print('A whole positive segment has identical p,q,h, yet distinct first moments:',S.expand(sum(wi*li for wi,li in zip(w,l))))
