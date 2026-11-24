# Complete analytic proof appendix

See PROOF_INDEX.md for the exact upper-bound parameters and computer certificate.



---

# Appendix section 1 — agent4_tv_lemma.md

# Monic-polynomial finite-variation lemma (all restart lengths)

After combining repeated eigenspaces, let the distinct active eigenvalues be
`lambda_1,...,lambda_m`, with positive initial squared spectral weights. Write
`p_{k,i}=||P_i r_k||^2/||r_k||^2`. The monic orthogonal polynomial `f_k` of degree
`s` satisfies `sum_i p_{k,i} f_k(lambda_i) lambda_i^j=0`, `0<=j<s`, and let
`N_k=sum_i p_{k,i} f_k(lambda_i)^2`. The normalized spectral-weight iteration is
`p_{k+1,i}=p_{k,i} f_k(lambda_i)^2/N_k`. An exact zero component remains zero.
Nontermination guarantees at least `s+1` support points, hence `N_k>0`.

Let `f=f_k`, `g=f_{k+1}`, `h=f_{k+2}`, `P=f*g`, `N=N_k`, `N'=N_{k+1}`.
Since `g` is monic, orthogonality of `f` gives `E_p[P]=N`.
Moreover `E_p[P^2]=N*N'`. Consequently

    E_p[(P-N)^2]=N*(N'-N),

so `N_k` increases to a finite positive limit `L`.

Put `v(x)=(1,x,...,x^(s-1))^T`, and
`M_2=sum_i p_{k+2,i} v_i v_i^T`. Since both `f` and `g` are orthogonal to
lower-degree polynomials under their corresponding weights,

    E_p[f*v]=0,       E_p[f*P*v]=0.

Thus `E_p[f*P^2*v]=E_p[f*(P-N)^2*v]`. If `c(h-f)` denotes the ascending
coefficient vector of `h-f`, its degree is below `s`, and orthogonality of `h`
at `p_{k+2}` yields the EXACT identity

    M_2 c(h-f) = -E_p[f*(P-N)^2*v]/(N*N').

All monic orthogonal polynomials here have roots in the fixed spectral hull;
their coefficients and spectral values are therefore uniformly bounded.
Also all matrices `M(p_k)` are uniformly positive definite. Indeed, the
minimum-monic norm `N(p)` is continuous on the closed simplex: it is a minimum
over a fixed compact coefficient set, because a minimizing polynomial can
always be chosen with roots in the spectral hull (including rank-deficient
weights). If a subsequence of `M(p_k)` became singular, its limiting measure
would have support at most `s-1`, and hence `N(p_k)->0`, contradicting
`N(p_k)>=N_0>0`. (In fact `N>0` excludes support at most `s`.)

Uniformly bounding the inverse of `M_2` in the exact identity gives

    ||c(f_{k+2}-f_k)|| <= C (N_{k+1}-N_k).

Therefore BOTH polynomial parities have finite total variation, and converge
to monic degree-s polynomials `f_infty,g_infty`. In particular

    ||f_{2j}-f_infty||+||f_{2j+1}-g_infty|| <= C (L-N_{2j}).

At any cluster point, equality in the norm Lyapunov identity forces the
two-block normalized residual to return to itself. Every eigenvalue in the
union of cluster supports consequently satisfies

    f_infty(lambda_i)*g_infty(lambda_i)=L.

There are at most `2s` such distinct eigenvalues. The limiting weights lie in
the one fixed affine polytope

    p>=0, sum p=1, sum p_i f_infty(lambda_i)lambda_i^j=0 (j<s).

This polynomial finite-variation lemma is independently checked over exact
rational arithmetic by `workspace/agent4_polynomial_tv_check.py`.

## Consequence when the two limiting polynomials coincide

Suppose `f_infty=g_infty=q`. If `q(lambda_i)^2>L`, the corresponding two-block
weight multiplier tends to a number greater than one, so this eigenvalue
cannot belong to the initial support and simultaneously have weight tending
to zero. Eigenvalues with `q(lambda_i)^2=L` form the limiting root set. Every
other initially active eigenvalue has `q(lambda_i)^2<L`, and its weight decays
exponentially. Orthogonality gives the exact identity

    L-N_k = E_{p_k}[(q-f_k)^2] + E_{p_k}[L-q^2].

The second term is exponentially small because it is supported off the
limiting root set. The first is at most `C||f_k-q||^2`, hence, by the tail bound,

    0 <= L-N_k <= C'(L-N_k)^2 + O(rho^k),  rho<1.

For large `k`, absorb the square term to obtain exponential norm-deficit
convergence. The strict Lyapunov inequality bounds the square of the
normalized residual's two-step displacement by a constant times
`N_{k+1}-N_k`; hence these displacements are summable, and the even residual
sequence converges. This holds for every `s`.


---

# Appendix section 2 — agent3_negative_weight_bound.md

# Quadratic bound on negative-neutral outsider weights
Fix the even-block indexing. Write t_k=L-N_{2k}>0 and p_k=p_{2k,mu} for an active spectral node mu satisfying f(mu)g(mu)=-L. The all-s polynomial-TV tail estimate implies
p_{k+1}/p_k = (f_{2k}(mu)f_{2k+1}(mu))^2/(N_{2k}N_{2k+1}) = 1+O(t_k).
Hence p_k-p_{k+1} <= C t_k p_k. The strict monic Lyapunov identity gives t_k-t_{k+1} >= c p_k for all large k: the mu coordinate of F^2 y-y equals (-2+o(1))y_mu, so the squared step controls p_k, and the norm gain controls the squared step uniformly since N>=N0>0.
Thus, telescoping (p_k->0),
p_k = sum_{j>=k}(p_j-p_{j+1}) <= (C/c) sum_{j>=k} t_j(t_j-t_{j+1}) <= (C/c)t_k^2.
The summands on the left need not be positive; finite partial sums suffice and the right converges. This proves p_{2k,mu}=O((L-N_{2k})^2) without any regular-variation assumption.

Furthermore an active negative-neutral outsider forces sum_k t_k=infinity: otherwise sum|log(p_{k+1}/p_k)|<infinity, contradicting p_k->0. Since t_k->0, log p_k=o(k), and the bound p_k<=C t_k^2 yields log t_k=o(k) from below. Hence all strictly contracting outsider weights O(rho^k) are o(t_k^2). On the limiting positive root set, f_{2k}f_{2k+1}-N_{2k}=O(t_k), so the variance identity now yields N_{2k+1}-N_{2k}=O(t_k^2), and the analogous odd estimate yields t_k-t_{k+1}=O(t_k^2).

Consequently any nontrivial negative-neutral asymptotic regime admits the compact normalization epsilon=t_k: polynomial errors divided by epsilon are uniformly bounded by TV, and negative-neutral weights divided by epsilon^2 are uniformly bounded by this lemma. This rules out using unbounded normal-form trajectories as evidence of actual fixed-target asymptotics.


---

# Appendix section 3 — agent3_root_turning_lemma.md

# Exact extreme-root turning lemma
Let q be a positive measure on finitely many distinct real nodes, H its monic degree-t orthogonal polynomial, and alpha its smallest zero. Let g be any monic degree-t polynomial with real smallest root a in the same node-free spectral gap as alpha; assume g has no zeros on the nodes. Set q_new=q*(H/g)^2, and let l be its monic degree-t orthogonal polynomial. If a<=alpha, then minroot(l)<=a. The analogous maximal-root statement reverses all inequalities.

Proof: The least Gaussian node is the least Rayleigh quotient of multiplication by x on polynomials of degree<=t-1 (standard symmetric moment compression). Choose test v=g/(x-a). Its Rayleigh quotient under q_new is R(a)=sum q*x*H^2/(x-a)^2 / sum q*H^2/(x-a)^2. Put S(z)=sum q*H^2/(x-z). Orthogonality gives S(alpha)=sum q*H*(H/(x-alpha))=0, while S'(z)=sum q*H^2/(x-z)^2>0 on the spectral gap. Hence a<=alpha gives S(a)<=0 and R(a)-a=S(a)/S'(a)<=0. Therefore minroot(l)<=R(a)<=a. Reflect x to obtain the maximal-root statement.

Application: In an exact dual-polynomial recurrence q_{k+2}=const*q_k*(H_k/H_{k+1})^2, if the smallest H-root stays eventually in one fixed spectral gap then its increments can change from positive to negative at most once. It therefore converges. The largest root likewise converges. For degree t<=2 all coefficients converge. This is an exact discrete argument, not an asymptotic ODE argument.


---

# Appendix section 4 — agent1_robust_extreme_root.md

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


---

# Appendix section 5 — agent2_s2_convergence_proof.md

# Complete convergence argument for restart s=2

Use the following already proved general lemmas: the monic orthogonal residual polynomials f_j of degree s have norms N_j increasing to L>0; the trajectory closure has uniformly positive definite degree-(s-1) moment Gram matrices; each polynomial parity has finite coefficient total variation and the tail estimate ||f_{2k}-f||+||f_{2k+1}-g|| <= C(L-N_{2k}); and ||y_{j+2}-y_j|| -> 0. The normalized monic map differs from the actual residual map by (-1)^s, so even sequences agree.

After the last coordinate annihilation, use distinct active eigenvalues, all positive spectral weights p_{j,i}. Let K_j=f_j f_{j+1}. The exact identities are
p_{j+2,i}=p_{j,i} K_j(lambda_i)^2/(N_j N_{j+1}),
SUM p_{j,i}(K_j(lambda_i)-N_j)^2 = N_j(N_{j+1}-N_j).
Consequently all omega points of p_even are supported on S={i:f(lambda_i)g(lambda_i)=L}, and |S|<=4. Any active outsider with |f_i g_i|>L is impossible (its two-step weight ratio eventually exceeds 1); strict |f_i g_i|<L gives exponential decay. The only other outsiders have f_i g_i=-L.

Let T be the union of supports of all omega points. The omega set is connected because successive even increments tend to zero. All its points satisfy SUM p=1, SUM p f=SUM p lambda f=0. If |T|<=3 these equations determine a unique p: every omega point has >=3 support nodes (since N>=N0); at a positive 3-node feasible point a dependence a+b f+c lambda f=0 has a=0 by averaging, and then b=c=0 since f is nonzero at every node. Thus convergence follows. If |T|=4, the same rank argument gives an affine line of feasible weights. A non-singleton connected omega set is an interval on this line; because T is the full support union, a relative interior point of that interval has all four weights positive.

## Global exclusion of negative outsiders, with no interior trapping assumption
Write the four nodes in T as lambda_1,...,lambda_4 and P(x)=PROD(x-lambda_i). Then fg=P+L. Fix an active negative outsider mu, so P(mu)=-2L. Let ell_i be the degree-3 Lagrange coefficients at mu. Since K_j is monic quartic,
K_j(mu)=-2L+SUM ell_i K_j(lambda_i), SUM ell_i=1.
Set t_j=L-N_j, R_j=sqrt(N_j N_{j+1}), e_{j,i}=K_j(lambda_i)-R_j. The polynomial TV tail implies |e_{j,i}|<=C t_j, and t_j/2<=L-R_j<=t_j. Define
Psi_j=log p_{j,mu}+SUM ell_i log p_{j,i}.
For even j, its two-step increment is exactly
2 log(2L-R_j-E_j)+2 SUM ell_i log(R_j+e_{j,i})-4 log R_j,
where E_j=SUM ell_i e_{j,i}. Taylor expansion on a fixed neighborhood of L gives
Psi_{j+2}-Psi_j = 2 log((2L-R_j)/R_j)+O(t_j^2) >= c t_j-C t_j^2 >=0
for all sufficiently large j. The linear E_j terms are O(t_j^2), since their coefficient is 2(1/R_j-1/(2L-R_j))=O(t_j). If t_j=0, exact strictness already excludes an active negative outsider. Along the omega subsequence with four positive base weights, Psi_j tends to minus infinity because p_{j,mu}->0, contradicting eventual monotonicity. Thus there are no negative outsiders. All outsiders decay exponentially.

## Reduction to an exponentially perturbed four-node map
Condition the weights on the four nodes T; call them q_j. They obey q_{j+1}=F(q_j)+O(rho^j), where F is the exact four-node restart-2 map and 0<rho<1. All required moment Gram matrices remain uniformly positive definite, even at limiting faces, since each omega support has >=3 nodes. Therefore F, its monic polynomial phi(q), and all functions below are uniformly smooth near the relevant compact closure. Also phi(q_j)-f_j=O(rho^j).

Put d_i=P'(lambda_i), nu(q)=SUM q_i phi(lambda_i)^2. Four-node orthogonality gives the exact dual formula
q_i=nu(q)(lambda_i-theta(q))/(d_i phi(q)(lambda_i)).
Equivalently the interpolant d_i q_i phi_i/nu is the monic linear polynomial x-theta(q). This provides a smooth formula for theta(q), including boundary limits. Because f_i g_i=L>0, phi(q_j) has the same eventual sign for both parities at each of the four nodes; hence theta(q_j) lies in one fixed eigenvalue gap for all sufficiently large j.

For the exact map define delta(q)=theta(Fq)-theta(q). The reciprocal-mean formula yields
 delta(Fq)=a(q) delta(q),
 a(q)=SUM Q_i r_i / SUM Q_i r_i^2,
 Q_i proportional 1/(d_i^2 q_i), r_i=(lambda_i-theta(q))/(lambda_i-theta(Fq)).
This follows by expanding (lambda-theta(q))^2/(lambda-theta(Fq)).
Moreover the polynomial identity
 r_i=nu(Fq)/(phi(q)(lambda_i) phi(Fq)(lambda_i))
shows r_i->1 uniformly at the four nodes, EVEN if theta approaches a node. Thus a(q_j)>0 eventually and a(q_j)->1.

Uniform smoothness of delta(q), together with exponentially small perturbations, now gives for theta_j=theta(q_j), delta_j=theta_{j+1}-theta_j,
 delta_{j+1}=a_j delta_j+O(rho^j), a_j->1, a_j>0.
A scalar lemma completes the proof. Pick eta with rho<eta<1 and eventually a_j>=eta. For D large, either delta_j remains in [-D rho^j,D rho^j] forever (so it is summable), or it leaves this band and its sign can never change again (because each exterior cone is forward invariant). Thus the bounded sequence theta_j converges.

Finally q_{2k,i}=nu(q_{2k})(lambda_i-theta_{2k})/[d_i phi(q_{2k})(lambda_i)] converges, and outsiders vanish. Even residual-coordinate signs stabilize on T because K_j(lambda_i)->L>0; outsider residual components vanish. Hence y_even converges in Euclidean norm.


---

# Appendix section 6 — agent2_s3_logmoment.md

# Exact s=3, five-base-node logarithmic moment
Let P(x)=prod_{i=1}^5(x-lambda_i), fg-L=P Q with Q=x-c, and let mu!=nu satisfy fg(mu)=fg(nu)=-L.
Define
 a=Q(mu)/(mu-nu), b=-Q(nu)/(mu-nu),
 c_i=2L/[P'(lambda_i)(lambda_i-mu)(lambda_i-nu)].
Then a+b=sum_i c_i=1. For every monic sextic K,
 sum_i c_i K(lambda_i)-a K(mu)-b K(nu)=2L.
Indeed these are 2L times the seven-node barycentric weights: for mu, P(mu)=-2L/Q(mu), and similarly nu. The leading coefficient interpolation formula proves the identity.

For any exact restarted residual orbit with limiting even/odd cubics f,g, L=N_infty>0 and these five positive-level and two negative-level nodes active, put
 Psi_k=sum_i c_i log p_{k,i}+a log p_{k,mu}+b log p_{k,nu}.
Write K_k=f_k f_{k+1} and R_k=sqrt(N_k N_{k+1}), t_k=L-N_k. Polynomial total variation gives K_k-fg=O(t_k). Exact two-block residual update and Taylor expansion imply
 Psi_{k+2}-Psi_k=4 log(L/R_k)+O(t_k^2).
The linear Taylor terms vanish by the sextic interpolation identity, since K_k-fg has degree <=5. Thus unless the orbit is eventually a two-cycle, this difference is >= c t_k eventually. Any active negative-level mode forces sum t_k=infinity, since otherwise its log weight has summable increments and cannot tend to zero. Hence Psi_k -> +infinity along each parity. Crucially, this calculation requires no positive lower bound on the five base weights.

## Continuous blowup identity
Use H=x-theta, physical scalar A=delta N, and h'=-theta'. Let q=gw+f dg-A. The dual differential gives q(lambda_i)=Lh'/(2H(lambda_i)). Thus
 q(x)=P(x) C + (Lh'/2) [1-P(x)/P(theta)]/(x-theta)
for a scalar C. At a negative mode z,
 ell_z=2(w(z)/f(z)+dg(z)/g(z))-2A/L=-2q(z)/L-4A/L.
The above weighted logarithm, using p_i proportional lambda_i-theta, has derivative
 d/dtau [a log Z_mu+b log Z_nu+Phi(theta)] =2-4A/L,
where
 Phi'(theta)=[Q(theta)+2L/P(theta)]/[(mu-theta)(nu-theta)]
 =R4(theta)/P(theta), R4=(P Q+2L)/[(x-mu)(x-nu)].
Partial fractions give Phi=sum_i c_i log|theta-lambda_i|. In homogeneous time the +2 is absent. Therefore no compact positive recurrent orbit of the logtime ODE with A<0 can exist in this five-base/two-charge stratum.

This does NOT by itself close the s=3 lower bound: boundary charge ratios and theta endpoint excursions still require a no-return estimate.


---

# Appendix section 7 — agent3_s3_complete_convergence.md

# Cubic restart convergence: complete stratum reduction (agent 3)

This note uses the already-proved spectral dynamics, polynomial total
variation, negative-neutral weight bound, and virtual-probe inequality.
It records ALL support strata; it does not assume an interior omega point.

Let f_(2k)->f, f_(2k+1)->g, N_k->L>0. Set T to the UNION of supports of
all omega points. Then T is contained in {fg=L}, so |T|<=6. All coordinates
outside T tend zero. Coordinates with |fg|<L decay exponentially; |fg|>L
cannot remain active. The remaining neutral outsiders satisfy fg=+L or fg=-L. Positive-neutral
outsiders are extra roots of fg-L outside T; they too have vanishing weights
by the definition of T. In the five-node stratum the only possible such
extra is c, explicitly retained below as a possible positive guard.
An annihilated coordinate is discarded once and for all.

The omega set is compact and connected, by asymptotic regularity. At every
omega point p, f is its monic cubic OP, and g is the partner OP. Feasibility
is linear in p (normalization and orthogonality of f). Averaging finitely
many omega points, one positive on each member of T, gives a FEASIBLE measure
positive on ALL T, even when no omega point is positive on all T. Its partner
has the same g since fg=L on T. This is used only to establish structure.

## A. Robust extreme-root turning

For exact dual dynamics, if a_k is the smallest Gauss root, a_(k+1) is in the
same spectral gap, the Rayleigh trial gives

 a_(k+2) <= a_(k+1) + S_k(a_(k+1))/S'_k(a_(k+1)),
 S_k(z)=sum q_(k,i) H_k(lambda_i)^2/(lambda_i-z), S_k(a_k)=0.

Consequently

 delta_(k+1) <= c_k delta_k,  c_k>0,

with c_k=S'_k(xi_k)/S'_k(a_(k+1)) for a point xi between the two roots.
The reflected inequality holds for the largest root.

We need the following uniform late-tail version. Suppose the tracked root
stays in one fixed spectral gap, remains uniformly separated from all other
dual roots, and the ratios H_(k+1)(lambda_i)/H_k(lambda_i) tend 1 on the
positive base nodes at the two gap endpoints. All other root factors vary
o(1) and are bounded away from zero there. Thus the ratios of the distances
from the tracked root to either gap endpoint tend 1. The same is automatic
for all other spectral nodes, whose distances stay bounded below. For any
xi between a_k,a_(k+1), all ratios

 (lambda_i-xi)/(lambda_i-a_(k+1)) -> 1

uniformly in i. Hence c_k->1 independently of possibly unbounded q weights.

If strictly contracting dual roots beyond the tracked extreme have to be
removed, factor them D_k. The remaining polynomial is EXACTLY an OP under
q_k D_k^2, by testing original orthogonality with D_k times a lower polynomial.
The two-step Christoffel update acquires a factor
(D_(k+2)/D_(k+1))^2=1+O(rho^k) away from the removed nodes. At a removed node,
its contribution to the Rayleigh numerator/denominator is O(rho^k), by
q_k H_k^2=p_k f_k^2/N_k^2 and separation of the tracked gap from that node.
The denominator has a uniform positive lower bound relative to the norm.
Thus the same argument yields

 delta_(k+1) <= c_k delta_k+O(rho^k), c_k->1,                       (A1)

or its reflection for the largest root. The detailed positive-measure
perturbation argument is the simpler, non-infinitesimal version of
agent2_strict_left_deflation.md.

A bounded scalar sequence satisfying (A1) converges. Choose rho<eta<1 and
c_k>=eta eventually. For sufficiently large D, delta_k<=-D rho^k implies
 delta_(k+1)<=-D rho^(k+1), so this negative cone is forward invariant. Either
the cone is entered and every subsequent increment is negative, or all late
negative increments are summable. In either case boundedness gives convergence.
The reflected assertion holds for a largest root.

## B. At most four omega-support nodes

A positive-norm cubic requires |T|>=4. If |T|=4, normalization plus cubic
orthogonality uniquely determine p: its entries are proportional to
1/[P_T'(lambda_i) f(lambda_i)], with the positive normalization fixed.
Hence the omega set is a singleton, and the even residual directions converge.

## C. Six omega-support nodes

Write P6=prod_T(x-lambda_i), lambda_1<...<lambda_6. Since fg-L is monic
of degree 6, fg=L+P6. Both f and g have three simple real roots. Their product
has no roots where P6>=0. Since P6 has a unique critical minimum in
each negative lobe, P6+L has at most two roots COUNTING MULTIPLICITY in each
such lobe; all six product roots are real, so there are exactly two in each
lobe (lambda_1,lambda_2), (lambda_3,lambda_4), (lambda_5,lambda_6).
Each OP has at most one zero in any spectral-node gap: two roots in an empty
gap contradict orthogonality against the OP divided by those factors.
Thus EACH of f,g has one zero in EACH of the three negative lobes.
Their signs on T are therefore (-,+,+,-,-,+).

Every feasible critical weight vector has the exact representation

 p_i=L H(lambda_i)/[P6'(lambda_i) f(lambda_i)],
 H(x)=(x-alpha)(x-beta),
 alpha in [lambda_2,lambda_3], beta in [lambda_4,lambda_5].

Conversely every such pair gives a feasible critical vector (normalization
follows by leading-coefficient interpolation of H*g). Thus the critical
polytope is a quadrilateral parametrized by this rectangle, with FOUR faces
alpha=lambda_2, alpha=lambda_3, beta=lambda_4, beta=lambda_5. The two slow
roots are uniformly separated by lambda_4-lambda_3>0.

The eventual actual dual polynomial has one root near each outsider and two
slow roots in these same fixed gaps. This follows from exact dual
interpolation H_k(lambda_i)=d_i p_(k,i) f_k(lambda_i)/N_k and positive
base-node product ratios tending 1. The slow roots are uniformly separated
from every outsider root and from one another.

For a negative-neutral outsider mu, P6(mu)=-2L. Let ell_i(mu) be its degree-5
Lagrange interpolation coefficients on T. The previously-proved monomial

 log p_mu+sum_i ell_i(mu) log p_i

is eventually increasing. At an omega point it tends -infinity if every
vanishing base coordinate has nonnegative ell_i. Hence omega must lie in
at least one face whose ell_i<0. Direct signs give:

 mu in (lambda_1,lambda_2): faces {3,5}, i.e.
       alpha=lambda_3 OR beta=lambda_5;                     (L)
 mu in (lambda_3,lambda_4): faces {2,5}, i.e.
       alpha=lambda_2 OR beta=lambda_5;                     (C)
 mu in (lambda_5,lambda_6): faces {2,4}, i.e.
       alpha=lambda_2 OR beta=lambda_4.                     (R)

These are the only possible mu intervals because P6(mu)<0. Let a category
be present if an active outsider lies in it.

* L and R together restrict omega to two isolated opposite rectangle
  vertices. Connectedness makes omega a singleton.
* L and C restrict omega to the single edge beta=lambda_5.
* C and R restrict omega to the single edge alpha=lambda_2.
* Only L present: beta is the GLOBAL LARGEST noncontracting dual root;
  all negative outsiders lie below alpha. Part A (deflating exponentially
  contracting roots beyond beta) gives convergence of beta. The L-star then
  makes omega either a point, or a subset of beta=lambda_5.
* Only R: similarly alpha converges, giving a point or alpha=lambda_2.
* Only C: alpha and beta are both global noncontracting extremes, and both
  converge by A.
* No negative outsiders: both slow roots converge after strict deflation.

In every non-singleton case omega would be contained in one FACE, so its
support UNION would omit one member of T. This contradicts |T|=6. Therefore
this stratum cannot contain a nonconvergent even subsequence.

## D. Five omega-support nodes

Write P=P5, so fg=L+P(x)(x-c) with a real c. Feasible critical weights have

 p_i=L(lambda_i-theta)/[P'(lambda_i) f(lambda_i)]

for theta in a single closed gap [a,b] of T. A non-singleton connected omega
set contains an interior point of this gap, hence an all-five-positive
omega point.

The cubic Gaussian quadrature of this positive measure has Stieltjes
numerator (x-c)(x-theta): indeed

 sum_i p_i/(z-lambda_i)=(z-theta)g(z)/P(z),
 (z-theta)g/P - (z-theta)(z-c)/f = L(z-theta)/(P f)=O(z^-7).

The first six moments agree, so the positive three-node Gaussian measure
at the f roots has numerator (z-c)(z-theta). Thus its two numerator roots
strictly interlace f; the same holds for g. Consequently c lies strictly
OUTSIDE [a,b]: otherwise take the feasible theta=c, including endpoints
where there are still four positive spectral weights. Its positive cubic
Gaussian measure would have a double numerator root, impossible by strict
interlacing. Reflect the spectrum if necessary, and assume c<a.
Then, for every theta in [a,b], both f and g have root placement

 zeta_1<c<zeta_2<a<=theta<=b<zeta_3.

In particular f(c),g(c)>0 and f,g<0 on [a,b]. Since d_a f(a)<0 from positive
endpoint weights, d_a>0, so a has odd index in T. The first gap is impossible
because the two OP roots below a would be below the smallest spectral node.
Hence necessarily a=lambda_3, b=lambda_4, d_a>0,d_b<0.

If active negative-neutral outsiders occur on opposite sides of c, the
five-node TWO-outsider monomial of agent2_s3_logmoment.md has positive
coefficients on both outsider logarithms. Along an all-five-positive omega
subsequence its value tends -infinity, contradicting eventual increase.
Thus all active negative-neutral outsiders are on the SAME side of c.

If there are no negative outsiders, or all lie below c, theta is the global
largest noncontracting dual root (a possible positive-neutral outsider at
c also lies below it). Part A gives convergence of theta, contradiction.

The only remaining case has all negative-neutral outsiders z>c. The virtual
probe lemma, including strict-left deflation and the degenerate c case,
proves liminf I_k/t_k>=0; see agent3_virtual_root_lemma.md,
agent2_strict_left_deflation.md, agent4_virtual_probe_degenerate.md.
The exact single-negative corrected log-weight argument in
agent3_single_negative_edge_closure.md then forces theta to one endpoint,
again contradiction to a non-singleton omega set.

Thus ALL s=3 nonterminating orbits have convergent even normalized residual
DIRECTIONS. Indeed convergent weights on T and vanishing outsiders give
convergent magnitudes; on T, f_k(lambda_i)f_(k+1)(lambda_i)>0 eventually,
so every even-coordinate sign is eventually fixed. Repeated eigenspaces
were combined at the start, and their original residual directions are
fixed under polynomial multiplication. Euclidean convergence follows.


---

# Appendix section 8 — agent1_s3_canonical_identities.md

# Exact scalar-dual s=3 canonical flight and wall formulas
Let f,g be monic cubics with f g-N=P5(x)(x-c), N>0; the hard dual gap is a<theta<b with c<a, ftheta,gtheta<0. All polynomials below are in ASCENDING coefficient convention only in code; f2 denotes the x^2 coefficient. Let Mtheta,Mptheta be base moment Gram matrices, w degree<=2, dg=-Mp^-1 M w, A=delta N, and btheta w=thetadot.

Define the FIXED linear coefficient map
 ell_w(x)=rem_f[(x-c)g(x)w(x)]=ell0+ell1*x+C*x^2.
Set R(theta)=gtheta/ftheta>0 and
 A=ell1-(f2+theta)C,
 B=ell0-(f1+f2*theta+theta^2)C,
 K=C/sqrt(R(theta)).
The displayed A is exactly the norm derivative (same symbol on purpose).

## Derivation of the fixed coefficient map
The first-order product polynomial q=gw+f*dg-A has degree<=5 and values q(lambda_i)=-N*thetadot/[2(lambda_i-theta)] on the five base nodes. Hence
 q(x)=Ctop*P5(x)-(N*thetadot/2)*[1-P5(x)/P5(theta)]/(x-theta).
At any f-root zeta, use P5(zeta)=-N/(zeta-c) and fg=N+P5(x)(x-c). Multiplying q(zeta)+A=g(zeta)w(zeta) by zeta-c gives
 ell_w(x)=A(x-c)-N*Ctop-N*thetadot/2+C*(f(x)-ftheta)/(x-theta),
 where comparing leading coefficients yields C=N*thetadot*gtheta/[2P5(theta)]. The polynomial identity is exact, not just modulo f, as both sides have degree<=2. Comparing coefficients gives A,B above and
 Ctop=-(B+cA)/N-thetadot/2.
In particular thetadot=2P5(theta)C/[N*gtheta].


## Resource and individual growth identity
Write v=thetadot and define

 I=-(c*A+B)+sqrt(f(theta)*g(theta))*K/(theta-c).

Since f,g<0 on the theta gap and K=C/sqrt(g/f), this equals

 I=N*Ctop-N^2*v/[2*P5(theta)*(theta-c)].

All expressions have continuous endpoint extensions because v is divisible
by P5(theta). For a negative-level node z, P5(z)*(z-c)=-2N, and

 ell_z=2*(w(z)/f(z)+dg(z)/g(z))-2*A/N=-2*q(z)/N-4*A/N.

Substitution of the displayed interpolation formula for q gives exactly

 ell_z=-4*A/N+4*I/[N*(z-c)]
        +v*(f(theta)*g(theta)+N)/[P5(theta)*(theta-c)*(z-theta)].

This is a linear identity in w and therefore needs no invertibility of
the coefficient map w -> (A,B,K). In particular common roots of f,g cause
no problem. All denominator factors used here are nonzero on the base
chart, except the explicitly cancelled endpoint factor P5(theta).


---

# Appendix section 9 — agent3_virtual_root_lemma.md

# Virtual extreme-Gauss-root log-ratio lemma (agent 3)

Let p_k be any nonterminating spectral orbit with s fixed. All retained active
weights are positive. Add a new spectral node zeta not in the spectrum and give
it initial weight epsilon>0, rescaling the original weights to sum 1-epsilon.
For each fixed k, the augmented orbit and its monic polynomials depend smoothly
on epsilon at zero. Let H_k be the original monic dual OP (degree n-s-1).
The augmented monic dual OP (degree n-s) tends to (x-zeta)H_k.
Assume zeta is strictly below every zero of every H_k on a tail. Then the
augmented smallest Gauss root is

    a_k(epsilon)=zeta+epsilon alpha_k+O(epsilon^2), alpha_k != 0.

All alpha_k have the same sign (root cannot cross the added spectral node).
If f_k is the original monic residual OP and N_k its squared norm, exact dual
interpolation gives

    alpha_(k+1)/alpha_k =
      f_k(zeta) f_(k+1)(zeta)/N_(k+1) * H_k(zeta)/H_(k+1)(zeta).       (1)

For the dual measure q_k, the two-step update is
q_(k+2) proportional to q_k (H_k/H_(k+1))^2. Take as Rayleigh trial polynomial
H_(k+1)/(x-a_(k+1)). With S_k(u)=sum q_k H_k(lambda)^2/(lambda-u), the bound is

    a_(k+2) <= a_(k+1)+ S_k(a_(k+1))/S'_k(a_(k+1)).

This is valid regardless of which side of zeta the roots occupy. The added
node's dual mass is C_k/epsilon+O(1), C_k>0. Let h=H_k(zeta), nonzero.
At zeta its OP value is -epsilon alpha_k h+O(epsilon^2). Therefore, writing
J_k for the finite contribution of all original nodes, S_k(a_k)=0 gives
J_k=C_k alpha_k h^2. At a_(k+1), the leading numerator is
C_k alpha_k h^2(1-alpha_k/alpha_(k+1)), while S' has leading term
C_k alpha_k^2 h^2/(epsilon alpha_(k+1)^2). Consequently

    alpha_(k+2) <= alpha_(k+1)^2/alpha_k.                            (2)

If alpha>0, beta_k=alpha_(k+1)/alpha_k is nonincreasing; if alpha<0,
beta_k is nondecreasing. If beta_k tends beta_infty>0, then

    sign(alpha_k) * (log beta_k-log beta_infty) >= 0.                (3)

No long-time uniformity of the epsilon expansion is needed: (2) is obtained
separately for each finite triple k,k+1,k+2.


The next two sections supply the complete general-probe application and strict-root error estimates.


---

# Appendix section 10 — agent4_virtual_probe_degenerate.md

# General-probe virtual-root constraint, including P5(c)=0

This supplements agent3_virtual_root_lemma.md. It avoids dividing by P5(c), so
covers the repeated-positive-level-root case c in the five-node support.

Use N for the limiting monic squared norm, P=P5, Q(x)=x-c,
F(x)=f(x)g(x)=N+P(x)Q(x). We consider even cluster states normalized by
t=N-N_k, with limiting polynomial perturbation w, first norm variation A=-1,
first partner variation dg, and slow-root two-block velocity v.
Write

    R(x)=g(x)w(x)+f(x)dg(x)-A.

Dual interpolation, to first order, gives

    R(x)=C P(x) - (N v/2) * [1-P(x)/P(theta)]/(x-theta).          (1)

In particular H R=-Nv/2 on the base nodes. C is the leading x^5 coefficient.
For theta at an endpoint, read (1) and subsequent formulas by continuous
extension after the cancelling factor is removed. All expressions below are
smooth on a neighborhood of c because c is separated from the allowed
slow-root gap.

Take a fixed probe z<c sufficiently close to c, avoiding every original node.
Choose it below all non-strict limiting dual roots. An active positive outsider
at c has a dual root tending to c and is therefore above z. Strict-left dual
roots are removed as described in agent2's deflation lemma.

Give the probe initial weight eta, and let its added dual root be

    a_k(eta)=z+eta d_k+O(eta^2).

For each fixed k the exact dual interpolation identity gives

 d_k=-P_active(z)*u_k(z)*f_k(z)/(N_k H_k(z)),

where u_k(z)>0 is the linearized probe weight. In the S5 limit,
P_active(z)/H_k(z) tends P(z)/(z-theta), since every outside node factor
cancels its limiting dual-root factor. This remains true if an active positive
outside node is c; first fix z<c and then let k tend to infinity. Therefore

    sign(d_k)=sign(P(z))                                      (2)

on a tail, because f(c),g(c)>0 and theta>c. No value of P(c) is used.

The finite-triple Rayleigh expansion gives d_{k+2}<=d_{k+1}^2/d_k. Hence the
positive ratios r_k=d_{k+1}/d_k decrease if P(z)>0 and increase if P(z)<0.
Their common limit is rho(z)=F(z)/N>0. With exponentially deflated strict-left
nodes the same conclusion has an O(r^k) error, r<1. Consequently

 sign(P(z))*[log r_k-log rho(z)] >= -O(r^k).                    (3)

The exact ratio is

 r_k= f_k(z)f_{k+1}(z)/N_{k+1} * H_k(z)/H_{k+1}(z).            (4)

Fast outside dual roots contribute o(t) to its logarithmic variation: negative
outsiders have p=O(t^2), an active positive c outsider has root displacement
increment O(t p_c)=o(t), and strict outsiders are exponentially small=o(t).
The slow dual factor x-theta contributes -v/[2(theta-z)]. Thus at any even
normalized cluster state,

 [log r_k-log rho(z)]/t ->
       (R(z)+A)/F(z)-A/N-v/[2(theta-z)] =: L(z).               (5)

Here (3) applies along the full orbit before extracting the cluster state, so

    sign(P(z))*L(z)>=0.                                      (6)

Substitute (1) into (5), noting F-N=PQ. Cancellation yields the exact identity

 L(z)/P(z) = 1/F(z) * [ C-A*Q(z)/N
                  +v/(2(z-theta))*(Q(z)+N/P(theta)) ].       (7)

Since P(z) != 0, (6) says **the right-hand side of (7) is nonnegative**.
Now let z increase to c, avoiding the finite set of nodes. The right-hand side
is continuous there even if P(c)=0, and its limit is

    C/N + v/[2(c-theta)P(theta)] = I/N^2,

where the canonical resource is

    I=q_w(c)/(theta-c)
     =N*C+N^2*v/[2(c-theta)P(theta)].                          (8)

Identity (8) follows either by polynomial remainder or by the canonical
(A,B,K) formulas. Thus I>=0 at EVERY deficit-normalized cluster state,
INCLUDING P(c)=0. Equivalently I_actual >= -o(t).

## Why no hidden c-factor changes the sign

If c is an active outside node (not one of the five base nodes), both
P_active(z) and the limiting H_k(z) have a factor z-c; their ratio cancels it,
leaving P5(z)/(z-theta). If c is itself one of the five base nodes, its factor
occurs in P5 and is NOT cancelled. In both cases (2) is exactly sign(P5(z)).
For P5(c)=0, use (7) BEFORE taking z to c, never the vanishing expression
P5(c)*I. This is the essential order of limits.


---

# Appendix section 11 — agent2_strict_left_deflation.md

# Strict-left dual-root deflation for the virtual-probe argument

This supplements `agent3_virtual_root_lemma.md`. All estimates below hold on a
sufficiently late actual orbit tail; constants may depend on the fixed probe
zeta, but not on the tail index. Write the index for consecutive restart blocks.

## 1. Exact identities and separation

Retain only the spectral nodes which never disappear; all weights p_{k,i} are
positive. Let d_i be the derivative at lambda_i of the polynomial through
these nodes, f_k the monic primal degree-s polynomial, N_k its norm, and H_k
the monic dual polynomial. Set q_{k,i}=1/(d_i^2 p_{k,i}) without normalizing.
Duality and the primal update give exactly

    H_k(lambda_i)=d_i p_{k,i} f_k(lambda_i)/N_k,
    H_{k+1}(lambda_i)/H_k(lambda_i)=f_k(lambda_i)f_{k+1}(lambda_i)/N_{k+1},
    q_{k+2}=constant*q_k*(H_k/H_{k+1})^2,
    q_{k,i}H_k(lambda_i)^2=p_{k,i}f_k(lambda_i)^2/N_k^2.          (1)

Thus sum_i q_{k,i}H_k(lambda_i)^2=1/N_k, uniformly bounded above and below.
Choose a fixed probe zeta below c, arbitrarily close to c, avoiding all spectral
nodes and limiting primal zeros. All non-strict slow dual roots are above zeta.
Every actual spectral node below zeta is a strict contractor and its primal
weight is O(rho^k), some rho<1. Each corresponding dual root a_{k,j} is simple,
is separated from all other limiting roots, and is lambda_j+O(rho^k).
These statements follow directly from (1), uniform primal Gram invertibility,
and the simple-root implicit function theorem. Uniform Gram invertibility on
the orbit closure follows from N_k>=N_0>0: a singular limiting degree-(s-1)
Gram matrix would put the limiting measure on at most s-1 nodes, making the
monic degree-s norm zero. In fact support at most s also contradicts N_0>0.

Let D_k(x)=product_j(x-a_{k,j}) over precisely these strict-left roots, and let
Hhat_k=H_k/D_k. All roots of Hhat_k are uniformly above zeta on this tail.
Hhat_k is EXACTLY the monic orthogonal polynomial for the positive measure
qhat_{k,i}=q_{k,i}D_k(lambda_i)^2: its orthogonality against x^j follows by
orthogonality of H_k against D_k x^j, whose degree is at most deg(H_k)-1.
Moreover,

    qhat_{k+2}=constant*qhat_k*(Hhat_k/Hhat_{k+1})^2*E_k,
    E_{k,i}=[D_{k+2}(lambda_i)/D_{k+1}(lambda_i)]^2.             (2)

Off the strict-left spectral nodes, E_{k,i}=1+O(rho^k). At strict-left nodes
this relative estimate is NOT asserted. Instead E_{k,i} is uniformly bounded:
use (1) to write its square root as

    D_{k+2}/D_{k+1}=(f_{k+1}f_{k+2}/N_{k+2})*(Hhat_{k+1}/Hhat_{k+2}).

The primal factor is bounded; the hatted evaluations at these left nodes are
bounded away from zero. Most importantly, the cancellation

    qhat_k Hhat_k^2=q_k H_k^2=p_k f_k^2/N_k^2                 (3)

means the strict-left part of this measure is O(rho^k), with total mass 1/N_k.
There is no reciprocal-Gram condition number hidden in these estimates.

## 2. Adding an infinitesimal primal probe

For a fixed triple k,k+1,k+2, add primal weight eta at zeta at time k. Use eta
as CURRENT probe weight, not as probe weight at the start of the infinite
orbit. The latter coefficient can grow or decay exponentially. Renormalizing
the perturbation parameter separately on each triple multiplies all three
virtual displacements by one positive number and changes neither their ratios
nor the signed root inequality.

The augmented dual polynomial tends to (x-zeta)H_j as eta decreases to zero.
Its extra root is a_j(eta)=zeta+eta alpha_j+O(eta^2). With the current-time
normalization, alpha_k=-P_n(zeta)f_k(zeta)/(N_k H_k(zeta)). It is bounded away
from zero and infinity uniformly in k. The same holds for alpha_{k+1} and
alpha_{k+2} with this common triple normalization: the probe primal weights
over this finite triple have ratios f_j(zeta)^2/N_j, bounded away from zero
and infinity. Their ratios are the ratios from the initial-weight convention
used in agent3's lemma, hence obey its exact beta formula.

Uniformly for small eta, the augmented strict-left roots stay
lambda_j+O(rho^k). Indeed the augmented primal coefficients and their eta
derivatives are uniformly bounded by the uniformly positive primal Gram
matrix, while (1) at a strict-left node has its O(p_{k,j}) factor. Thus (2),
(3), the bounds on E, and their errors hold uniformly for small eta. The
augmented hatted extra root is now its leftmost root.

## 3. Uniform error at the displacement scale

Use the same Rayleigh trial as agent3's exact argument, namely the next hatted
polynomial divided by x-a_{k+1}(eta). Let

    mu_i=qhat_{k,i} Hhat_k(lambda_i)^2,
    R_E=sum_i E_i mu_i lambda_i/(lambda_i-a)^2
        /sum_i E_i mu_i/(lambda_i-a)^2,
    R_1=the same quotient with E identically one,

where a=a_{k+1}(eta). Scalar normalizations cancel. The only spectral node
within fixed distance of zeta is the probe itself. By (3), at every original
node mu_i is uniformly bounded, and its strict-left part is O(rho^k). At the
probe mu_zeta is comparable to eta, since q_zeta is comparable to eta^-1 and
Hhat_k(zeta) is comparable to eta alpha_k. Consequently the denominator of
each quotient is comparable to eta^-1.

CRUCIAL: subtract zeta before estimating the numerator:

    R_E-zeta = [sum_i E_i mu_i(lambda_i-zeta)/(lambda_i-a)^2]
               /[sum_i E_i mu_i/(lambda_i-a)^2].              (4)

The probe's numerator term is EXACTLY ZERO. Therefore each numerator is O(1),
the numerator difference is O(rho^k), and the denominator relative difference
is O(rho^k). (At strict-left nodes use small mu and bounded E; elsewhere use
E=1+O(rho^k).) Equation (4) yields

    R_E-R_1=O(eta rho^k),                                    (5)

uniformly on the tail. An O(rho^k) estimate without the eta factor would NOT
suffice; (4) is what gives the required factor.

The Rayleigh bound and agent3's unperturbed first-order calculation now give

    alpha_{k+2} <= alpha_{k+1}^2/alpha_k + O(rho^k)

with the current-weight triple normalization, whose alpha's are uniformly
nonzero and bounded. Therefore, writing beta_k for the exact common-parameter
ratio, one obtains

    sign(alpha_k)*(log beta_{k+1}-log beta_k) <= C rho^k.       (6)

The signs are fixed on the tail. If beta_k -> beta_infinity>0, summing the
geometric tail of (6) gives

    sign(alpha_k)*(log beta_k-log beta_infinity) >= -C' rho^k. (7)

This is precisely the exponentially perturbed virtual-root inequality needed
in the lower-s=3 proof. All limits in eta were taken separately at fixed
finite triples; uniform estimates were needed only for the explicit error
coefficient in (5), and were established above.

## 4. Comparison with deficit

In a hard case with an active negative-neutral outsider, sum t_k=infinity
and t_{k+1}/t_k ->1. Thus rho^k=o(t_k). Dividing (7) by t_k leaves the same
limiting signed inequality as if there had been no strict-left spectral nodes.
This applies at every fixed zeta<c; the subsequent zeta -> c limit is handled
by agent4's general-zeta/P_5(zeta) calculation (including P_5(c)=0).


---

# Appendix section 12 — agent3_single_negative_edge_closure.md

# Single-negative monomial closes the hard cubic edge (agent 3)

Assume the hard s=3 configuration: P=prod_{i=1}^5(x-lambda_i),
fg=L+P(x)(x-c), and the only nonconstant limiting weight coordinate is
theta in [a,b], with c<a<b and d_a=P'(a)>0, d_b=P'(b)<0.
All active negative-neutral outsiders satisfy z>c. Let t_k=L-N_(2k).
The virtual-root lemma supplies, uniformly along the actual orbit,

    liminf I_k/t_k >= 0,

where A_k=-t_k and I is the canonical first-order linear functional
I=-(cA+B)+sqrt(f(theta)g(theta))*K/(theta-c).

For a fixed negative-neutral spectral node z, define the smooth-on-(a,b)
function Phi_z by

    Phi_z'(theta)=-(f(theta)g(theta)+L)
                  /[P(theta)(theta-c)(z-theta)].

The pole at theta=z cancels because f(z)g(z)+L=0. Only the poles at a,b
matter on the closed edge. Their residues are

    eta_a=2L/[P'(a)(a-c)(a-z)],
    eta_b=2L/[P'(b)(b-c)(b-z)].

Thus Phi_z=eta_a log(theta-a)+eta_b log(b-theta)+G_z(theta), where G_z
extends smoothly with bounded derivatives to [a,b]. This formulation also
handles c coinciding with another positive base node: its possible double
pole is strictly outside [a,b] and is absorbed in G_z.

If c<z<a, eta_a>0, eta_b<0, so Phi_z is a proper increasing bijection
(a,b)->R. If z>b, eta_a<0, eta_b>0, so it is proper decreasing.

## An actual exact-iteration scalar

On a sufficiently late even tail, factor the exact monic dual polynomial as

    H_k(x)=D_k(x)(x-theta_k),

where D_k consists of every root converging to a vanished outsider. All those
roots remain uniformly separated from [a,b]. Repeated eigenvalues were
already combined. Exact interpolation gives, for each base endpoint i=a,b,

    p_(k,i)=N_k D_k(lambda_i)(lambda_i-theta_k)/(d_i f_k(lambda_i)).

Here d_i is the derivative of the polynomial through ALL active spectral
nodes. Consequently

    p_(k,a)=C_(k,a)(theta_k-a),
    p_(k,b)=C_(k,b)(b-theta_k),

with C_(k,a),C_(k,b)>0 converging to nonzero constants, uniformly as theta
approaches either face. Moreover, over a two-block update,

    Delta log C_(k,i)=o(t_k), i=a,b.                              (1)

Indeed, Delta N and the even-polynomial coefficient change are O(t_k^2)
by the Lyapunov gain bound and polynomial TV. Strict-outsider dual roots
move exponentially. A negative-neutral dual root differs from its spectral
node by O(p_z)=O(t_k^2), and moves O(t_k p_z) over two blocks. A possible
positive-neutral outsider at c has root displacement O(p_c), p_c->0, and
moves O(t_k p_c)=o(t_k). These follow uniformly from the exact dual identity
H_k(lambda_i)=d_i p_(k,i)f_k(lambda_i)/N_k and simple-root implicit inversion.

Define the exact scalar

    Psi_k=log p_(k,z)+eta_a log p_(k,a)+eta_b log p_(k,b)+G_z(theta_k).

It differs from log p_(k,z)+Phi_z(theta_k) by a bounded scalar converging
to a constant. The canonical first-order identity is

    growth_z + Phi_z'(theta)*theta_dot =
       -4A/L+4I/[L(z-c)].                                      (2)

Equation (2), (1), and the analytic two-block map expansion imply uniformly,
INCLUDING theta arbitrarily close to a or b,

    Psi_(k+1)-Psi_k = 4t_k/L+4I_k/[L(z-c)]+o(t_k).               (3)

Uniformity of logarithmic Taylor remainders at faces follows from exact
face invariance: Delta theta has factors (theta-a)(b-theta), so relative
endpoint changes are O(t_k); their log-Taylor errors are O(t_k^2).

By liminf I/t>=0, (3) is >=2t_k/L eventually. A positive, nonannihilated
negative-neutral coordinate forces sum_k t_k=infinity: otherwise its exact
two-block logarithmic multiplier, O(t_k), would be summable and p_(k,z)
could not tend zero. Thus Psi_k->+infinity.

Since log p_(k,z)<=0, the bounded-difference identity forces
Phi_z(theta_k)->+infinity. Therefore theta_k->b if z<a, and theta_k->a
if z>b. Either conclusion gives convergence of the even weight vector.
In particular a bracketing pair of active negative outsiders is impossible.
This finishes the hard cubic edge as soon as the virtual-root liminf
inequality is fully justified with strict-left deflation.


---

# Appendix section 13 — agent2_normal_form_proof.md

# Derivation of the weighted two-block normal form (arbitrary s,t)
Let base nodes lambda_i (m=s+t+1) satisfy f_i g_i=N>0, monic f,g degree s. Set d_i=P_m'(lambda_i), monic dual H degree t, and p_i=N H_i/(d_i f_i)>0. The partner weights are pp_i=H_i f_i/d_i. Both sums are one by Lagrange interpolation, and f,g are their monic OP_s, each of squared norm N. This follows because degree(H*x^j)<=m-2 for j<s and degree(H*f)=m-1 with leading coefficient one.
Use the analytic base-weight chart
 p_i=C(H,u) H_i/[d_i(f+u)_i], C^{-1}=sum H_i/[d_i(f+u)_i],
and append outside weights z_mu, scaling base weights by 1-sum z. Orthogonality and the squared norm identity still hold exactly for the conditional base distribution, with f+u its monic OP and norm C. The full-distribution monic OP differs from f+u by O(|z|), analytically, because its moment Gram matrix is nonsingular.

Put u=epsilon*w and z_mu=epsilon^2 Z_mu, where outside nodes obey f_mu*g_mu=-N. Fix H in a compact region of the positive chart. With v(x)=(1,x,...,x^(s-1)), V_i=v(lambda_i)^T, define
 M=sum p_i V_i V_i^T, Mp=sum pp_i V_i V_i^T,
 dg=-Mp^{-1} M w,
 A=delta N=N^2 sum H_i w_i/(d_i f_i^2),
 R_i=(g_i w_i+f_i dg_i-A)/N.
The one-block partner conditional weights are exactly H_i(f+u)_i/d_i, so differentiating their monic OP equations gives dg=-Mp^{-1}M w. Differentiating C gives A. Differentiating the partner squared norm also gives A, since sum H_i w_i g_i^2/d_i equals the displayed A.
Consequently if K is the product of the consecutive full-distribution monic OPs and N0,N1 their norms, then
 K_i=N+epsilon*(g_i w_i+f_i dg_i)+O(epsilon^2),
 N0=N+epsilon*A+O(epsilon^2), N1=N+epsilon*A+O(epsilon^2).
The two-block base-weight ratio is therefore 1+2epsilon R_i+O(epsilon^2). The base OP changes only by O(epsilon^2), as follows also from the identity below. Since C(H,0)=N identically in H, recovering the dual chart gives
 H^+=H+2epsilon*dh+O(epsilon^2), dh(lambda_i)=H_i R_i.
The right side is a polynomial of degree<t, by the differentiated exact dual relation; for t=1 it is a constant.

## Exact polynomial increment identity
For any exact weighted residual orbit let f0,f1,f2 be three consecutive monic OPs, K=f0*f1, norms N0,N1, and p2=p*K^2/(N0*N1). Orthogonality implies
 sum p f0 v=0, sum p f0 K v=0.
Thus
 M(p2)*(f2-f0)=-1/(N0*N1) sum p f0 (K-N0)^2 v.          (EXACT)
Its Taylor expansion on base nodes is
 -epsilon^2 M^{-1} sum p_i f_i R_i^2 V_i+O(epsilon^3).
At each negative-level outside node, K-N0=-2N+O(epsilon), giving the contribution
 -4epsilon^2 M^{-1} sum Z_mu f_mu v(mu)+O(epsilon^3).
Full-vs-conditional OP corrections are O(z); their change over two blocks is O(epsilon^3) because z^+-z=O(epsilon^3), H^+-H=O(epsilon), u^+-u=O(epsilon^2), so the same leading increment applies to u. Hence
 u^+=u+epsilon^2*W(H,w,Z)+O(epsilon^3),
 W=-M^{-1}[sum p_i f_i R_i^2 V_i+4 sum Z_mu f_mu v(mu)].
The outside weights satisfy
 z_mu^+=z_mu*[1+epsilon*ell_mu+O(epsilon^2)],
 ell_mu=2(w_mu/f_mu+dg_mu/g_mu)-2A/N.

All statements have uniformly bounded state derivatives on compact positive charts: the exact finite weighted-map formulas and chart inverses are analytic and all Gram matrices stay nonsingular. Now set epsilon_k=1/(k+K), epsilon_{k+1}=epsilon_k/(1+epsilon_k). Rescaling u=epsilon*w,z=epsilon^2 Z gives exactly
 Y^+=Y+epsilon*V(Y)+epsilon^2*bounded analytic remainder,
 V=(2dh, w+W, Z_mu*(2+ell_mu)).
This is the vector field implemented by agent2_blowup_ode.py, and (for s4,t1) by the algebraically simplified interval field. The derivation establishes the expansion independently of numerical difference tests; those tests only audit the implementation.

## Rational simplifications used by the interval implementation (s4,t1)
Let H=x-theta. The moment matrices M(theta),Mp(theta) are affine in theta. Their determinants satisfy
 det M(theta)=c*f(theta), det Mp(theta)=cp*g(theta).
This is an exact algebraic identity, not merely interval residual inclusion: if zeta is any root of f, the coefficient vector of f(x)/(x-zeta), degree s-1, lies in ker M(zeta), since the jth component of its image equals N sum_i lambda_i^j/d_i=0 for j<s. The determinant has degree <=s and f has s distinct roots; comparing leading coefficients gives the identity. The same argument uses g for Mp. In the example c,cp are nonzero (the finite interval coefficient bounds verify this), and the resulting inverses are adjugate polynomial matrices divided by c*f(theta),cp*g(theta).

The scalar dual increment is Hdot=2dh, and R_i=Hdot/[2(lambda_i-theta)]. Thus
 sum_i p_i f_i R_i^2 v_i
 =N Hdot^2/4 sum_i v_i/[d_i(lambda_i-theta)]
 =-N Hdot^2 v(theta)/[4P_m(theta)],
where the last equality is the exact barycentric partial-fraction identity, valid componentwise because deg(x^j)<m-1. Hence the homogeneous w increment is
 +N/[4P_m(theta)] M(theta)^{-1}v(theta)*thetadot^2.
The first-coordinate formula can use node lambda=0:
 thetadot=2theta/N*[g(0)w(0)+f(0)dg(0)-A].
These identities give exactly the b,K,force,L rational coefficient formulas in agent4_interval_blowup.py, with K=-N M^{-1}v(theta)/(4P_m(theta)) and wdot=w-K*thetadot^2+force*Z.


---

# Appendix section 14 — agent1_floquet_tube_theorem.md

# Explicit Floquet-tube existence certificate

Let G be C2 autonomous on R^(d+1). Let gamma(s), P(s) be periodic, piecewise C2/C1 respectively, P invertible; piecewise smoothness with finitely many knots suffices. Fix D=diag(0,Dn), with Dn real block diagonal, each block either a nonzero real scalar or [[u,-v],[v,u]] with u nonzero. Use the maximum of scalar absolute values and Euclidean norms of the 2D blocks, including the scalar phase block. Then exp(t Dn) on stable/unstable blocks has exact exponential rate, and the whole-line/periodic Green operator for d/ds-Dn has norm at most 1/alpha, alpha=min |Re spec Dn|.

Define
 a=P^-1 gamma', B=P^-1 P', d=P^-1(G(gamma)-gamma'),
 E=P^-1(DG(gamma) P-P')-D.
All bounds below are in the indicated block norm and its induced multilinear norms, on every s in [0,1]. Suppose
 ||d||<=delta, ||E[:,normal]||<=e, a_0>=astar>0, ||a_normal||<=anorm,
 ||B[:,normal]||<=b, ||Dn||<=dmax,
and ||P^-1 D2G(gamma+P(0,eta))[P(0,u),P(0,v)]||<=H||u||||v|| for ||eta||<=rho.

Set
 r=delta+e*rho+H*rho^2/2,
 qbar=r/(astar-b*rho),
 qLip=(e+H*rho+b*qbar)/(astar-b*rho),
 Nbar=r+(anorm+(b+dmax)*rho)*qbar,
 fbar=Nbar/(1-qbar),
 LipN=e+H*rho+(b+dmax)*qbar+(anorm+(b+dmax)*rho)*qLip,
 Lipf=LipN/(1-qbar)+Nbar*qLip/(1-qbar)^2.

**Certificate inequalities:**
 b*rho<astar, qbar<1, fbar<alpha*rho, Lipf<alpha.
Then G has a periodic orbit entirely in the tube gamma(s)+P(s)(0,eta), ||eta||<rho. It has exactly the one neutral multiplier associated to phase; all normal multipliers are off the unit circle. If the theta-component range of gamma exceeds twice rho*sup ||theta-row(P_normal)||, theta on this orbit is nonconstant.

## Proof, including phase correction
Write x=gamma(s)+P(s)v with v=(0,eta), and let dot denote physical G-time. Taylor's theorem gives
 vdot+(a+Bv)(sdot-1)=d+(D+E)v+R(s,eta),
 ||R||<=H||eta||^2/2, ||Deta R||<=H||eta||.
The first component imposes sdot=1+q, where
 q=[d0+(Ev)0+R0]/[a0+(Bv)0].
The displayed bounds give |q|<=qbar and ||Deta q||<=qLip. In particular phase is strictly increasing. Dividing normal equation by sdot yields
 deta/ds=Dn eta+f(s,eta),
 f=[dn+(Ev)n+Rn-(an+(Bn+Dn)eta)q]/(1+q).
Here Bn+Dn means B restricted to normal columns/normal output plus Dn. Quotient and product rules give ||f||<=fbar and ||Deta f||<=Lipf as displayed.

On the Banach space of continuous periodic normal functions of norm<=rho, solve eta=Green(f(.,eta)). The map sends the closed ball strictly inside itself and is a strict contraction. Its unique fixed point is piecewise C1. Its image x(s) is an actual smooth G-orbit after the strictly positive time change; period equals integral_0^1 (1+q(s,eta(s)))^-1 ds. Knot regularity causes no issue because x solves the same autonomous ODE on adjacent intervals.

For normal hyperbolicity, the variational equation in the phase coordinate has the form z'=(Dn+Delta(s))z with ||Delta||<=Lipf<alpha. For any 0<beta<alpha-Lipf, the stable-past/unstable-future Green operator in the exponentially beta-weighted norm has norm <=1/(alpha-beta), so perturbation by Delta is a contraction. This constructs an exponential dichotomy, hence excludes all unit-circle normal multipliers. Phase contributes exactly one neutral multiplier. Positive time changes preserve the normal return map.

## Convenient exact tangent column
Taking P[:,0]=gamma' makes a=e0 exactly, so astar=1 and anorm=0. Gamma can be C2 periodic Hermite/quintic and P can have this exact polynomial derivative as its first column. If instead a is merely close to e0, use the general bounds above.

## Converting coordinate infinity bounds
For one real 2D rotational Floquet block, ||z||_infty<=||z||_block<=sqrt(2)||z||_infty. Thus safe block bounds for vectors, operators, and the stated Hessian are sqrt(2) times their coordinate-infinity bounds (inputs of block norm<=1 have coordinate-infinity norm<=1). The scalar a0 lower bound is unchanged. Bounds on dmax can be computed directly blockwise: |lambda| for real blocks and sqrt(u^2+v^2) for rotational blocks.


---

# Appendix section 15 — agent4_parabolic_lifting_theorem.md

# Parabolic lifting of a hyperbolic logtime periodic orbit

**Conditional theorem (independent of whether such an orbit has been certified).**
Let an exact analytic map in coordinates `(h,u,z)` have weighted expansion

    h+ = h + B(h)u + O(epsilon^2),
    u+ = u + Q(h,u) + F(h)z + O(epsilon^3),
    z_i+ = z_i [1 + L_i(h)u + O(epsilon^2)],

uniformly on compact sets under `u=epsilon*w, z=epsilon^2*Z`; Q is quadratic.
Here a term O(epsilon^j) and its state derivatives have that uniform bound.
Put

    V(h,w,Z) = (B(h)w,
                 w+Q(h,w)+F(h)Z,
                 Z_i*(2+L_i(h)w)).

If V has a nonconstant hyperbolic periodic orbit Gamma, contained in the
interior of the coordinate domain and with every Z_i>0, then an exact forward
orbit of the map exists, with

    dist((h_k,(k+K)u_k,(k+K)^2 z_k), Gamma) -> 0.

More precisely the scaled orbit shadows one complete forward traversal after
another, with asymptotic phase `tau_k + phi + o(1)`, where
`tau_k=sum_{j=0}^{k-1}1/(j+K)=log(k+K)+constant+o(1)`.
Thus if h is nonconstant on Gamma, h_k does not converge.

## Proof

Set epsilon_k=1/(k+K), so epsilon_{k+1}=epsilon_k/(1+epsilon_k).
Exact rescaling gives a nonautonomous map

    Y_{k+1}=Y_k+epsilon_k V(Y_k)+epsilon_k^2 R(Y_k,epsilon_k),

where R and its first state derivatives are uniformly bounded in a fixed
compact tubular neighborhood of Gamma. This is an identity, not a formal
truncation: analyticity of the original map and its weighted Taylor remainder
give bounded R, extending continuously (indeed smoothly) to epsilon=0.

Let gamma(s) parametrize Gamma by V-flow time, with period T. Hyperbolicity
means its variational equation has precisely one unit multiplier, the simple
tangent multiplier, and all normal multipliers avoid the unit circle.
Choose a periodic adjoint covector ell(s) with ell(s)gamma'(s)=1; the normal
bundle is ker ell(s). In smooth tubular coordinates `(s,e)`, where e is in
that normal bundle, the ODE has

    s' = 1+O(|e|^2),
    e' = A(s)e+O(|e|^2).

The absence of a linear normal term in s' follows from the adjoint equation.
Use a periodic frame of the normal bundle (or pass to period 2T if necessary).
Its normal fundamental solution U(t,s) admits stable and unstable projections
P^s,P^u and constants C,alpha>0 with

    ||U(t,s)P^s(s)|| <= C exp(-alpha*(t-s))  (t>=s),
    ||U(t,s)P^u(s)|| <= C exp(-alpha*(s-t))  (t<=s).

Fix phi and write s_k=tau_k+phi+eta_k. Using the exact flow propagator over
[tau_k,tau_{k+1}] in the linear normal term, the scaled map is exactly

    eta_{k+1}-eta_k = a_k(eta_k,e_k),
    e_{k+1} = U(tau_{k+1}+phi,tau_k+phi)e_k + f_k(eta_k,e_k),

where, on a fixed small tube,

    |a_k| <= C[epsilon_k*|e_k|^2+epsilon_k^2],
    |f_k| <= C[epsilon_k*(|e_k|^2+|eta_k|*|e_k|)+epsilon_k^2].

The first-derivative versions of these bounds also hold, with a term
C*epsilon_k^2 in the Lipschitz constants. Uniformity follows from periodicity.
The dependence of A on eta is included in f_k. Local Euler-vs-flow error is
O(epsilon_k^2) and is also included in f_k.

Choose 0<beta<min(alpha,1), reducing alpha if needed. On the Banach space
with norm

    ||(eta,e)||_beta = sup_{k>=0} (k+K)^beta*(|eta_k|+|e_k|),

define the graph transform by

    eta_k = -sum_{j=k}^infinity a_j,
    e_k = sum_{j=0}^{k-1} U(tau_k+phi,tau_{j+1}+phi) P^s_{j+1} f_j
          -sum_{j=k}^infinity U(tau_k+phi,tau_{j+1}+phi) P^u_{j+1} f_j.

Thus the stable initial component is set to zero; any sufficiently small
stable initial component could instead be specified. These series converge.
The elementary estimate `tau_k-tau_j = log((k+K)/(j+K))+O(1/K)` converts the
exponential dichotomy estimates to power estimates. Weighted convolution of
an O((j+K)^(-1-2beta)) source is O((k+K)^(-beta))*O(K^(-beta)); weighted
convolution of an O((j+K)^(-2)) source is
O((k+K)^(-beta))*O(K^(beta-1)). The same estimates hold for the future phase
sum. In particular, on a fixed radius-r ball the transform has norm at most

    C[r^2*K^(-beta)+K^(beta-1)]

and Lipschitz constant at most `C[r*K^(-beta)+K^(-1)]` (enlarging C harmlessly).
Take K sufficiently large. The transform maps the ball into itself and is a
strict contraction. Its fixed point gives an exact scaled-map orbit satisfying
eta_k,e_k=O((k+K)^(-beta)). In particular e_k->0 and eta_k->0.

Finally tau_k is increasing, tends to infinity, and has increments tending to
zero. Modulo T it therefore approaches every phase along subsequences. Every
point of Gamma is a cluster point of Y_k. Any coordinate nonconstant on Gamma
fails to converge. Positivity and membership in the original coordinate chart
hold for large K because Gamma is compact in its interior. This proves the
theorem.

## Application to restarted residual map

Take base conditional weights p_i on m=s+t+1 nodes. With monic base residual
polynomial f_u and monic dual H_h,

    p_i = C H_h(lambda_i)/(d_i f_u(lambda_i)),
    C^(-1)=sum_i H_h(lambda_i)/(d_i f_u(lambda_i)).

This is an analytic coordinate chart whenever these weights are positive.
Orthogonality follows from Lagrange interpolation, since deg(H*x^j)<=m-2
for 0<=j<s; its monic squared norm equals C. Append small outside weights z_i
and renormalize the base weights by (1-sum z_i). This gives analytic spectral
weights of an actual residual vector. The exact two-block map has the weighted
expansion used above (to be verified/certified from its finite rational formulas).
If h is nonconstant on the periodic orbit, base weights are nonconstant: for
fixed limiting f, p_i are proportional to H_h(lambda_i)/f(lambda_i). Thus even
normalized residual directions fail to converge, irrespective of signs.
All weights stay positive, so there is no finite termination.


---

# Appendix section 16 — agent4_interval_blowup_README.md

# Interval blowup field: formulas and guarantees

Implementation: `agent4_interval_blowup.py`.
Checks: `agent4_interval_blowup_checks.py` (RAN, all passed).

**Convention:** state is `(theta,w0,w1,w2,w3,Z0,Z1)` with theta POSITIVE;
the earlier shared `BlowupODE` instead uses h=-theta.

Parameters q1,q2,N are exact rationals passed as strings. Form
P6=prod(x-lambda), lambda=(-3,-1,0,1,2,3), Q2=(x-q1)(x-q2).
The exact eight real roots of P6 Q2+N are isolated by SymPy's exact rational
Sturm intervals, each of width <=10^(-floor(.302*bits)-20). The factor f uses
ordered indices 0,3,5,6; g uses 1,2,4,7. The negative outside eigenvalues are
ordered roots 1,6 of P6 Q2+2N. All roots are simple; the constructor asserts
these facts by exact isolation. Interval/ball coercions and every subsequent
arithmetic operation round outward. The construction works at both candidate
q1=-289/400 and the newer q1=-143/200; N=3/50,q2=17/10 by default.

Write d_i=P6'(lambda_i), H_i=lambda_i-theta and V_ij=lambda_i^j, j=0..3.
Then p_i=N H_i/(d_i f_i), p'_i=H_i f_i/d_i, and
M=V^T diag(p)V, Mp=V^T diag(p')V. Both M,Mp are affine in theta.
The first-order partner polynomial perturbation is dg=-Mp^(-1)M w and
D=deltaN=N sum_i p_i w_i/f_i. For the limiting two-cycle, f_i*g_i=N exactly;
for the negative nodes, f_mu*g_mu=-N exactly. The code uses these exact
identities to remove avoidable interval dependence.

The rational coefficient form is

 theta' = b(theta) w =: v,
 w' = w-K(theta) v^2 + Force(theta) Z,
 Z_mu' = Z_mu [2+L_mu(theta) w].

Here

 K= -N/(4P6(theta)) M^(-1) (1,theta,theta^2,theta^3)^T,
 Force_mu=-4 f_mu M^(-1) (1,mu,mu^2,mu^3)^T,
 L_mu w=2[w(mu)/f_mu+dg(mu)/g_mu]-2D/N,
 b_j=2theta/N [g(0)*1_(j=0)+f(0)*DG_(0,j)-D_j], DG=-Mp^(-1)M.

The b formula evaluates theta'=-2H_i*ratio_i at the base node lambda_i=0,
where ratio_i=(g_i*w_i+f_i*dg_i-D)/N. All six nodal values agree exactly
(the first-order dual polynomial is monic linear). For K, use
sum_i lambda_i^j/[d_i(lambda_i-theta)]=-theta^j/P6(theta), j<=4;
this follows from partial fractions of z^j/P6(z).

## No interval matrix inversions at runtime

The Christoffel determinant identities are

 det M(theta)=c*f(theta), det Mp(theta)=cp*g(theta),

where c,cp are the degree-four leading determinant coefficients. They follow
by applying the Christoffel determinant formula to the signed base weights
1/(d_i f_i) and f_i/d_i. The associated degree-four monic orthogonal polynomials
are f and g, as checked directly by Lagrange interpolation. Both are polynomial
identities and remain valid without any positivity assumption on those signed
auxiliary weights. The code also computes all determinant coefficients by
permutation expansion and asserts every coefficient difference encloses zero.

Adjugate entries are polynomials of degree <=3. All numerators for b,K,Force,L
are precomputed and combined algebraically BEFORE interval/PS evaluation:

 b=nb/g(theta), K=nK/[f(theta)P6(theta)],
 Force=nForce/f(theta), L=nL/g(theta).

`coefficient_formulas(theta)` accepts a generic ring scalar, including power
series over RBF/RIF. `field_generic(y)` never coerces the input scalars.
`field_jac_hess(y)` computes first and second derivatives by univariate Jet2
coefficient differentiation, followed by the explicit polynomial-in-(w,Z)
chain rule. It works for interval/ball boxes and for PS scalars alike.

`transformed(W,Zscale)` returns the field with original w=W*wnew and
original Z=Zscale*Znew; theta is unchanged. The rational polynomial numerators
are combined with W and W^(-1) ONCE, before evaluating any uncertain theta.
This is important for interval Taylor conditioning. The same transformed object
provides full interval field/Jacobian/Hessian and generic PS evaluation.

## Independent checks performed

* Interval and ball arithmetic both tested at five phases, three independent
  integer directional Taylor seeds per phase: generic multivariate PS field
  coefficients agree with explicit analytic F, J*d, (d^T H d)/2, with every
  difference interval containing zero.
* Twenty random corners of a genuine box were enclosed componentwise by its
  field, Jacobian, and Hessian interval evaluations.
* Original field agrees with shared independently-coded double formulas to
  3.2e-11 at a sample phase.
* With agent2's exact-ball whitening W,Zscale, transformed field agrees with
  independently-coded WhiteGenericField to 5.7e-82 at 300 bits.
* Dynamical order16 Taylor jets in transformed coordinates took .029 seconds;
  coefficient radii were ~8e-73 at order1 and ~6e-46 at order16 (300 bits).

These are finite implementation checks, NOT the periodic-orbit interval
existence certificate, which is a separate computation owned by agent2.
