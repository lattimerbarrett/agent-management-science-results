# Uniform projected inverse: complete conditional analytic lemma

This lemma is standard analytic infrastructure, NOT a sharp-dimensional
compactness theorem or an existence construction.

Let (M,g) be smooth compact, n>=3, with boundary and positive first conformal
Laplacian Robin eigenvalue. Put a=(n-2)/2, kappa=n(n-2), p=(n+2)/(n-2).
Use the coercive Hilbert form
 E(v,w)=int_M(<grad v,grad w>+c_n R vw)+2c_n int_boundary H vw.
Coercivity follows from lambda_1>0, the trace inequality, and interpolation.

Let q_j tend to a boundary point, delta_j tend to zero, and use smooth uniformly
controlled boundary flattening charts. Let W_j be the ordinary halfspace
bubble U_delta,xi=(delta/(delta^2+|x'-xi|^2+t^2))^a, cut off at a fixed chart
radius. Smooth chart Jacobians and coefficients converge after rescaling to
the Euclidean halfspace. Let Z_{j,0}=cutoff*delta*d_delta U and
Z_{j,b}=cutoff*delta*d_xi_b U (1<=b<=n-1). Set K_j=span{Z_j,b}.
Define the bounded self-adjoint A_j by
 E(A_j v,w)=E(v,w)-n(n+2) int_M W_j^(4/(n-2)) v w.
Then for j sufficiently large the compression P_j^perp A_j on K_j^perp is
invertible and its inverse operator norm is bounded independently of j.
All conclusions remain uniform for parameters in compact rescaled sets.

## Proof

1. Sobolev and Holder give a uniform operator bound for A_j, because
   ||W_j^(4/(n-2))||_(n/2) is uniformly bounded. The Gram matrix E(Z_j,b,Z_j,c)
   converges to the positive definite Gram matrix of the n Euclidean Jacobi
   fields z_0,z_1,...,z_(n-1). Cutoff errors and smooth coefficient errors
   tend to zero in H^{-1}; hence ||A_j Z_j,b||_H tends to zero. This last
   assertion can be proved by first restricting rescaled coordinates to a
   fixed halfball, where coefficients converge smoothly and the Jacobi
   equation is exact, and then making Jacobi D^{1,2} tails small.

2. Suppose the uniform lower bound failed. Choose v_j in K_j^perp with
   ||v_j||_H=1 and ||P_j^perp A_j v_j||_H tending to zero. Write
   A_j v_j=sum_b c_j,b Z_j,b+o_H(1). Test with Z_j,c, use self-adjointness
   and step1: the left side is E(v_j,A_j Z_j,c)=o(1). Nondegeneracy of the
   Gram matrix gives c_j,b ->0. Thus A_j v_j ->0 in H.

3. On bubble scale, vtilde_j(y)=delta_j^a v_j(q_j+delta_j y) is bounded in
   D^{1,2}_loc on the halfspace, and in L^{2n/(n-2)} globally on expanding
   charts. A subsequence converges weakly, and strongly in L2 on compact
   sets, to psi satisfying
     -Delta psi-n(n+2)U^(4/(n-2))psi=0,  partial_n psi=0.
   Finite energy follows by lower semicontinuity. Orthogonality to Z_j,b
   passes to int grad psi.grad z_b=0, by approximation and Jacobi tails.

4. The only finite-energy halfspace solutions of this linearized equation
   are span{z_0,...,z_(n-1)}. Indeed conjugate by
   phi=2^((n-2)/2)U and compactify stereographically to the unit hemisphere.
   The equation becomes (-Delta_Sn-n)w=0 with Neumann data. Neumann
   eigenvalue n consists exactly of restrictions of the n coordinate
   functions even under equatorial reflection. The possible missing pole
   is removable in H1 (a point has zero H1 capacity in n>=3). Dirichlet
   orthogonality to z_b is a positive constant times L2 orthogonality to
   those eigenfunctions. Consequently psi=0.

5. Therefore int_M W_j^(4/(n-2))v_j^2 ->0. On a fixed rescaled halfball this
   follows from strong local L2 convergence. On its complement use Holder:
     integral <= ||W_j||_(2*,outside radius R delta)^(4/(n-2)) ||v_j||_(2*)^2.
   The first factor tends uniformly to the corresponding U tail, which
   tends to zero as R tends to infinity. Outside the fixed chart W_j=0.

6. Testing A_j v_j=o_H(1) with v_j now gives
   1=n(n+2) int_M W_j^(4/(n-2))v_j^2+o(1) ->0, a contradiction.

For each fixed j, A_j=I-compact on H, since its smooth bounded potential
factors through the compact embedding H1(M)->L2(M). Its compression is
self-adjoint Fredholm of index zero on K_j^perp. The lower bound therefore
implies bijectivity and the claimed inverse bound.

## Scope of the cutoff assertion

This statement uses ordinary fixed-radius cutoff bubbles in fixed smooth
background charts. It does not assert that an arbitrary large polynomial
moving-domain perturbation has the uniform residual or reduced-energy
expansion needed for the dimension-18 construction. Those require separate
weighted estimates. It establishes only the projected-inverse lemma.

Density convention: smooth compactly supported halfspace approximants mean
`C_c^infinity(overline{R_+^n})`, smooth up to the boundary with unrestricted
trace; no Dirichlet-zero boundary condition is imposed.
