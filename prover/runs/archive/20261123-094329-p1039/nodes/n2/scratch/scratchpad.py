import sympy as s
x,y,u,v=s.symbols('x y u v', real=True)
rho=1-x*x-y*y-u*u-v*v
# rho <= 0 defines the exterior of the closed unit ball locally.
levi=s.diag((s.diff(rho,x,2)+s.diff(rho,y,2))/4,(s.diff(rho,u,2)+s.diff(rho,v,2))/4)
print('Levi form for the exterior of the unit ball:',levi)
print('Levi form for its compact complement:',-levi)
