import sympy as s
from pathlib import Path

# Independent coordinate-level curvature checks of conformal flat metrics.
def conformal_curvature_check(n):
    p=s.symbols('p0:'+str(n)); q=s.symbols('q0:'+str(n))
    h=[[s.Symbol('h%d_%d'%(min(i,j),max(i,j))) for j in range(n)] for i in range(n)]
    delta=lambda i,j: s.Integer(i==j)
    # Gamma^k_ij = delta_ki phi_j+delta_kj phi_i-delta_ij phi_k.
    G=lambda k,i,j:delta(k,i)*p[j]+delta(k,j)*p[i]-delta(i,j)*p[k]
    dG=lambda a,k,i,j:delta(k,i)*h[j][a]+delta(k,j)*h[i][a]-delta(i,j)*h[k][a]
    ric=[]
    for i in range(n):
        ric.append(s.expand(sum(dG(k,k,i,i)-dG(i,k,i,k)+sum(G(k,k,l)*G(l,i,i)-G(k,i,l)*G(l,i,k) for l in range(n)) for k in range(n))))
    # R * exp(2 phi).
    R=s.expand(sum(ric))
    expected=-(n-1)*(2*sum(h[i][i] for i in range(n))+(n-2)*sum(t*t for t in p))
    assert s.expand(R-expected)==0
    contracted=[s.expand(sum(G(k,i,i) for i in range(n))) for k in range(n)]
    assert all(s.expand(contracted[k]+(n-2)*p[k])==0 for k in range(n))

for n0 in range(3,11): conformal_curvature_check(n0)
print('Coordinate Christoffel/Ricci/Laplacian checks passed for dimensions 3,...,10.')

n,r,lam=s.symbols('n r lam',positive=True)
a=(n-2)/2
U=(lam/(lam**2+r**2))**a
# Radial Euclidean Laplacian checks the precise n(n-2) normalization.
res=s.diff(U,r,2)+(n-1)/r*s.diff(U,r)+n*(n-2)*U*(lam/(lam**2+r**2))**2
assert s.simplify(res)==0
print('Bubble PDE checked symbolically for arbitrary n.')

# Derive conformal covariance using independent formal 2-jets.
w,v,Dw,Dv,gwgv,gw2,R=s.symbols('w v Dw Dv gwgv gw2 R',positive=True)
b=2/(n-2); c=(n-2)/(4*(n-1))
# ghat=w^(4/(n-2))*g, phi=b log w.
Dphi=b*(Dw/w-gw2/w**2)
gphi2=b*b*gw2/w**2
Rhat_scaled=R-2*(n-1)*Dphi-(n-1)*(n-2)*gphi2
Lhat_scaled=Dv+(n-2)*b*gwgv/w-c*Rhat_scaled*v
Lwv_over_w=Dv+2*gwgv/w+v*Dw/w-c*R*v
assert s.simplify(Lhat_scaled-Lwv_over_w)==0
print('Conformal Laplacian covariance checked symbolically for arbitrary n.')

# Boundary transformation, with H the trace and dim(boundary)=n-1.
H,nuw,nuv=s.symbols('H nuw nuv')
Hhat_scaled=H+(n-1)*b*nuw/w
Bhat_scaled=nuv+2*c*Hhat_scaled*v
Bwv_over_w=nuv+v*nuw/w+2*c*H*v
assert s.simplify(Bhat_scaled-Bwv_over_w)==0
print('Boundary-operator covariance checked symbolically for arbitrary n.')

# Exact flat graph geometry, no asymptotic expansion.
for d in range(2,7):
    z=s.symbols('z0:'+str(d)); t=s.Symbol('t')
    # generic quadratic graph with mixed terms
    f=sum((j+1)*z[j]**2 for j in range(d))+sum(z[j]*z[j+1] for j in range(d-1))
    F=s.Matrix(list(z)+[t+f]); x=list(z)+[t]
    J=F.jacobian(x); g=s.simplify(J.T*J)
    assert s.simplify(g.det()-1)==0
    grad=s.Matrix([s.diff(f,y) for y in z]); W2=1+(grad.T*grad)[0]
    N=s.Matrix(list(grad)+[-1]) # unnormalized outward normal
    assert s.simplify((N.T*N)[0]-W2)==0
    assert all(s.expand((N.T*J[:,j])[0])==0 for j in range(d))
