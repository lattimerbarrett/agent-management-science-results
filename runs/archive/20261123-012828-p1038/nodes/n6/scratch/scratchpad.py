import sympy as s
T=s.symbols('T')
x,y,u,v,z=s.symbols('x y u v z', positive=True)
P=[(1-x*T)*(1-y*T),(T+x)*(1-z*T)*(1+u*T),(T+y)*(T+z)*(1+v*T),T*(T-u)*(T-v)]
M=s.Matrix([[s.expand(p).coeff(T,e) for e in range(4)] for p in P])
det=s.Poly(s.expand(M.det()),x,y,u,v,z)
print('Number of determinant monomials:',len(det.terms()))
print('Coefficient signs:',set(s.sign(c) for _,c in det.terms()))
# Map the unit cube to positive orthant and inspect numerator signs.
a,b,c,d,e=s.symbols('a b c d e',positive=True)
newvars=[a,b,c,d,e]
oldvars=[x,y,u,v,z]
expr=0
for powers,coeff in det.terms():
    term=coeff
    for q,k in zip(newvars,powers):
        term*=q**k*(1+q)**(2-k)
    expr+=term
p=s.Poly(s.expand(expr),*newvars)
neg=[(mon,coef) for mon,coef in p.terms() if coef<0]
print('Unit cube Bernstein negative coefficients:',neg)
print('Number of nonzero coefficients:',len(p.terms()))
