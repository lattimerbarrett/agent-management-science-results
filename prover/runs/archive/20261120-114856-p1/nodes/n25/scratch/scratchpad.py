import sympy as S
x,a=S.symbols('x a',real=True)
nodes=list(map(S.Integer,[-3,-1,1,2,3]));n=5;s=3
chi=S.prod(x-t for t in nodes);p=x**3-7*x;h=S.Integer(36)
d=[1/S.prod(t-u for u in nodes if u!=t) for t in nodes]
w=S.Matrix([S.factor(h*di*(t-a)/p.subs(x,t)) for t,di in zip(nodes,d)])
print('chi=',S.expand(chi)); print('plateau factorization=',S.factor(p*p-h));print('stationary weights=',list(w));print('sum=',S.factor(sum(w)))
X=S.Matrix([[t**j for j in range(s)] for t in nodes]);pv=S.Matrix([p.subs(x,t) for t in nodes]);W=S.diag(*list(w));M=X.T*W*X
assert X.T*W*pv==S.zeros(3,1)
P=S.diag(*[1/z for z in pv])*X*M.inv()*X.T*W*S.diag(*list(pv))
J=S.eye(5)-2*P
assert S.simplify(J*J)==S.eye(5)
print('At every a in (1,2): full-support stationary two-cycle, D(T^2)=I exactly.')
# Check scalar recurrence for arbitrary 5-node weights exactly.
v=S.Matrix([S.Rational(t,15) for t in [1,2,3,4,5]])
def theta(v):
 z=[di**2/vi for di,vi in zip(d,v)];return S.factor(sum(t*zi for t,zi in zip(nodes,z))/sum(z))
def T(v):
 av=theta(v);u=S.Matrix([di**2/vi*(t-av)**2 for t,di,vi in zip(nodes,d,v)]);return u/sum(u)
aa=theta(v);v1=T(v);bb=theta(v1);v2=T(v1);cc=theta(v2)
z=[di**2/vi for di,vi in zip(d,v)]
ratio=sum(zi*(t-aa)/(t-bb) for t,zi in zip(nodes,z))/sum(zi*((t-aa)/(t-bb))**2 for t,zi in zip(nodes,z))
print('recurrence discrepancy=',S.factor(cc-bb-(bb-aa)*ratio))
print('theta samples=',[float(t) for t in [aa,bb,cc]])