print('Exact graph metric determinant and outward normal checked in dimensions 3,...,7.')

# Check the full outward mean-curvature formula by differentiating the normal.
for d in range(2,6):
    z=s.symbols('z0:'+str(d)); eps=s.Symbol('eps')
    f=sum((j+1)*z[j]**2 for j in range(d))+s.prod(z[:2])
    grad=[s.diff(f,x) for x in z]
    q=sum(v*v for v in grad)
    K=sum(grad[i]*grad[j]*s.diff(f,z[i],z[j]) for i in range(d) for j in range(d))
    lap=sum(s.diff(f,x,2) for x in z)
    Hdirect=sum(s.diff(eps*grad[i]/s.sqrt(1+eps**2*q),z[i]) for i in range(d))
    Hformula=eps*(lap-eps**2*K/(1+eps**2*q))/s.sqrt(1+eps**2*q)
    assert s.simplify(Hdirect-Hformula)==0
print('Full nonlinear graph mean-curvature formula checked in dimensions 3,...,6.')

# First-order boundary residual on graph eps*f; Euler gives z.Df=k*f.
eps,f,k,lapf,q,K,r,lam=s.symbols('eps f k lapf q K r lam')
ratio=(n-2)*eps/s.sqrt(1+eps**2*q)*(-(k-1)*f/(lam**2+r**2+eps**2*f**2)+(lapf-eps**2*K/(1+eps**2*q))/(2*(n-1)))
first=s.diff(ratio,eps).subs(eps,0)
expected=(n-2)*(lapf/(2*(n-1))-(k-1)*f/(lam**2+r**2))
assert s.simplify(first-expected)==0
print('First shape derivative of B(U)/U checked symbolically for arbitrary n and homogeneous degree k.')

out=Path('workspace/agent4_conformal_checks.py')
out.parent.mkdir(exist_ok=True)
# Save this independently reusable checker.
out.write_text(Path(__file__).read_text())
print('Saved',out)

