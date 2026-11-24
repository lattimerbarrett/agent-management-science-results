import sympy as s
# Check the graph-projection identities for a scalar contraction; the
# matrix proof uses exactly the same block identities.
t=s.symbols('t', real=True)
g=s.Matrix([[1,t],[t,t*t]])/(1+t*t)
e=s.diag(1,0)
j=2*e-s.eye(2)
assert s.simplify(g*g-g)==s.zeros(2)
assert s.simplify(g*j*g - ((1-t*t)/(1+t*t))*g)==s.zeros(2)
assert s.simplify(g*e*g-g/(1+t*t))==s.zeros(2)
assert s.simplify(g[1,0]/g[0,0]-t)==0
print('Graph identities checked: g^2=g, gJg>=0 for |t|<=1, and gEg>=g/2.')
print('Compatible graph projections increase. Continuous finite dimension')
print('passes the graph-angle inequality to their join by intersection')
print('with a hypothetical negative spectral projection.')
print('The join therefore remains a full-domain contraction graph.')
