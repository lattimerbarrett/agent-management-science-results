import sympy as s
x1,y1,x2,y2,x3,y3=s.symbols('x1 y1 x2 y2 x3 y3', real=True)
xs=[x1,x2,x3]; ys=[y1,y2,y3]
rho=(x1*x1+y1*y1-1)**2+x2*x2+y2*y2+x3*x3+y3*y3-2
p={x1:0,y1:0,x2:1,y2:0,x3:0,y3:0}
# Complex Hessian d^2 rho / (dz_j dbar z_k)
L=s.Matrix(3,3,lambda j,k:(s.diff(rho,xs[j],xs[k])+s.diff(rho,ys[j],ys[k])+s.I*(s.diff(rho,xs[j],ys[k])-s.diff(rho,ys[j],xs[k])))/4)
print('rho(p) =',rho.subs(p))
print('complex gradient at p =',[(s.diff(rho,xs[j])-s.I*s.diff(rho,ys[j])).subs(p)/2 for j in range(3)])
print('complex Hessian at p =',L.subs(p))
print('Tangential Levi eigenvalues (directions z1,z3):',L.subs(p).extract([0,2],[0,2]).eigenvals())
print('This exhibits a smooth compact obstacle with mixed Levi signature; it makes no claim that its complement is Oka.')
