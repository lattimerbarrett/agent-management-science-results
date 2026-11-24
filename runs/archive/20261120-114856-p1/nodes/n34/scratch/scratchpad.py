import sympy as S
x,eps=S.symbols('x eps', positive=True)
nodes=[S.Integer(1),S.Integer(2),S.Integer(4),S.Integer(7)]
weights=[S.Rational(1,6)*(1-eps),S.Rational(1,3)*(1-eps),S.Rational(1,2)*(1-eps),eps]
P=S.prod(x-a for a in nodes)
N=S.cancel(sum(w*P/(x-a) for a,w in zip(nodes,weights))).expand()
M=S.Matrix(2,2,lambda i,j:sum(w*a**(i+j) for a,w in zip(nodes,weights)))
b=S.Matrix([-sum(w*a**(i+2) for a,w in zip(nodes,weights)) for i in range(2)])
c=M.inv()*b
q=x*x+c[1]*x+c[0]
h=S.factor(sum(w*q.subs(x,a)**2 for a,w in zip(nodes,weights)))
u=S.rem(S.Poly(S.cancel(q*N),x),S.Poly(P,x)).as_expr()
Nnext=S.cancel(sum((w*q.subs(x,a)**2/h)*P/(x-a) for a,w in zip(nodes,weights)))
assert S.cancel(Nnext-q*u/h)==0
assert S.Poly(u,x).degree()==1
eta=S.factor(-S.Poly(u,x).nth(0)/S.Poly(u,x).nth(1))
print('Exact identity: R_next(z) = q(z) u(z) / (h P(z)).')
print('Free Stieltjes zero eta(eps) =',eta)
print('Limit eta as disappearing weight tends to zero:',S.limit(eta,eps,0,dir='+'))
print('Its derivative at eps=0:',S.factor(S.diff(eta,eps).subs(eps,0)))
print('Residual monic q limit:',S.factor(q.subs(eps,0)))
print('Stieltjes numerator at eps=0:',S.factor(N.subs(eps,0)))
print('The zero at 7 cancels a pole only at eps=0; for eps>0 its contribution must be retained.')
from pathlib import Path
for name in ['root_connection_checks_agent2.py','root_barrier_checks_agent2.py']:
    path=Path('experiments/e1')/name
    print('\nChecking',name)
    exec(compile(path.read_text(),str(path),'exec'), {'__name__':'__main__'})
