import sympy as S
x=S.symbols('x')
nodes=list(map(S.Rational,[-3,-2,-1,1,2,3]))
d=[S.prod(a-b for b in nodes if b!=a) for a in nodes]
p=[S.Rational(i,21) for i in range(1,7)]
def norm(p):
 z=sum(p);return [S.cancel(a/z) for a in p]
def R(p):return norm([1/(di*di*pi) for di,pi in zip(d,p)])
def dual(q):
 M=S.Matrix([[sum(w*a**(i+j) for w,a in zip(q,nodes)) for j in range(2)] for i in range(2)])
 b=S.Matrix([-sum(w*a**(i+2) for w,a in zip(q,nodes)) for i in range(2)])
 c=M.inv()*b
 return x*x+c[1]*x+c[0]
def step(p):
 q=R(p);h=dual(q)
 return norm([w*h.subs(x,a)**2 for w,a in zip(q,nodes)])
q=R(p);H=dual(q);p1=step(p);h=dual(R(p1));p2=step(p1);h2=dual(R(p2))
delta=h-H;eta=h2-h
vec=lambda f:S.Matrix([S.expand(f).coeff(x,i) for i in range(2)])
M2=S.zeros(2);M1=S.zeros(2);rhs=S.zeros(2,1)
for w,a in zip(q,nodes):
 v=S.Matrix([1,a]);rr=H.subs(x,a)/h.subs(x,a)
 M2+=w*rr**2*v*v.T;M1+=w*rr*v*v.T
 rhs+=w*H.subs(x,a)*delta.subs(x,a)**2/h.subs(x,a)**2*v
assert all(S.cancel(v)==0 for v in M2*vec(eta)-M1*vec(delta))
assert all(S.cancel(v)==0 for v in M2*vec(eta-delta)-rhs)
print('Exact rational dual-polynomial recurrence verified (n6,s3).')
