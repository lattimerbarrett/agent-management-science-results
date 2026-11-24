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
# Save reusable self-contained verification, not a claim of Oka-ness.
from pathlib import Path
Path('workspace/agent4_geometry_checks.py').write_text(Path(__file__).read_text().split('# Save reusable')[0])
Path('workspace/agent4_nonpseudoconvex_candidate.md').write_text(r'''# Verified candidate geometry (Oka complement NOT proved)
For n>=3 write z in C^(n-1), w in C, and let
rho(z,w)=||z||^2+(|w|^2-1)^2-2, Omega={rho<0}, K={rho<=0}.

Put u=||z||^2 and t=|w|^2. On K, u<=2 and t<=1+sqrt(2), so K is compact. The origin has rho=-1. Under real radial scaling by sqrt(lambda), rho becomes lambda*u+(lambda*t-1)^2-2, a convex function of lambda. Its endpoint values on [0,1] are nonpositive, and strictly negative for lambda<1. Thus Omega is star-shaped, nonempty and connected; K=closure(Omega).

The squared real gradient divided by four is u+4t(t-1)^2. This cannot vanish on rho=0: vanishing requires u=0 and t=0 or 1, which give rho=-1 or -2. Hence boundary is C-infinity. In fact, the outward radial derivative on boundary is u+2t(t-1)=1+t^2>0, so K is strictly star-shaped and diffeomorphic to a closed real ball.

The complex Levi matrix is diag(1,...,1,4t-2). At p=((1,0,...,0),0), rho=0 and partial rho/partial w=0. Thus the complex w-direction is tangential, with Levi value -2. Boundary is not pseudoconvex.

At every boundary point, the positive coordinate subspace C^(n-1) x {0} intersects the complex tangent hyperplane in dimension at least n-2. The Levi form there is the standard positive form. Thus K has at least n-2 positive tangential Levi eigenvalues everywhere, and its defining function has at least n-1 positive ambient Levi eigenvalues everywhere.

What is NOT established: C^n minus K is Oka. A full-CAP complement theorem for smooth compact domains with at least n-2 positive tangential Levi eigenvalues, in dimension n>=3, would imply it immediately. No such theorem is asserted here without proof/source.
''')
# Exact algebra for refuting another tempting but FALSE auxiliary lemma.
# A nondegenerate entire map need not have connected outside-ball preimages.
h,g=s.symbols('h g')
T=s.Matrix([s.exp(h*h),s.exp(h*h)*g])
assert s.factor(T.jacobian([h,g]).det())==2*h*s.exp(2*h*h)
v=s.symbols('v',nonnegative=True)
assert s.simplify(s.diff(s.exp(-2*v)*(1+v),v))==(-1-2*v)*s.exp(-2*v)
barrier=(s.exp(-h*h)-s.exp(-2*h*h))/(h*h)
assert s.limit(barrier,h,0)==1
assert s.Rational(5,16)<s.Rational(1,2)
assert s.E<4
Path('workspace/agent4_disconnected_superlevels.md').write_text(r'''# Negative control: rank-two entire maps can have disconnected superlevels
Take an attracting quadratic Henon basin B, with a Fatou--Bieberbach parametrization (h,g): C^2 -> B. The standard escape cone implies B lies in the horn |g|<=max(|h|,R0), with R0>=1.
Define G=(exp(h^2), exp(h^2)g). Its Jacobian is 2h exp(2h^2) times the nonvanishing Jacobian of (h,g), hence G is nondegenerate.
On Re h=0, writing h=iy, the squared norm is at most exp(-2y^2)(1+max(y^2,R0^2)) <=1+R0^2. For y^2<=R0^2 this is immediate; for y^2>=R0^2 use exp(-2s)(1+s)<=1 (its derivative is negative).
The nonconstant entire scalar function h takes every complex value except possibly one, by restricting to a complex line where it is nonconstant and applying Picard. Thus for arbitrarily large T, both h=T and h=-T occur. At those points ||G||>=exp(T^2).
For L>sqrt(1+R0^2), G^{-1}({||z||>L}) consequently has nonempty portions in Re h>0 and Re h<0 but no point with Re h=0. It is disconnected.
This refutes the proposed universal connectivity lemma. It is NOT a target Oka counterexample.

## Stronger negative control: finite source curves / psh hulls
Let C=sqrt(1+R0^2), L=4C, and f(h)=(exp(-h^2)-exp(-2h^2))/h^2, extended by f(0)=1. This f is entire.
If ||G||>L then |h|>1, since for |h|<=1 the horn gives ||G||<=e*C<4C. Put r=|h|>1 and a=exp(-Re h^2). The horn gives ||G||<=exp(Re h^2)*C*r, hence a<C*r/L=r/4. Consequently |f(h)|<=a*(1+a)/r^2<1/(4r)+1/16<5/16.
At h=iy with y nonzero, f(iy)=exp(y^2)*(exp(y^2)-1)/y^2>1. Thus v=max(log|2f(h)|,-1) is a global continuous psh function, positive at separator points h=iy (where G has full rank), but negative on {||G||>L}.
Therefore the psh hull of the outside-ball preimage need not contain such a regular point. Also no compact bordered source curve through such a point can have its whole boundary in that outside-ball preimage, by the maximum principle for v restricted to the curve. This refutes the proposed generic finite-source-curve selection lemma as well.
''')
print('Checked determinant and scalar inequality for disconnected-superlevel negative control.')
Path('workspace/agent4_disconnected_superlevel_checks.py').write_text('import sympy as s\nh,g=s.symbols("h g")\nT=s.Matrix([s.exp(h*h),s.exp(h*h)*g])\nassert s.factor(T.jacobian([h,g]).det())==2*h*s.exp(2*h*h)\nv=s.symbols("v",nonnegative=True)\nassert s.simplify(s.diff(s.exp(-2*v)*(1+v),v))==(-1-2*v)*s.exp(-2*v)\nbarrier=(s.exp(-h*h)-s.exp(-2*h*h))/(h*h)\nassert s.limit(barrier,h,0)==1\nassert s.Rational(5,16)<s.Rational(1,2)\nassert s.E<4\nprint("Exact determinant, monotonicity, and barrier checks passed.")\n')
