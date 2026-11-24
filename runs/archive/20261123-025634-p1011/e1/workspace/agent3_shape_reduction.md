# Uniform shape reduction near a round hemisphere (derived analytic lemma)

Let D be the unit round hemisphere in S^n, Sigma its equator, m=n-1,
a=4(n-1)/(n-2), q=2n/(n-2), R=n(n-1). For a sufficiently small
C^2 normal graph h over Sigma, write D_h for the deformed domain and
J_h(w)=int_Dh [a|grad w|^2/2+Rw^2/2-R(w_+)^q/q]+int_boundary H_h w^2.
Use a fixed collar pullback to compare Sobolev spaces. Put
mu=||h||_(H^{3/2}), delta=||h||_(C^2).
Let K be the n-dimensional first-Neumann-eigenfunction kernel of
A_0=a(-Delta-n). On K-perp, A_0:H^1->H^{-1} has a bounded inverse.
The constant mode is negative but invertible; no volume constraint is needed.

For mu,delta sufficiently small, projected contraction gives a unique
v_h in K-perp, ||v_h||H1<=C mu, satisfying projected J'_h(1+v_h)=0.
If r_1(phi)=2 int_Sigma H'_0[h] phi, then
v_h=-A_0^{-1}r_1+O_H1(delta mu+mu^{q-1}).
Consequently
J_h(1+v_h)=J_0(1)-1/2 <r_1,A_0^{-1}r_1>
                 +O(delta mu^2+mu^q).
All constants are uniform for small C^2 graph domains.

Proof details:
1. w=1 solves the ambient interior Euler equation on every D_h. Thus
   J'_h(1) is only the boundary residual 2H_h; there is no bulk forcing.
2. In round Fermi coordinates dt^2+cos^2(t) gamma_Sigma, graph mean
   curvature linearization is +/- (Delta_Sigma+m)h. Tame multiplication
   and the graph formula give
   ||H_h-H'_0h||H^{-1/2} <= C delta ||h||H^{3/2}.
   The boundary measure change is absorbed in the same estimate.
3. The pulled-back quadratic forms A_h satisfy
   ||A_h-A_0||_(H1->H-1)<=C delta. This follows directly from C^1
   closeness of collar diffeomorphisms, bounded round scalar curvature,
   and ||H_h||L^m<=C delta with the critical trace Sobolev inequality.
4. For n>=7 (in particular n=19), the nonlinearity N has
   ||N(v)||H-1<=C||v||H1^{q-1}, and its local Lipschitz bound is
   C(||v||+||z||)^{q-2}||v-z||. A_0 inverse and contraction prove the
   asserted v estimate; analogous smooth estimates hold in low n.
5. J_h(1)-J_0(1)=O(delta ||h||H1^2). Its first variation vanishes:
   R/n=n-1=m and volume variation cancels mean-curvature variation.
   Its second variation vanishes by equatorial reflection: both the
   volume difference and integral mean curvature are odd in h.
   The graph action formula followed by integration by parts bounds
   the remaining third-order terms as stated.
6. Taylor expansion in v has remainder O(||v||H1^q). Substitute v_h,
   use steps2-5, and complete the square with A_0.

Positivity at a full critical point follows by using the positive-part
nonlinearity: test the full equation with the negative part. The first
Robin conformal eigenvalue is positive for small graph perturbations,
so the negative part vanishes; strong maximum principle gives positivity.

For the n19 degree8 polynomial cutoff, h_e=mu eta_R+nonlinear error,
mu=e^8, R=rho/e. The stereographic jet eta_R has H^{3/2} norm uniformly
bounded since 2*8<19. Its C^2 norm is O(R^8), so delta=O(rho^8)->0.
Thus delta mu^2+mu^q=o(mu^2), uniformly on compact scale/center parameter
sets, and Q_R converges with parameter derivatives to Q_infinity.

LIMITATION: This lemma handles globally C^2-small graph domains in the
bubble's spherical compactification. In a fixed domain with previously
inserted distant patches, that compactification need not be globally
C^2-small. Extending the lemma to those distant patches, with residual
O(e^{(n-2)/2}) and uniform inverse, remains a separate analytic step.
No original-problem counterexample or desired compactness theorem is
claimed here.
