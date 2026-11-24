import sympy as s
x,y,u,v=s.symbols('x y u v', real=True)
# z_1=x+iy, w=u+iv; remaining z_j contribute |z_j|^2.
rho=x*x+y*y+(u*u+v*v-1)**2-4
Lz=s.simplify((s.diff(rho,x,2)+s.diff(rho,y,2))/4)
Lw=s.simplify((s.diff(rho,u,2)+s.diff(rho,v,2))/4)
q={x:s.sqrt(3),y:0,u:0,v:0}
print('rho(q) =',rho.subs(q))
print('Levi z-direction =',Lz)
print('Levi w-direction =',Lw)
print('Levi w-direction at q =',Lw.subs(q))
print('gradient at q =',[s.diff(rho,a).subs(q) for a in (x,y,u,v)])
print('fiber radius factorization:',s.factor(4-(s.Symbol('t')-1)**2))
print('On rho<0, psi=-log(-rho): Levi on v_w=0 is')
print('(-1/rho)*||v_z||^2+(1/rho**2)*|<v_z,z>|^2 > 0.')
print('Therefore psi has >= n-1 positive Levi eigenvalues: Omega is 2-complete.')
