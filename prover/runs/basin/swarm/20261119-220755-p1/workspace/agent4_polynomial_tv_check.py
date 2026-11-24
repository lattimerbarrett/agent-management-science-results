import sympy as S
x=S.symbols('x')
nodes=list(map(S.Rational,[-3,-2,-1,1,2,3]))
p=[S.Rational(i,21) for i in range(1,7)]
s=3
v=lambda a:S.Matrix([a**j for j in range(s)])
def step(p):
 M=sum((w*v(a)*v(a).T for a,w in zip(nodes,p)),S.zeros(s))
 rhs=-sum((w*a**s*v(a) for a,w in zip(nodes,p)),S.zeros(s,1))
 c=M.inv()*rhs;f=x**s+sum(c[j]*x**j for j in range(s))
 N=sum(w*f.subs(x,a)**2 for w,a in zip(p,nodes))
 pp=[S.cancel(w*f.subs(x,a)**2/N) for w,a in zip(p,nodes)]
 return pp,f,S.cancel(N)
p1,f,N=step(p);p2,g,NN=step(p1);p3,h,NNN=step(p2)
H=S.expand(f*g)
M2=sum((w*v(a)*v(a).T for a,w in zip(nodes,p2)),S.zeros(s))
diff=S.Matrix([S.expand(h-f).coeff(x,j) for j in range(s)])
rhs=-sum((w*f.subs(x,a)*(H.subs(x,a)-N)**2*v(a)/(N*NN) for w,a in zip(p,nodes)),S.zeros(s,1))
assert all(S.cancel(z)==0 for z in M2*diff-rhs)
variance=sum(w*(H.subs(x,a)-N)**2 for w,a in zip(p,nodes))
assert S.cancel(variance-N*(NN-N))==0
print('Exact OP coefficient finite-variation identity and variance identity verified.')
