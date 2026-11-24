# Local insertion on a fixed positive background: proof draft for review

**Purpose.** This would bridge exact reduced algebra to the conditional Baire construction. It is not asserted here to settle the problem: the n19 model discrepancy remains, so this argument needs independent scrutiny, especially the uniform local energy comparison in step 5.

## Statement
Let n>16. Let (M,g) be a fixed compact positive-Yamabe manifold whose boundary contains a conformally Euclidean half-ball chart. Suppose the polynomial graph profile h=H_2 p(|z|^2), of degree at most eight, has a strict local minimum of minus its response quadratic form in bubble scale/translation parameters. Then arbitrarily small C^K boundary-graph perturbations supported in that chart admit positive solutions with arbitrarily large boundary maximum, realized by a persistent strict reduced minimum. Here K is arbitrary but finite. The ambient metric is unchanged and remains locally conformally flat when it was so initially.

## Parameters and scales
Fix chart radius rho. Insert

 b_{mu,lambda}(z)=mu lambda^8 chi(|z|/rho) h(z/lambda).

The bounds ||b||C^K <= C_K mu rho^(8-K) hold for lambda<=rho, so mu is first chosen to meet the C^K perturbation budget. Set t=mu lambda^7, R=rho/lambda. Then tR^7=mu rho^7 is small. Choose lambda subsequently so

 eta=lambda^((n-2)/2)=o(t), equivalently lambda^((n-16)/2)=o(mu).

Constants depending on the fixed background and chart cause no restriction because lambda is free after mu. For proofs of little-o statements, take a joint sequence mu->0 and lambda->0 with eta/t->0.

## 1. Ansatz and model source
Write g=phi^(4/(n-2))delta in the half-ball chart, with baseline boundary flat. Use W=phi^(-1)chi_0 U_{lambda,xi}, transported to the perturbed domain, where chi_0 is a fixed cutoff. The cutoff source has H^{-1} norm O(eta), and its action is O(eta^2). These follow by direct radial integration of U~lambda^((n-2)/2)r^(2-n) and its gradient in the cutoff annulus.

After rescaling by lambda and conformally mapping the half-space to a hemisphere, the graph source divided by t converges in boundary L^{2(n-1)/n} to beta*a0*D f, with f=2h/(1+|z|^2). This is the graph-curvature estimate in agent2_finite_domain_shape_reduction.md, since f_R has growth r6, gradient r7, Hessian r8. Integrability and convergence hold for n>16. The nonlinear source is therefore O(t)+O(eta).

## 2. Uniform projected inverse
Let Z_a be the cutoff derivatives of the bubble in its n conformal parameters, normalized in the positive conformal Robin Hilbert norm. Project away their span. The projected Hessian is uniformly invertible for small mu,lambda. For contradiction, take unit vectors v_j in its complement with residual tending to zero. Testing against Z_a first shows the finite kernel multipliers tend to zero, because the Gram matrix converges to the hemisphere kernel Gram and the Z_a have Hessian residual tending to zero.

Away from the bubble, v_j converges weakly to a solution of the background homogeneous conformal Robin problem; positive Yamabe type forces that limit to be zero. Rescaling at the bubble gives a finite-energy hemisphere Jacobi solution orthogonal to its entire Neumann kernel; it too is zero. Compactness of the weighted potential embedding implies

 integral U_lambda^(4/(n-2)) v_j^2 ->0.

For this last compactness, use ordinary Rellich on bounded rescaled annuli; the far tail is bounded by C R^(-2)||grad v_j||_2^2 via Hardy because the potential is O(r^-4). Testing the Hessian equation on v_j then forces its positive Hilbert norm to vanish, contradiction. The small moving-graph perturbation is controlled in form norm by mu rho^7 and is absorbed.

## 3. Nonlinear correction
For n>16, p=(n+2)/(n-2) lies between one and two. The pointwise remainder is O(|w|^p), so the Sobolev-to-dual estimate and the projected inverse give a contraction on an O(t+eta) ball. Hence w=O(t). The linear model response z, conformally pulled back and cut off in the chart, satisfies the projected correction equation with residual o(t). The inverse estimate consequently gives w/t -> z strongly in energy. This uses eta/t->0 and dominated convergence of the model profile in W^{2,2(n-1)/n}.

## 4. Model action expansion
For the unnormalized positive-part action, the constant hemisphere value a0 has zero first and second shape derivatives. The graph mean-curvature and volume formulas give a direct remainder bounded by

 C t^3[1+R^max(23-n,0)+log R]=o(t^2).

The correction contributes -(beta*a0)^2 t^2 Q(f)/2+o(t^2), and the nonlinear remainder is O(t^q)=o(t^2). These estimates are uniform over compact scale/translation parameter sets. This establishes the finite-hemisphere expansion already detailed in the finite-domain note.

