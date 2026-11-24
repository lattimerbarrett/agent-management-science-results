import sympy as sp
m3,v,m4=sp.symbols('m3 v m4', nonzero=True)
t=sp.symbols('t')
poly=sp.Poly((t*t-m3/v*t-v)**2,t)
mom={0:1,1:0,2:v,3:m3,4:m4}
pearson=sp.expand(sum(c*mom[i[0]] for i,c in poly.terms()))
vp=m4/v-(m3/v)**2
assert sp.simplify(vp-v-pearson/v)==0
p,a,b=sp.symbols('p a b',real=True)
mu=p*a+(1-p)*b
var=sp.factor(p*(a-mu)**2+(1-p)*(b-mu)**2)
assert sp.simplify(var-p*(1-p)*(a-b)**2)==0
pnext=sp.factor(p*(a-mu)**2/var)
assert sp.simplify(pnext-(1-p))==0
mu2=sp.expand((1-p)*a+p*b)
assert sp.simplify((mu-a)*(mu2-a)-var)==0
assert sp.simplify((mu-b)*(mu2-b)-var)==0
print('Verified variance increment identity, two-point mass swap, and normalized vector two-cycle identity symbolically.')
