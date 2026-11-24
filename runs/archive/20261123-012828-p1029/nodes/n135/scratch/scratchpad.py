import sympy as s
t,u,c=s.symbols('t u c', real=True)
# Two rank-one projections, with ||PQ|| = |c|.
P=s.diag(1,0)
Q=s.Matrix([[c*c,c*s.sqrt(1-c*c)],[c*s.sqrt(1-c*c),1-c*c]])
D=s.factor((s.eye(2)-t*P-u*Q).det())
print('det(1-tP-uQ)=',D)
assert s.simplify(D-((1-t)*(1-u)-t*u*c*c))==0
print('Hence positivity requires ||PQ||^2 <= (1-t)(1-u)/(t*u).')
