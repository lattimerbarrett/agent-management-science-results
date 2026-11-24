import sympy as s
x,y=s.symbols('x y',real=True)
r=x*x+y*y
# rho=(|z|^2-1)^2+||w||^2-2
rho=(r-1)**2-2
levi_z=s.simplify((s.diff(rho,x,2)+s.diff(rho,y,2))/4)
print('z Levi eigenvalue:',levi_z)
print('At z=0, ||w||=1: tangent Levi eigenvalues are -2, followed by n-2 copies of 1.')
print('Critical values of rho occur at (z,w)=(0,0) or (|z|,w)=(1,0):',rho.subs({x:0,y:0}),rho.subs({x:1,y:0}))
