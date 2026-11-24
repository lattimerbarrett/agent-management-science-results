# Extreme dual roots converge after exponentially small strict-mode deflation

## Setting
Retain a finite active spectrum with positive weights, fixed s, monic primal OPs f_k and squared norms N_k increasing to L>0. Let H_k be the monic dual OP defined by H_k(lambda_i)=d_i p_(k,i) f_k(lambda_i)/N_k. Suppose a<b are adjacent ACTUAL spectral nodes, f_k(a)f_(k+1)(a)/N_(k+1)->1 and likewise at b. After deflating dual roots near strictly contracting spectral nodes, let h_k be the remaining monic dual polynomial. Assume its smallest root alpha_k lies in (a,b), all other roots stay a fixed positive distance from [a,b], and all roots of H_(k+1)-H_k move o(1). More generally another root may move in a disjoint closed interval, as for the cubic full-six-node rectangle; uniform separation suffices. All deflated roots approach their fixed spectral nodes exponentially, p_strict=O(rho^k), some rho<1.

Then alpha_k converges. The analogous largest-root assertion follows by reflecting the spectrum.

## 1. Exponentially distorted Rayleigh inequality
Write H_k=D_k h_k. Exact Christoffel orthogonality makes h_k the OP for the positive measure qhat_k=q_k D_k^2. Its two-step update is
 qhat_(k+2) = const*qhat_k (h_k/h_(k+1))^2 E_k,
 E_k=(D_(k+2)/D_(k+1))^2.
Away from the deflated nodes, E_k=1+O(rho^k); on those nodes E_k is uniformly bounded, and
 qhat_k(lambda) h_k(lambda)^2 = q_k(lambda) H_k(lambda)^2
 =p_k(lambda) f_k(lambda)^2/N_k^2.
Thus the deflated-node contribution to the Rayleigh numerator/denominator for the trial h_(k+1)/(x-alpha_(k+1)) is O(rho^k), since those nodes are separated from [a,b]. The total unperturbed denominator is at least
 [max_i |lambda_i-alpha_(k+1)|]^-2 * sum_i p_(k,i)f_k(lambda_i)^2/N_k^2
 = [max distance]^-2 /N_k >=c>0.
On other nodes the multiplicative error is O(rho^k), even if an endpoint term is large. Rayleigh quotients are averages of bounded spectral nodes, so these estimates give a UNIFORM O(rho^k) quotient error, including when alpha approaches a or b.

Put S_k(u)=sum qhat_(k,i) h_k(lambda_i)^2/(lambda_i-u). Orthogonality gives S_k(alpha_k)=0, and S_k'(u)>0 in the entire node-free gap. The Rayleigh bound therefore gives
 alpha_(k+2) <= alpha_(k+1)+S_k(alpha_(k+1))/S_k'(alpha_(k+1))+C*rho^k.   (1)
This is the same exact root-turning bound as without deflation, with the uniform perturbation just proved.

## 2. Relative endpoint motion is small
The exact dual interpolation identity gives
 H_(k+1)(a)/H_k(a)=f_k(a)f_(k+1)(a)/N_(k+1)->1.
Factoring H_k(a)=(a-alpha_k)*[all other factors], and using their separation from a and o(1) motion (including the exponentially moving deflated roots), yields
 (alpha_(k+1)-a)/(alpha_k-a)->1.
Likewise (b-alpha_(k+1))/(b-alpha_k)->1. Hence, for delta_k=alpha_(k+1)-alpha_k,
 epsilon_k=max_i |delta_k|/|lambda_i-alpha_(k+1)| ->0.                 (2)
This conclusion remains true arbitrarily near an endpoint; no absolute-distance lower bound is assumed.

## 3. Positive coefficient tends to one
For delta_k nonzero define
 A_k=S_k(alpha_(k+1))/[delta_k*S_k'(alpha_(k+1))]
 =integral_0^1 S_k'(alpha_k+t*delta_k)/S_k'(alpha_(k+1)) dt.
All summands in S_k' are positive. By (2), termwise denominator comparison gives
 (1+epsilon_k)^-2 <= A_k <= (1-epsilon_k)^-2.
Thus A_k>0 and A_k->1. If delta_k=0 take A_k=1. Equation (1) becomes
 delta_(k+1) <= A_k*delta_k+C*rho^k.                                (3)

## 4. One-sided exponential-cone lemma
If a bounded scalar sequence alpha satisfies (3) with A_k->1, then it converges. Choose rho<a_*<1 and k0 so A_k>=a_* thereafter. Choose D>C/(a_*-rho). If delta_k<=-D*rho^k at any k>=k0, induction gives
 delta_(k+1)<=-(a_*D-C)rho^k<=-D*rho^(k+1),
so all later increments are negative and alpha converges monotonically. If no such k exists, the negative variation is bounded by sum D*rho^k<infinity. Since alpha is bounded, its positive variation is also finite, and alpha converges. This uses only a ONE-SIDED recurrence; no inverse-map bound or equality is required.

## Why the setting holds in the cubic strata
At an equality-limit positive node, f(a)g(a)=L, so the endpoint product condition holds. Dual coefficients are continuous in primal weights via interpolation and N_k>=N_0, and every equality-limit point is a two-cycle with the SAME dual polynomial on the two parities. Consequently H_(k+1)-H_k->0. The relevant slow roots lie in fixed disjoint node-free gaps: for six positive nodes they are (lambda2,lambda3) and (lambda4,lambda5); for the hard five-node edge the moving root is in its one gap and all outsider roots are separated. No active spectral node can lie strictly inside such a gap, since there f*g>L, making a vanishing active weight impossible. Selecting the global slow extreme, and deflating all strict roots on that side, therefore gives exactly the setting above.
