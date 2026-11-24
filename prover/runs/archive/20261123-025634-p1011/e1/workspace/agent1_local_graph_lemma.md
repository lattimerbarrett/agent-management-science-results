# Direct local graph perturbation lemma (n=19)

This is the analytic construction whose implication conflicts with the problem's stipulated answer. It is stated here in full to permit adversarial review.

Let a=17/2, p=21/17, k=323, b=17/36. Suppose (M,g) has positive first Robin eigenvalue and admits a boundary chart in which g is Euclidean and M={x_n>0}. Put
 E_g(v,w)=int_M (grad v.grad w+c_n Rvw)+b int_boundary Hvw,
 J_g(v)=E_g(v,v)/2-k int_M(v_+)^(p+1)/(p+1).
Positive first eigenvalue and the trace interpolation inequality make E_g equivalent to the H1 norm.

Choose even polynomial F of degrees<=8. For eps>0 let rho=1/log(1/eps), mu=eps^8, R=rho/eps, and perturb boundary in this chart to
 f_eps(x')=eps^9 F(x'/eps) chi(x'/rho),
chi=1 on B1 and supported B2. The metric is unchanged ambient Euclidean metric in the chart, and unchanged elsewhere. Pulling to M by a graph diffeomorphism gives smooth metrics converging C-infinity to g, since each kth derivative of f_eps is bounded by C_k sum_{d<=8} eps^(9-d)rho^(d-k), which tends zero. The first eigenvalue stays positive. After this identification all energy forms, Riesz operators and projections below are those of the perturbed metric, denoted E_{g_eps}, A_{g_eps}; any shorter E_g notation in the reduction means this varying form, whose norms are uniformly equivalent to the fixed H1 norm.

Let sigma=(xi,lambda) range in a fixed small compact set, lambda>0. Let W_eps,sigma be the standard target-normalized bubble centered at eps xi on the old boundary plane, of scale eps lambda, with a fixed smooth cutoff supported in the flat chart and identically one throughout the graph support. In its own rescaled coordinates the graph is mu lambda^-1 F(xi+lambda y) with expanding cutoff. Every bound below is uniform in sigma. Write F_sigma=lambda^-1 F(xi+lambda y).

## Residual
On graph t=mu G(y), put Q=1+|y|^2+mu^2G^2, S=1+mu^2|grad G|^2. For U=(1+|y|^2+t^2)^(-a), direct differentiation gives
 B U=17mu(G-y.grad G)Q^(-19/2)S^(-1/2)
 +b mu[Delta G S^(-1/2)-mu^2 G_iG_jG_ij S^(-3/2)]Q^(-17/2).
For G=F_sigma with cutoff at O(R), |D^jG|<=C(1+r)^(8-j), j<=2. Thus delta=Cmu R7 ->0 and
 ||BU-mu g_G||_{L^(36/19)}<=Cdelta^2mu,
 g_G=17(G-y.grad G)(1+r2)^(-19/2)+b Delta G(1+r2)^(-17/2).
Indeed the pointwise remainder is bounded by Cdelta²mu(1+r)^(-11); this function is in L^(36/19)(R18). Also ||g_G-g_Fsigma||<=C R^(-3/2). Domain surface measure differs by1+O(delta²). The vertical graph map has derivative I+O(delta), and H has L18 norm O(delta), so trace/form constants are uniform. The fixed cutoff's interior residual has H^-1 norm O(eps^a)=O(eps^8.5)=o(mu). Consequently J'(W)/mu converges strongly, after transplantation, to the halfspace functional r_Fsigma(psi)=int g_Fsigma psi. The same estimates after one parameter derivative hold; in particular ||J'(W)||+||partial_sigma J'(W)||=O(mu).

## Projected inverse and correction
Let Z_j=partial_sigma_j W, K=span Z_j, and project using E_g onto Kperp. The operator
 T_eps=Pperp[I-pk A_g^-1(W^(p-1) .)]|Kperp
has inverse bounded independently of eps. A complete concentration proof is in agent3_formal_inverse_reduction.md / agent3_uniform_inverse.md. Its ingredients are: approximate kernel residual O(mu), positivity of A_g, removability of a boundary point for H1, halfspace bubble Jacobi kernel exactly span of parameter derivatives (unit-hemisphere first Neumann spherical harmonics), Rellich on bounded rescaled sets, and U^(p-1) in L^(19/2) with vanishing tails. Fredholm index0 gives surjectivity.

For1<p<2, pointwise |(W+phi)_+^p-W^p-pW^(p-1)phi|<=C|phi|^p, with the corresponding Lipschitz estimate on a small H1 ball. Sobolev embedding and the uniform inverse therefore give a unique projected correction phi_sigma in Kperp with ||phi||<=Cmu and Pperp J'(W+phi)=0. The map is C1 in sigma because the positive-part Nemytskii map is C1 H1->H^-1. Differentiating the fixed point gives only partial_sigma phi=o(1) (a sufficient bound is O(mu^(p-1))+O(mu)); no O(mu) derivative claim is needed. Strong residual profile convergence, transplanted finite-energy Jacobi solutions and the uniform inverse give phi/mu ->v_Fsigma, with L v_Fsigma=-r_Fsigma on the kernel complement.

## Energy
For an ambient bubble define D=|grad U|²/2-k U^(p+1)/(p+1). The domain integral is even in the normal variable, while H U² dS is odd when G is replaced by-G. First graph variation cancels exactly after integration by parts:
 D(y,0)=(b/2)Delta_y(U(y,0)^2).
The volume Taylor remainder is bounded by Cmu³ int |G|³(1+r)^(-38), since |partial_tt D|<=C(1+r)^(-38) for |t|<=delta(1+r). The boundary remainders are bounded by
 Cmu³ int [|grad G|²|D²G|(1+r)^(-34)+|Delta G|G²(1+r)^(-36)].
All three radial integrands, after r17dr, grow at worst r3. Hence the full fixed-bubble shape remainder is O(mu³(1+R4))=O(eps20 rho4)=o(mu²). The old-background/cutoff bubble energy differs from the halfspace constant by O(eps17)=o(mu²).

Taylor expansion in phi has error O(||phi||^(p+1))=o(mu²). The projected equation and phi orthogonality give
 J(W+phi)=J(W)+(1/2)J'(W)[phi]+o(mu²).
Strong profile convergence therefore identifies the leading quadratic with stationary elimination of the bubble's linear shape correction. Conformal transfer to the unit hemisphere gives
 J_red(sigma)=J_bubble-Cmu² Q(F_sigma)+o(mu²), C>0,
uniformly on compact parameter sets. The positive C only records normalization of the target bubble (radius1/2 rather than unit sphere). The exact spectral formula is
 Q(eta)=sum_{L>=2} [(L-1)(L+18)]²/mu_L * ||eta_L||²,
 mu_L=2Gamma(L/2)Gamma((L+20)/2)/[Gamma((L-1)/2)Gamma((L+19)/2)],
 eta(y)=2F_sigma(y)/(1+|y|²).
L0 contribution is zero (Neumann solution is normal coordinate, boundary trace0), L1 forcing vanishes. The source is orthogonal to the bubble kernel, since the boundary operator -(Delta+18) annihilates L1. The spectral derivation and exact maximum certificate are in agent4's notes/scripts.

## Actual solution and robustness
If Q has a strict full local maximum at sigma0, choose a small closed parameter ball with Q(sigma0)>sup_boundary Q+gamma. Uniform C0 energy expansion gives J_red(boundary)>J_red(sigma0)+Cgamma mu²/2 for small eps. A minimizer is interior and critical. The residual lies in K, and its pairing with parameter derivatives has matrix E(Z_i,Z_j)+o(1), since partial phi=o1. The bubble Gram matrix is nonsingular, so all residual coefficients vanish. Thus u=W+phi solves the full modified equation.

Test with u_-: coercivity forces u_-=0. Critical-exponent weak elliptic regularity (Brezis-Kato truncation followed by bootstrap), strong maximum principle and Robin Hopf lemma give u smooth and strictly positive on the closure. Its boundary L^(36/17) mass on an O(eps) cap is bounded below: bubble mass is uniform and phi's trace tends0. Cap area is O(eps18), so max_boundary u>=c eps^-8.5.

For each fixed sufficiently small eps the inverse, contraction, C1 natural-constraint matrix, energy boundary gap and trace lower bound persist under all sufficiently small later smooth metric/domain changes. This gives an OPEN high-peak solution packet, without requiring nondegeneracy of a chosen PDE solution.

## Certified polynomial
F(y)=(y1²-|y|²/18)[1-461|y|²/1000+7|y|4/125-693|y|6/500000].
The exact certificate agent4_exact_full_hessian.py proves Q has a strict full maximum at xi0, lambda in[.951902323,.951902324]. Translation coordinates used there differ by the positive factor lambda, which changes Hessian by positive congruence. Thus the local hypothesis is met.

Together with the robust disjoint-patch diagonal lemma, this appears to prove19 is in D, contradicting the requested conclusion. Every local estimate above has been independently audited by agents2/3/4. The team has requested a source for the alleged empty-set theorem and received none.
