import sympy as s
b0,b1,b2=s.symbols('b0 b1 b2')
es=[b0+b1+b2,
    b0*b1+b0*b2+3*b0+b1*b2+2*b1+b2,
    2*b0*b1+b0*b2+2*b0]
G=s.groebner(es,b0,b1,b2)
points=s.solve_poly_system(list(G),b0,b1,b2)
assert set(points)=={(0,0,0),(0,1,-1),(1,-1,0),(2,0,-2)}
assert all(all(e.subs(dict(zip((b0,b1,b2),p)))==0 for e in es) for p in points)
print('P2 ranks111 exact points:',points)
