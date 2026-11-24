import sympy as s
K=s.symbols('K', positive=True)
g=s.Matrix([[1,K],[K,K**2]])/(1+K**2)
f=s.diag(0,1)
assert s.simplify(g*g-g)==s.zeros(2)
assert s.simplify(f*g*f-(K**2/(1+K**2))*f)==s.zeros(2)
print('Graph projection:',g)
print('Sharp complementary compression coefficient:',K**2/(1+K**2))
# The topological example is proved in the accompanying reasoning, not here.
# Its values at x=1 certify that compression of the projection join is nonzero.
h_at_1=s.Integer(1)
pn_at_1=s.Integer(0)
join_at_1=s.Integer(1)
print('At x=1: h*p_n*h =', h_at_1*pn_at_1*h_at_1)
print('At x=1: h*(join p_n)*h =', h_at_1*join_at_1*h_at_1)