proof = r'''# Hemisphere shape-Hessian lemma

This proposition is independent of the asserted compactness/noncompactness theorem. It proves no gluing or compactness statement.

Let (S^n,g0) be the unit round sphere, n>=3, and let Ω0={x_{n+1}>=0}. Write Σ=S^{n-1}, ν0=−e_{n+1}, q=2n/(n−2), c=(n−2)/(4(n−1)), and α=2c. For f in C^∞(Σ), let Ωε be the domain whose boundary is the normal graph exp_y(ε f(y)ν0). All mean curvatures use the outward normal and trace convention. Use smooth collar diffeomorphisms to identify Ωε with Ω0.

Define

Iε(u)= (1/2) ∫_{Ωε} (|∇u|²+c n(n−1)u²) + c∫_{∂Ωε} Hε u² − ((n−2)²/8)∫_{Ωε} u^q.

The Euler equation is

−Δu+c n(n−1)u−[n(n−2)/4]u^{(n+2)/(n−2)}=0,
∂νu+α Hε u=0.

Thus u=1 solves the ε=0 equation. This is the unit-sphere normalization of the question: multiply u by 2^{−(n−2)/2} to recover the coefficient n(n−2).

## Proposition

There is a smooth branch of projected critical points uε=1+εv+O(ε²), using the L²-orthogonal complement of K=span{x1,...,xn} on Ω0. Its first derivative is the unique solution orthogonal to K of

(Δ+n)v=0 in Ω0,
∂νv=α(ΔΣ+n−1)f on Σ.

The reduced energy at the identity bubble has expansion

Iε(uε)=I0(1)−(ε²/2)∫Σ v∂νv+O(ε³).

If f=Σ_{l>=0} f_l is its orthogonal spherical-harmonic decomposition on Σ, then

Iε(uε)=I0(1)−(α² ε²/2) Σ_{l>=2} [(l−1)²(l+n−1)² / D_l] ||f_l||²_{L²(Σ)}+O(ε³),

where

D_l=(l−1) Γ(l/2)Γ((l+n+1)/2)/[Γ((l+1)/2)Γ((l+n)/2)]>0.

The quadratic shape energy is strictly negative unless f consists only of degrees 0 and 1. It is an elliptic quadratic form of order 3, equivalent to the squared H^{3/2} norm modulo those degrees.

## Proof

1. **First shape variation.** The standard hypersurface variation formulas at the totally geodesic equator are dVol/dε=∫Σ f and H'=−(ΔΣ+n−1)f. The bulk integrand Iε(1) equals (n−2)/4. Consequently

(d/dε)Iε(1)|0=[(n−2)/4]∫f−c(n−1)∫f=0.

Reflection in the equator exchanges Ωε with the complement of Ω_{−ε}, preserving volume and reversing outward H. Hence Iε(1)+I_{−ε}(1)=2I0(1), exactly. In particular its second derivative vanishes.

2. **Fredholm complement.** The Hessian at (0,1) is

H(v,w)=∫Ω0(∇v·∇w−n v w).

Its Neumann kernel is exactly K: Neumann reflection identifies these functions with even degree-1 spherical harmonics on S^n. The self-adjoint Neumann map is an isomorphism after restricting to K-perpendicular and projecting the residual onto the corresponding compatible codomain. The implicit function theorem in C^{2,β} (0<β<1), with the nonlinear map into C^{0,β}×C^{1,β}, therefore gives the smooth projected branch. For small ε it is positive since it tends to 1 uniformly. This branch need not be an actual critical point: its unprojected residual may have K components of order ε².

The shape derivative of the residual, applied to a test function w, is

−α∫Σ(ΔΣ+n−1)f·w.

The forcing is orthogonal to K because (ΔΣ+n−1)xj=0 on Σ. Thus the derivative v obeys the stated homogeneous interior equation and inhomogeneous Neumann condition, with no first-order K residual.

3. **Energy reduction.** Expanding the functional along the projected branch yields

Iε(uε)=I0(1)+ε²{(1/2)H(v,v)−α∫Σ(ΔΣ+n−1)f·v}+O(ε³).

The linearized equation and integration by parts give H(v,v)=∫Σv∂νv=α∫Σ(ΔΣ+n−1)f·v. Substitution proves the claimed negative-half formula. No unknown second derivative of uε enters, because I0'(1)=0.

4. **Spectrum.** Write latitude θ∈[0,π/2], with θ=0 at the equator. A mode y(θ)Y_l, where −ΔΣY_l=l(l+n−2)Y_l, satisfies

y''−(n−1)tanθ y'−l(l+n−2)sec²θ y+n y=0.

Set z=sinθ. The solution regular at the pole is proportional to

(1−z²)^{l/2} 2F1(l−1,l+n;l+n/2;(1−z)/2).

For l>=2, Gauss's second summation formula at 1/2, applied also to the derivative, gives −y'(0)/y(0)=D_l. Since outward normal is −∂θ, this is precisely the Dirichlet-to-Neumann multiplier. The boundary source is

α[(n−1)−l(l+n−2)]f_l=−α(l−1)(l+n−1)f_l.

Hence v_l|Σ=−α(l−1)(l+n−1)f_l/D_l, which proves the series formula.

For l=0, the solution is −α(n−1)f_0 x_{n+1}; its boundary trace vanishes, so its quadratic energy vanishes. For l=1, the source is zero and the complement condition selects v=0. These are exactly the infinitesimal conformal motions of round boundaries, not additional hidden negative modes.

Finally Γ-ratio asymptotics imply D_l~l, and the summand weight is asymptotic to l³. Smooth f makes the series converge in every n>=3.

## Computational verification

agent2_hemisphere_DtN_checks.py independently checks the hypergeometric radial ODE and the gamma multiplier against high-precision values. agent4_conformal_checks.py checks the PDE normalization and conformal/graph conventions. Both were run successfully. No numerical check is used to replace the analytic Fredholm or shape-variation proof above.
'''
Path('workspace/agent4_shape_hessian.md').write_text(proof)
print('Saved workspace/agent4_shape_hessian.md')
