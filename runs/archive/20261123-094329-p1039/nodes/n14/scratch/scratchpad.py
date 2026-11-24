import sympy as s
# Restrict the nonpseudoconvex quartic to the complex two-plane
# z_3=...=z_n=0, at q=(0,sqrt(3),0,...,0).
x,y,u,v=s.symbols('x y u v', real=True)
rho=(x*x+y*y-1)**2+u*u+v*v-4
q={x:0,y:0,u:s.sqrt(3),v:0}
levi11=s.simplify((s.diff(rho,x,2)+s.diff(rho,y,2))/4)
print('Levi value in the negative tangential direction:',levi11.subs(q))
print('Exterior slice Levi value:',-levi11.subs(q))
# In ambient dimension >=3, a point may lie outside K only because
# of its discarded coordinates. Thus orthogonal projection need not
# map the exterior to the exterior slice.
print('rho at projected origin:',rho.subs({x:0,y:0,u:0,v:0}))
print('rho at ambient point (0,0,2,0,...):',rho.subs({x:0,y:0,u:0,v:0})+4)
print('Therefore projection is not a retraction of the exterior onto its slice.')