import sympy as s
# Candidate K_n: sum_{j=1}^{n-1}|z_j|^2+(|w|^2-1)^2<=2.
# Verify the complex Levi matrix via Wirtinger derivatives in dimensions 3..8.
for n in range(3,9):
    z=s.symbols('z0:'+str(n)); zb=s.symbols('b0:'+str(n))
    rho=sum(z[j]*zb[j] for j in range(n-1))+(z[-1]*zb[-1]-1)**2-2
    L=s.Matrix(n,n,lambda j,k:s.diff(rho,z[j],zb[k]))
    expected=s.diag(*([1]*(n-1)+[4*z[-1]*zb[-1]-2]))
    assert s.simplify(L-expected)==s.zeros(n)
    point={a:0 for a in z+zb};point[z[0]]=point[zb[0]]=1
    assert rho.subs(point)==0
    assert s.diff(rho,z[-1]).subs(point)==0
    assert L[-1,-1].subs(point)==-2
    # Boundary critical points must have z'=0 and either w=0 or |w|^2=1.
    # Those have rho=-1 or -2, so none is on rho=0.
    assert rho.subs({a:0 for a in z+zb})==-1
print('Verified exact Levi and negative complex-tangent value for n=3,...,8.')
# Dimension-free scalar identities for gradient norm and radial star-shaped path.
u,t,lam=s.symbols('u t lam',nonnegative=True)
rho=u+(t-1)**2-2
print('rho=',rho)
print('boundary gradient norm squared /4 =',u+4*t*(t-1)**2)
# Vanishing gradient forces u=0 and t(t-1)=0 (sum of nonnegative terms).
# The resultant certifies these critical-point equations never meet rho=0.
assert s.resultant(rho.subs(u,0),t*(t-1),t)==2
# On rho<=0, u<=2 and 0<=t<=1+sqrt(2), giving boundedness.
assert s.expand(rho-(u+t*t-2*t-1))==0
# Connectivity: all vertical slices over |w|²<1+sqrt2 are balls centered at zero;
# their centers lie in a disk, and hence domain is connected.
assert s.solve(s.Eq((t-1)**2,2),t)==[1+s.sqrt(2)]
print('Projection onto w is disk |w|²<1+sqrt(2); all nonempty z-fibers are balls.')
# The candidate is even strictly star-shaped and diffeomorphic to a closed ball.
# For real spatial scaling sqrt(lam), rho becomes lam*u+(lam*t-1)^2-2.
scaled=lam*u+(lam*t-1)**2-2
assert s.diff(scaled,lam,2)==2*t**2
# Boundary radial derivative is strictly positive (1+t^2).
assert s.expand(s.diff(scaled,lam).subs(lam,1).subs(u,2-(t-1)**2))==1+t**2
print('Boundary radial derivative = 1+t² >0; K is strictly star-shaped.')
