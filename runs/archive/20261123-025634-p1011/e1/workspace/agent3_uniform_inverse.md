# Uniform bubble-complement inverse: explicit contradiction proof

Let A_g=-L_g with Robin B_g=0 and positive first eigenvalue. Use its
coercive quadratic form E_g as the Hilbert H^1 norm. Let W_e be a
cutoff halfspace standard bubble in a flat boundary chart. Assume chart
boundary after rescaling converges C^2_loc to the plane (true for the
polynomial patch mu=e^8). Let K_e span cutoffs of the n bubble Jacobi
fields (scale and n-1 tangent translations), and P_e the E-orthogonal
projection on K_e-perp. Define
T_e v=v-p*n(n-2) A_g^{-1}(W_e^{p-1}v), p=(n+2)/(n-2).
Then P_e T_e restricted to K_e-perp has a uniform bounded inverse.

Proof. Otherwise choose ||v_i||E=1, v_i perpendicular K_i, with
P_i T_i v_i->0. The Gram matrix of Jacobi cutoffs has positive definite
limit. Also ||T_i Z_i,j||E->0, checked by rescaling and bubble tails.
By self-adjointness, testing T_i v_i against Z_i,j shows all residual
K_i coefficients vanish, so T_i v_i->0 in H^1.

Away from the concentration point W_i->0, and weak H^1 limit v solves
A_g v=0,B_g v=0; positivity gives v=0. Rescale about the bubble. The
rescaled v_i is bounded in homogeneous H^1(halfspace); every weak limit
phi satisfies
-Delta phi=n(n+2)U^{4/(n-2)}phi, d_n phi=0.
E-orthogonality passes to orthogonality against all n Jacobi fields.

Kernel classification: even-reflect across the plane, divide phi by U,
and conformally map to the round sphere of radius1/2. The equation is
(Delta+4n)w=0. Finite energy implies H^1 removability at the omitted
point. First spherical harmonics span the kernel; even reflection
selects exactly n coordinates, the scale+tangent-translation fields.
Thus phi=0.

For fixed R the rescaled v_i converges strongly in L^2(B_R^+). The
potential tail is bounded uniformly by
(int_{|y|>R} U^{2n/(n-2)})^{2/n} ||vtilde_i||_{2n/(n-2)}^2 ->0 as R->infty.
Hence int W_i^{p-1}v_i^2->0. But testing T_i v_i->0 against v_i gives
1-p*n(n-2)int W_i^{p-1}v_i^2->0, contradiction.

For varying global domains pulled back by C^2-small normal graphs the
same proof applies with uniformly coercive energy forms and uniformly
bounded Sobolev constants; weak limits use the limiting smooth metric.
One does NOT need uniform high derivatives of the moving local patch.

Nonlinear contraction for n19: p=21/17<2. Using positive-part power,
||N(phi)-N(psi)||_{H^-1}<=C(||phi||H1+||psi||H1)^{p-1}||phi-psi||H1.
For residual O(mu), uniform inverse yields unique projected correction
||phi||H1=O(mu), with energy nonlinear remainder O(mu^{p+1})=o(mu^2).
If the rescaled residual/mu converges strongly to r_F and the cutoff
linear solution v_F has finite energy, the same uniform inverse proves
phi/mu converges strongly after rescaling to the projected halfspace
solution v_F. Indeed transplant/cut off v_F, verify its residual by
finite-radius convergence plus small energy tails, and apply the inverse.
This identifies the correction energy as -1/2<r_F,A_0^{-1}r_F>.

This note supplies a local LS ingredient. It is not itself a completed
construction or a proof of the requested empty-set conclusion.
