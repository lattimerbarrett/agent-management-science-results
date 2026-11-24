# Single-patch reduction: candidate counterexample lemma, audit required

Let n=19, and let (M,g) be positive Yamabe type, LCF, with boundary equal to a plane in a flat conformal chart about p. Let F be an even polynomial of degrees 2,4,6,8. Write mu=eps^8 and deform the physical boundary to
f_eps(x')=eps^9 F(x'/eps) chi(x'/rho), rho=1/log(1/eps).
The chart and base geometry are fixed during this lemma. Let W_eps,xi,lambda be a cutoff half-space bubble centered at p+eps xi, of scale eps lambda, with cutoff identically one on support f_eps. The target-normalized standard bubble compactifies to a radius-1/2 hemisphere. For spectral shape calculations one uses the unit hemisphere after a fixed constant conformal rescaling; this changes the action quadratic only by a positive constant.

Action, in the convention Delta u+n(n-2)u^p=0, is
J_g(u)=1/2 E_g(u,u)-n(n-2)/(p+1) int (u_+)^(p+1),
E_g(u,u)=int(|grad u|^2+c_n R u^2)+2c_n int H u^2.
The positive first Robin eigenvalue makes E_g coercive.

1. Graph C^k perturbation tends zero for every fixed k: highest-degree contribution is O(eps rho^(8-k)). Thus g_eps ->g C-infinity after pulling back by chart diffeomorphisms. Scaled boundary graph is mu F_R, R=rho/eps, and delta=mu R^7=eps rho^7 ->0.

2. Exact local Robin residual of ambient radial bubble U=(1+|y|^2)^(-(n-2)/2) on graph y_n=mu F_R is mu g_F+o(mu) in the critical trace dual L^(36/19); g_F=(n-2)(F-y.grad F)(1+r^2)^(-n/2)+b Delta F(1+r^2)^(-(n-2)/2), b=(n-2)/(2(n-1)). The first-order profile behaves O(r^-11), and is L^(36/19). The cutoff profile error is O(R^-3/2). Exact nonlinear graph error is <=C delta^2 mu (1+r)^-11. Fixed bubble cutoff residual is O(eps^8.5)=o(mu). Estimates uniform and differentiable once in (xi,lambda) on compact sets.

3. Projected linearized operator has uniform inverse on complement of the n bubble kernel modes. Proof: normalized bad sequence has zero global weak limit by positivity; rescaled limit is Jacobi field and orthogonality kills all n modes (hemisphere first Neumann harmonics); weighted-potential integral then tends zero by local compactness and U^(p-1) L^(n/2) tail, contradicting norm1. Graph perturb coefficient and curvature-form norms tend zero. Projection coefficients vanish by pairing with approximate kernel derivatives, whose residuals tend zero.

4. Positive-part nonlinearity gives remainder norm O(||phi||^p) since 1<p<2. Contraction produces unique projected correction phi=O(mu). Strong residual convergence and uniform inverse give phi/mu ->v_F, where v_F is the linear shape correction in the bubble limit. Energy Taylor remainder is O(mu^(p+1))=o(mu^2). Dependence is C1 in parameters, with derivative phi=O(mu).

5. Fixed-bubble shape action has zero first derivative and no second derivative. Indeed its volume integrand is even in y_n and H U^2 is odd under graph sign reversal. First derivative cancels pointwise after integration by parts because
D=1/2|grad' U|^2 - n(n-2)/(p+1) U^(p+1)=(b/2) Delta'(U^2).
Cubic remainder is O(mu^3(1+R^4))=O(eps^20 rho^4)=o(mu^2). Base cutoff energy error O(eps^17)=o(mu^2).

6. Hence reduced energy is
J_red(xi,lambda)=J_bubble-C mu^2 Q_F(xi,lambda)+o(mu^2), C>0,
uniformly on a compact parameter neighborhood. Q is the positive shape quadratic on the translated/dilated graph polynomial lambda^(-1) F(xi+lambda y). The translation certificate instead parameterizes F_lambda(y+zeta), so xi=lambda*zeta; strict Hessian signs are unchanged. Its spectral formula is
Q(eta)=sum_{L>=2} ((L-1)(L+n-1))^2 / mu_L * ||eta_L||^2,
mu_L=2 Gamma(L/2)Gamma((L+n+1)/2)/(Gamma((L-1)/2)Gamma((L+n)/2)).
No contribution from L0 or L1. Bubble-normalization factors only change overall C>0.

7. If Q_F has a strict full local maximum, J_red has an interior minimum for sufficiently small eps. At a critical point, projected residual lies in n-dimensional kernel span; parameter derivative matrix tends to the nonsingular bubble Gram matrix, so all coefficients vanish and u=W+phi solves full equation. Testing modified equation with negative part and coercivity implies u>=0; maximum principle gives u>0. Boundary trace mass on an eps-cap gives max_boundary u >=c eps^-8.5.

8. The strict reduced-energy boundary gap and projected inverse persist for all sufficiently small smooth later metric/domain changes (for each fixed eps). Thus the high-peak solution packet is robust, without needing exact nondegeneracy. Combined with disjoint-patch diagonal construction this would yield one fixed metric with boundary blowup.

Exact algebra certificate already verified by agents3/4: F(x)=(x1^2-|x|^2/18)*(1-461|x|^2/1000+7|x|^4/125-693|x|^6/500000) has a strict full maximum of Q at xi0, lambda in [.951902323,.951902324]. Full Hessian signs certified in workspace/agent4_exact_full_hessian.py.

STATUS: These steps appear to prove a counterexample, contradicting requested conclusion. They require line-by-line auditing, especially step6 identification of shape profile normalization and the uniform reduced-energy C0 expansion. Do not label theorem counterexample until audited.