## 5. Localization back to the arbitrary background
The intended comparison estimate is

 I_M(W+w)=I_bubble-C_n t^2 Q(f_theta)+o(t^2)+O(eta*t+eta^2),

uniformly on a fixed small parameter neighborhood, C_n>0. Cutoffs cost eta in energy norm, and the profile response has finite energy. Its tail can be truncated with energy tending to zero; the uniform projected inverse identifies the global correction with that localized response up to o(t). Thus no background term survives at order t^2. This needs a careful written localization argument; it is the most important remaining review point in this draft.

## 6. Reduced minimum and positivity
Since eta=o(t), a strict minimum of -Q persists under the uniform energy expansion. The parameter-to-kernel pairing matrix is invertible, so an interior reduced critical point is an actual critical point of I. The positive-part formulation and positivity of the conformal Robin form imply its negative part vanishes. Strong maximum principle and the boundary point lemma give strict positivity. Local rescaled elliptic estimates show its boundary height is asymptotic to a positive multiple of lambda^(-(n-2)/2), so exceeds any prescribed value. The strict reduced energy barrier persists under sufficiently small C^K perturbations, giving the open property required by the Baire construction.

## Limitation and consistency warning
The statement and every scale exponent above apply already at n19. Since the current exact profile algebra also has a strict full minimum there, this draft cannot be used to claim n<=19 compactness. Either a substantive defect lies in the proposed local insertion argument/model, or the source theorem/hypotheses need clarification. The unresolved issue must not be concealed by calling this a proof of the advertised complete result.


## Step 5 localization addendum: two-cutoff argument

Write A_j for the global projected Hessian, E_j=I'_j(W_j) for the residual restricted to K_j-perpendicular, and t_j=mu_j lambda_j^7. Assume the inverse bound from step 2. The scaled local boundary source g_j converges to g in L^{2(n-1)/n}, including its tail; the cutoff source has norm O(eta_j)=o(t_j).

Let z solve the limiting projected equation A_0 z=-g. For a fixed large A choose z_A=chi_A z in Euclidean bubble coordinates and project it off the limiting kernel. Let Z_{j,A} be the conformal chart transplantation to M_j at scale lambda_j, projected off K_j. For fixed A its support eventually lies wholly inside the conformal half-ball chart. Ordinary smooth coefficient convergence there gives convergence of every local quadratic form and residual pairing. The portion outside that fixed compact set is bounded in dual norm by the source tail and energy tail. More precisely,

 limsup_j ||A_j Z_{j,A}+E_j/t_j||_{H^{-1}}
 <= C(||z-z_A||_{D^{1,2}}+||g-chi_A g||_{L^{2(n-1)/n}}).

The terms introduced by kernel projection obey the same bound because z is orthogonal to the limiting kernel. This estimate follows by subtracting the model weak equation before applying Cauchy-Schwarz and the trace inequality; hence its constant is independent of A after a standard fixed-width radial cutoff choice.

The model tails tend to zero. For a degree-eight source, g=O(r^{8-n}), z=O(r^{9-n}), and the squared gradient tail is O(A^{16-n}); the source dual-norm tail has the same scale A^{(16-n)/2}. Alternatively the finite-energy and L^p hypotheses alone suffice, without pointwise decay.

The correction equation is A_j w_j=-E_j+N_j(w_j), with ||N_j(w_j)||_{H^{-1}}<=C||w_j||^{p}=O(t_j^p). Apply the uniform inverse to w_j/t_j-Z_{j,A}, take limsup in j, then A->infinity. The right-hand side tends to zero. Thus

 lim_{A->infinity}limsup_j ||w_j/t_j-Z_{j,A}||_{H^1}=0.

The Hessian forms have uniformly bounded norm. Fixed-A form convergence and the preceding approximation consequently imply

 A_j(w_j,w_j)/t_j^2 -> A_0(z,z)=(beta*a0)^2 Q(f).

Finally, Taylor expansion of the action at W_j and testing the projected correction equation on w_j give respectively

 I_j(W_j+w_j)=I_j(W_j)+E_j(w_j)+A_j(w_j,w_j)/2+O(t_j^q),
 E_j(w_j)+A_j(w_j,w_j)=O(t_j^q).

Since q>2, subtraction yields the claimed second-order response energy. The direct W_j action is the finite-domain shape calculation plus cutoff terms O(eta_j^2+eta_j*t_j), by the same critical Sobolev and energy-norm estimates. Since eta_j=o(t_j), these vanish after division by t_j^2. Compact parameter sets retain the same dominating tails, so the result is uniform in reduced parameters.

This closes the formal localization mechanism subject to the already-listed source convergence and global inverse estimates. It supplies no dimension20-specific obstruction: every exponent in this argument only requires n>16. The full theorem's low-dimensional claim remains unresolved and inconsistent with the currently certified n19 reduced minimum unless some other substantive defect is found.
