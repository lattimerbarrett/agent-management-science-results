import sympy as S
nodes=list(map(S.Rational,[1,2,4,7]))
w=list(map(S.Rational,[1,3,2,4])); w=[x/sum(w) for x in w]
x=S.symbols('x')
d=[1/S.prod(t-u for u in nodes if u!=t) for t in nodes]
def theta(w):
 z=[dd**2/ww for dd,ww in zip(d,w)]
 return sum(t*zz for t,zz in zip(nodes,z))/sum(z)
def step(w):
 A=S.Matrix([[sum(wi*t**(i+j) for wi,t in zip(w,nodes)) for j in range(2)] for i in range(2)])
 rhs=-S.Matrix([sum(wi*t**(i+2) for wi,t in zip(w,nodes)) for i in range(2)])
 co=A.inv()*rhs
 vals=[t*t+co[1]*t+co[0] for t in nodes]
 h=sum(wi*val**2 for wi,val in zip(w,vals))
 return [wi*val**2/h for wi,val in zip(w,vals)]
a=theta(w);wp=step(w);b=theta(wp);c=theta(step(wp))
z=[dd**2/ww for dd,ww in zip(d,w)]
rhs=(b-a)*sum(zz*(t-a)/(t-b) for zz,t in zip(z,nodes))/sum(zz*((t-a)/(t-b))**2 for zz,t in zip(z,nodes))
print('a,b,c',a,b,c)
print('recurrence defect',S.factor(c-b-rhs))
print('old answer theorem supplied no author, statement, explicit A, or initial residual')
