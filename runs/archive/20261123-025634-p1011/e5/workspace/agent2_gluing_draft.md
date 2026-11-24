# Polynomial-graph gluing: proof plan and exact estimates

**Status: conditional analytic draft, NOT a proved theorem.** The finite-dimensional quadratic energy used here has a certified strict local minimum already in dimension19, whereas the requested answer says compactness through20. Therefore some hypothesis/estimate in this draft or the claimed classification must be clarified before using it as a proof.

Set D=deg h, n>2D, h a polynomial on R^(n-1). Let U=(1+|y|^2)^(-(n-2)/2), and let H be homogeneous D^{1,2}(R^n_+). The Hessian at U is
 Q(v,w)=int grad v.grad w-n(n+2)int U^(4/(n-2))vw.
Its kernel consists of tangential translations and dilation; on the Dirichlet-inner-product complement its inverse has norm (n+4)/4 (agent3 proved by sphere spectrum).

For a graph x_n=t h(x'), first Robin residual is
 A_h=(n-2)U[(h-x'.Dh)/(1+|x'|^2)+Delta h/(2(n-1))].
This lies in the dual trace space when n>2D. For all bubbles U_(xi,eps), first direct shape energy is zero by integration by parts, and second direct shape energy is zero by reflection. Hence candidate reduced coefficient is F_h=-1/2<A_h,Q^(-1)A_h>, with projection away from the bubble kernel. The first shape identity implies A_h annihilates this kernel.

## Geometric assembly
Start with a round hemisphere, conformally flattening the metric and boundary on a coordinate neighborhood of p. The resulting metric remains LCF and positive Yamabe. Pick disjoint boundary balls B_(2rho_i)(q_i), with q_i->p. Take mu_i>0 flat in rho_i, meaning mu_i*rho_i^(-k)->0 for every integer k, and lambda_i << rho_i. Replace the flat boundary in this ball by
 h_i(x')=mu_i lambda_i^D h((x'-q_i)/lambda_i) chi((x'-q_i)/rho_i).
For every k, ||D^k h_i|| <= C_k mu_i rho_i^(D-k), since lambda_i<=rho_i. The boundary is therefore smooth at the accumulation point; its entire jet there is zero. Choose the mu_i sufficiently small so the domain remains C^2-close to the hemisphere, hence its first conformal Robin eigenvalue stays positive. A nonzero tracefree Hessian at a bump rules out conformal equivalence to a hemisphere.

## Rescaled parameters
Define t_i=mu_i lambda_i^(D-1), R_i=rho_i/lambda_i, and cutoff h_R=h chi(./R).
Then rescaled boundary is y_n=t_i h_R(y'), with
 sup t_i|Dh_R| <= C mu_i rho_i^(D-1)=:s_i ->0.
Choose lambda_i so
 eta_i=(lambda_i/rho_i)^((n-2)/2)=o(t_i),
which is equivalent to lambda_i^((n-2D)/2)rho_i^(-(n-2)/2)=o(mu_i), possible when n>2D.
The weighted integral controlling geometry is
 int_(R^n_+) (1+|y|)^(2D-2)|grad U|^2 dy < infinity,
whose radial tail is r^(2D-n-1). This is precisely the condition n>2D.

## Estimates that must be established rigorously
Uniformly for (xi,eps) in a compact parameter set:
 1. ||J'(W_i)-t_i A_h||_(H^-1) <= o_R(t_i)+O(s_i t_i)+O(eta_i).
 2. J(W_i)=J_hem+o_R(t_i^2)+O(s_i t_i^2)+O(eta_i^2).
 3. The Hessian restricted off the n-dimensional approximate kernel has a uniform inverse. A contradiction proof rescales a normalized bad sequence to the halfspace; kernel orthogonality eliminates its weak limit, while concentration plus positivity of the fixed background operator eliminates the remaining norm.
 4. Solve the projected equation by the contraction/implicit-function theorem: v_i=-t_i Q^-1 A_h+o(t_i) in H^1.
 5. Uniform reduced energy is J_hem+t_i^2 F_h+o(t_i^2).
A strict local minimum of F_h then yields an interior minimum of the reduced energy, hence a full critical point (the usual derivative-versus-kernel Gram matrix is invertible).

The main unproved portion of this draft is the complete detailed coordinate proof of estimates1-3. They look plausible from the weighted bounds, but must not simply be assumed; the model discrepancy makes independent audit essential.

## Positivity and boundary blowup once the reduction works
Use the energy with nonlinearity (u_+)^q. Positive Yamabe type implies any nonzero weak critical point is nonnegative by testing its negative part, then positive by strong maximum principle; smoothness follows from elliptic regularity. The correction is o(1) in H^1, so its boundary critical trace norm is o(1). The bubble has a fixed positive trace mass in a ball of radius C lambda_i. Therefore max_boundary u_i >= c lambda_i^(-(n-2)/2) -> infinity.


## Further functional details (still audit before promoting to theorem)

The graph map T_t(x,z)=(x,z+t h_R(x)) has determinant1 and its inverse-metric difference from Euclidean has L-infinity norm O(s), where s=t R^(D-1). The boundary curvature density satisfies ||H_t dS||_(L^(n-1))<=C s: indeed t|D²h_R|<=Ct(1+r)^(D-2), whose L^(n-1) norm on r<=CR is O(tR^(D-1)). Critical trace Holder therefore bounds its bilinear form by Cs||v||_(D¹)||w||_(D¹). Thus the full graph Jacobi form is an O(s) bounded perturbation of the halfspace form, including the Robin term; no compactified C² metric bound is required.

For the fixed compact background, let W_i be the physical bubble times a cutoff supported in B_(rho_i)(q_i). Let K_i be its rescaled translation/dilation span and P_i its orthogonal complement projection in the positive conformal-energy Hilbert norm. Let T_i be the full linearized operator represented in this Hilbert norm. The projected inverse P_i T_i|_(K_i perpendicular) is uniformly bounded: if not, choose norm1 v_i with projected image0 in the limit. Testing cutoff Jacobi fields shows the missing K_i coefficients tend0. Away from q_i, weak limits solve the positive background homogeneous equation and therefore vanish. After rescaling, the weak limit solves the halfspace Jacobi equation and is kernel-orthogonal, therefore vanishes. The potential integral int W_i^(4/(n-2))v_i² tends0: inside a fixed rescaled ball by Rellich, outside by Holder with the tail L^(n/2) norm of U^(4/(n-2)). Testing T_i v_i against v_i now forces its norm to tend0, contradiction.

For the nonlinear projected equation, use the nonlinearity (u_+)^p, p=(n+2)/(n-2)>1. On H¹ it is C¹ as a map to the Sobolev dual; the nonlinear remainder is bounded by C||w||^min(2,p) (plus the familiar U-dependent quadratic term when p>2). The uniform inverse and residual O(t_i+eta_i) give a unique w_i in K_i perpendicular with norm O(t_i), and C¹ parameter dependence. In the dimensions considered here p<2, so the contraction estimate is particularly simple: its local Lipschitz constant is O(t_i^(p-1)).

Let z_h be the unique kernel-orthogonal halfspace solution Q(z_h,.)=-A_h. Cut it off at radius R_i, transplant it, and subtract its small K_i projection. Density of compactly supported functions in D¹, local coefficient convergence, and the preceding O(s) form bound imply that its projected Jacobi image differs from -A_h by o(1). The uniform inverse therefore gives ||w_i/t_i-z_h(transplanted)||=o(1).

For q=2n/(n-2)>2, the Sobolev energy has second-order Taylor remainder bounded by O(||w||^q) when 2<q<3 (all dimensions >=7 here). Therefore
 J(W_i+w_i)=J(W_i)+J'(W_i)w_i+1/2 J''(W_i)[w_i,w_i]+o(t_i²)
 =J_hem-1/2 t_i²<A_h,Q^-1 A_h>+o(t_i²).
Uniformity over a compact bubble-parameter set follows because all polynomial-growth bounds are uniform there, and the limiting inverses depend continuously on the parameters.

If the model F has a strict interior local minimum, choose a compact parameter ball on whose boundary F exceeds its minimum by a fixed gap. Uniform reduced C0 convergence yields an interior reduced-energy minimum. The full gradient at the projected critical point lies in K_i. Differentiating orthogonality of w_i to K_i shows its pairings with parameter derivatives equal the nondegenerate bubble tangent Gram matrix plus O(t_i). Hence vanishing reduced derivatives forces all K_i coefficients of the full gradient to vanish.

Every argument in this subsection is standard functional analysis once all coordinate estimates are written, but the unresolved n19 consequence means the assembled proof should receive an independent line-by-line audit before being cited as an established gluing theorem.
